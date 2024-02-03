from google.cloud import aiplatform
from vertexai import preview



predict_custom_trained_model_sample(
    project="391102393555",
    endpoint_id="3318370073093079040",
    location="us-east1",
    instances={ "instance_key_1": "value", ...}
)
