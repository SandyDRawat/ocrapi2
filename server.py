import runpod
import torch
from transformers import AutoModel, AutoTokenizer, AutoProcessor
from PIL import Image
from io import BytesIO
import os
from base64 import b64decode

# Define local model path
MODEL_PATH = "/app/model/MiniCPM-V-2_6-int4"

# Check if GPU is available
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load model, tokenizer, and processor from local path
def load_local_model(model_path: str, device: str):
    model = AutoModel.from_pretrained(model_path, trust_remote_code=True)
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    processor = AutoProcessor.from_pretrained(model_path, trust_remote_code=True)
    return model, tokenizer, processor

# Load model at startup
try:
    model, tokenizer, processor = load_local_model(MODEL_PATH, device)
    model.to(device)
    model.eval()
except Exception as e:
    print(f"Error loading model: {e}")
    exit(1)

# RunPod Serverless Handler
def handler(event):
    try:
        input_data = event.get("input", {})
        image_bytes = input_data.get("image")
        question = input_data.get("question", "")

        if not image_bytes:
            return {"error": "No image provided"}

        # Convert base64 string to PIL image
        image = Image.open(BytesIO(b64decode(image_bytes))).convert("RGB")

        # Prepare input
        msgs = [{"role": "user", "content": [image, question]}]

        # Run inference
        with torch.no_grad():
            answer = model.chat(image=None, msgs=msgs, tokenizer=tokenizer)

        return {"answer": "".join(answer)}

    except Exception as e:
        print(f"Error during generation: {e}")
        return {"error": f"An error occurred: {e}"}

# Start RunPod serverless
runpod.serverless.start({"handler": handler})
