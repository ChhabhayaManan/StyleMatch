import torch
from huggingface_hub import login
from dotenv import load_dotenv
load_dotenv()
import os
from sam3.model_builder import build_sam3_image_model

"""Module to load the SAM3 model for image segmentation."""

login(token=os.environ["HUGGINGFACEHUB_API_TOKEN"])
model = None

print("Sam3 is loading......")
device = "cuda" if torch.cuda.is_available() else "cpu"

try:
    #building model
    model = build_sam3_image_model()
    model.eval()
    model.to(device)

    print("Successfully Loaded")
except Exception as e:
    print("Model loading failed")
    print(e)