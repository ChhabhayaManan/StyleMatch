from sentence_transformers import SentenceTransformer
import torch

print("CLIP model is loading......")
clip_model = None
try:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    clip_model = SentenceTransformer('clip-ViT-B-32', device=device)
    print("CLIP model loaded successfully.")
except Exception as e:
    print(f"Error loading CLIP model: {e}")
    clip_model = None
