import runpod
#import torch
#from transformers import AutoModel, AutoTokenizer, AutoProcessor
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
    seconds = input.get('seconds', 0)

    # Just a test to confirm image was received correctly
    width, height = image.size

    msgs = [{"role": "user", "content": ["Image received", f"Question: {question}"]}]
    #time.sleep(seconds)
    return {
        "msg": "Success",
        "answer": "This is a test answer",
        "image_size": f"{width}x{height}"
    }
   # answer = model.chat(image=None, msgs=msgs, tokenizer=tokenizer)


if __name__ == '__main__':
    runpod.serverless.start({'handler': handler})
