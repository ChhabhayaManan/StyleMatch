import modal


image = (
    modal.Image.debian_slim(python_version="3.10")
    .apt_install("git")
    .run_commands(
        "git clone https://github.com/facebookresearch/sam3.git /sam3",
        "pip install -e /sam3"
    )
    .pip_install(
        # core
        "torch==2.7.0",
        "torchvision",
        "torchaudio",
        "numpy<2",
        "typing",
        "pillow",
        "psutil",

        # sam3 deps
        "timm>=1.0.17",
        "tqdm",
        "ftfy==6.1.1",
        "regex",
        "iopath>=0.1.10",
        "huggingface_hub",

        # dev extras
        "pytest",
        "pytest-cov",
        "black==24.2.0",
        "ufmt==2.8.0",
        "ruff-api==0.1.0",
        "usort==1.0.2",
        "gitpython==3.1.31",
        "yt-dlp",
        "pandas",
        "numba",
        "python-rapidjson",

        # notebooks extras
        "matplotlib",
        "jupyter",
        "notebook",
        "ipywidgets",
        "ipycanvas",
        "ipympl",
        "decord",
        "einops",
        "scikit-image",
        "scikit-learn",

        # train extras
        "hydra-core",
        "submitit",
        "tensorboard",
        "zstandard",
        "scipy",
        "torchmetrics",
        "fvcore",
        "fairscale",

        # your existing stack
        "transformers",
        "langchain",
        "langgraph",
        "pydantic",
        "gradio",
        "google-generativeai",
        "google-genai",
        "sentence-transformers",
        "pycountry",
        "faiss-cpu",
        "opencv-python",
        "python-dotenv",
        "pycocotools"
    )
    .add_local_dir(".", remote_path="/root")
    .add_local_dir("./data", remote_path="/root/data")
)

app = modal.App(image=image, name="stylematch-app")

@app.function(
        gpu="T4",
        timeout=20 * 60,
        secrets=[
             modal.Secret.from_name("hf-api-secret"),
             modal.Secret.from_name("gemini_key")
        ])
def run_workflow():
    from app.Workflows.ImgProcessingWorkflow import ImgProcessing
    from PIL import Image


    test_img_path = "/root/data/demo.jpg"
    test_img = Image.open(test_img_path)

    print("Starting workflow...")
    ImgProcessing(test_img , "Shoes")

@app.local_entrypoint()
def main():
    run_workflow.remote()
    


