from google import genai
from google.genai import types

import PIL.Image
import os
import dotenv

dotenv.load_dotenv()

GEMINI_API_KEY =  os.getenv("GEMINI_API_KEY") 
image = PIL.Image.open('C:/Users/ASUS/Desktop/runpod_ocr/example.jpg')

client = genai.Client(api_key=GEMINI_API_KEY)
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=["Extract the content form this image and convert it to latex?", image])

print(response.text)