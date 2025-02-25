import runpod
import torch
from transformers import AutoModel, AutoTokenizer, AutoProcessor
from PIL import Image
from io import BytesIO
import os
from base64 import b64decode
import time

def handler(event):
    input = event['input']
    question = input.get('question')
    image64 = input.get('image')
    image = Image.open(BytesIO(b64decode(image64)))
    #seconds = input.get('seconds', 0)

    MODEL_PATH = "/app/model/MiniCPM-V-2_6-int4"
    # Check if GPU is available
    device = "cuda"

    # Load model, tokenizer, and processor from local path
    def load_local_model(model_path: str, device: str):
        model = AutoModel.from_pretrained(model_path,trust_remote_code=True)
        tokenizer = AutoTokenizer.from_pretrained(model_path,trust_remote_code=True)
        processor = AutoProcessor.from_pretrained(model_path,trust_remote_code=True)
        return model, tokenizer, processor

    # Load model at startup
    try:
        model, tokenizer, processor = load_local_model(MODEL_PATH, device)
        model.to(device)
        model.eval()
    except Exception as e:
        print(f"Error loading model: {e}")
        exit(1)

    # Prepare input
    msgs = [{"role": "user", "content": [image, question]}]
    
    answer = model.chat(image=None, msgs=msgs, tokenizer=tokenizer)

    #time.sleep(seconds)
    return {"answer": "".join(answer)}


runpod.serverless.start({'handler': handler})
