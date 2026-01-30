import torch
from sam3.model_builder import build_sam3_image_model
from sam3.model.sam3_image_processor import Sam3Processor


print("Sam3 is loading......")
device = "cuda" if torch.cuda.is_available() else "cpu"

try:
    #building model
    model = build_sam3_image_model()
    Processor = Sam3Processor(model, confidence_threshold=0.7)
    model.eval()
    model.to(device)

    print("Successfully Loaded")
except Exception as e:
    print("Model loading failed")
    print(e)