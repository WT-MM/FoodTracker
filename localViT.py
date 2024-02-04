import requests
from PIL import Image
import torch

from transformers import Owlv2Processor, Owlv2ForObjectDetection

processor = Owlv2Processor.from_pretrained("google/owlv2-base-patch16-ensemble")
model = Owlv2ForObjectDetection.from_pretrained("google/owlv2-base-patch16-ensemble")

url = "https://www.marthastewart.com/thmb/ss0fVAXAReJJAIoMizh7yY4e-wY=/750x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/fruits-vegetables-what-season-when-getty-0323-2df940a74f2847fdaafbc7932746d16d.jpg"
image = Image.open(requests.get(url, stream=True).raw)

with open("ModifiedNames.txt", "r") as file:
    data = file.read()
    data = data.split("\n")
    

texts = [data]
print(texts)
#texts = [["carrots", "tomatoes"]]
inputs = processor(text=texts, images=image, return_tensors="pt")
outputs = model(**inputs)

# Target image sizes (height, width) to rescale box predictions [batch_size, 2]
target_sizes = torch.Tensor([image.size[::-1]])
# Convert outputs (bounding boxes and class logits) to Pascal VOC Format (xmin, ymin, xmax, ymax)
results = processor.post_process_object_detection(outputs=outputs, target_sizes=target_sizes, threshold=0.1)
i = 0  # Retrieve predictions for the first image for the corresponding text queries
text = texts[i]
boxes, scores, labels = results[i]["boxes"], results[i]["scores"], results[i]["labels"]
for box, score, label in zip(boxes, scores, labels):
    box = [round(i, 2) for i in box.tolist()]
    print(f"Detected {text[label]} with confidence {round(score.item(), 3)} at location {box}")
