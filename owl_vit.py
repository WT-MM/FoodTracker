# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START aiplatform_predict_custom_trained_model_sample]
import base64
from io import BytesIO

from typing import Dict, List, Union

from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from google.cloud import aiplatform
from PIL import Image

def parse_text_queries(tensor_byte_string):
    """Converts text query bytes to string tensor as an input for the original SavedModel."""
    return tf.io.parse_tensor(tensor_byte_string, tf.string)


def get_serve_fn(model):
    """Creates a serving function for the modified SavedModel which takes jpeg bytes and text-embeddings bytes as an input."""

    @tf.function(
        input_signature=[
            tf.TensorSpec([None], tf.string),
            tf.TensorSpec([None], tf.string),
        ]
    )
    def serve_fn(image_jpeg_bytes_inputs, text_queries_bytes_inputs):
        text_queries = tf.map_fn(
            parse_text_queries,
            text_queries_bytes_inputs,
            dtype=tf.string,
        )
        model_output = model(image=image_jpeg_bytes_inputs, text_queries=text_queries)
        return {
            "predicted_boxes": model_output["predicted_boxes"],
            "instance_logits_image": model_output["instance_logits_image"],
        }

    return serve_fn


def get_jpeg_bytes(image_path, new_width=640):
    with Image.open(image_path) as img:
        width, height = img.size
        print("original input image size: ", width, " , ", height)
        new_height = int(height * new_width / width)
        print("new input image size: ", new_width, " , ", new_height)
        new_image = img.resize((new_width, new_height))

        # Convert image to RGB if it's RGBA
        if new_image.mode == 'RGBA':
            new_image = new_image.convert('RGB')

        buffered = BytesIO()
        new_image.save(buffered, format="JPEG")
        return buffered.getvalue()


def get_text_queries_bytes(text_queries):
    """Returns text queries list as bytes."""
    tensor_array = tf.convert_to_tensor(text_queries)
    tensor_byte_string = tf.io.serialize_tensor(tensor_array)
    return tensor_byte_string.numpy()


def plot_predictions(
    image, logits, boxes, text_queries, score_threshold=0.1, max_num_boxes=200
):
    """Plots the predicted bounding boxes and labels on the given image."""
    colors = plt.cm.hsv(np.linspace(0.0, 1.0, len(text_queries)))
    logits = logits[..., : len(text_queries)]  # Remove padding.
    scores = tf.nn.sigmoid(np.max(logits, axis=-1)).numpy()
    labels = np.argmax(logits, axis=-1)

    fig, ax = plt.subplots(1, 1, figsize=(16, 16))
    ax.imshow(image, extent=(0, 1, 1, 0))
    ax.set_aspect(image.shape[0] / image.shape[1])
    ax.set_axis_off()

    num_boxes = 0
    for score, box, label in zip(scores, boxes, labels):
        color = colors[label % 10]
        if score < score_threshold:
            continue
        if num_boxes >= max_num_boxes:
            break
        num_boxes += 1

        y0, x0, y1, x1 = box
        cx, cy, w, h = (x0 + x1) / 2, (y0 + y1) / 2, x1 - x0, y1 - y0
        ax.plot(
            [cx - w / 2, cx + w / 2, cx + w / 2, cx - w / 2, cx - w / 2],
            [cy - h / 2, cy - h / 2, cy + h / 2, cy + h / 2, cy - h / 2],
            color=color,
            zorder=10 + score,
        )
        ax.text(
            cx - w / 2,
            cy + h / 2 + 0.015,
            f"{text_queries[label]}: {score:1.2f}",
            ha="left",
            va="top",
            color=color,
            zorder=10 + score,
            bbox={
                "facecolor": "white",
                "edgecolor": color,
                "boxstyle": "square,pad=.3",
            },
        )


def predict_custom_trained_model_sample(
    project: str,
    endpoint_id: str,
    instances: Union[Dict, List[Dict]],
    location: str = "us-central1",
    api_endpoint: str = "us-central1-aiplatform.googleapis.com",
):
    """
    `instances` can be either single instance of type dict or a list
    of instances.
    """
    # The AI Platform services require regional API endpoints.
    client_options = {"api_endpoint": api_endpoint}
    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    # The format of each instance should conform to the deployed model's prediction input schema.
    instances = instances if isinstance(instances, list) else [instances]
    instances = [
        json_format.ParseDict(instance_dict, Value()) for instance_dict in instances
    ]
    parameters_dict = {}
    parameters = json_format.ParseDict(parameters_dict, Value())
    endpoint = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )
    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )
    print("response")
    print(" deployed_model_id:", response.deployed_model_id)
    # The predictions are a google.protobuf.Value representation of the model's predictions.
    predictions = response.predictions
    for prediction in predictions:
        print(" prediction:", dict(prediction))



TEXT_QUERIES = ["peach", "glass", "melon", "bottle", "egg", "grape"]
image_bytes = get_jpeg_bytes("Images/fridge.png")

text_queries_bytes_inputs = get_text_queries_bytes(TEXT_QUERIES)

instances_list = [
    {
        "image_jpeg_bytes_inputs": {
            "b64": base64.b64encode(image_bytes).decode("utf-8")
        },
        "text_queries_bytes_inputs": {
            "b64": base64.b64encode(text_queries_bytes_inputs).decode("utf-8")
        },
    }
]
#instances = [json_format.ParseDict(s, Value()) for s in instances_list]
instances = instances_list

predict_custom_trained_model_sample(
    project="391102393555",
    endpoint_id="7101393760084295680",
    location="us-central1",
    instances=instances
)
