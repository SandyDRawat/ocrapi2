import base64
import requests
import json
import dotenv
import os

dotenv.load_dotenv()

RP_API_KEY =  os.getenv("RP_API_KEY") 

def send_request(image_path, question, url="https://api.runpod.ai/v2/l32k9po3kztez6/runsync"): # change the url to your server url
    # Convert image to base64
    with open(image_path, "rb") as img_file:
        base64_image = base64.b64encode(img_file.read()).decode("utf-8")

    # Prepare JSON payload (without nesting in "input")
    # Prepare payload
    data = {
        "input": {
            "image": base64_image,
            "question": question,
        }
    }

    # Send request
    headers = {
        'Content-Type': 'application/json',
        'Authorization': RP_API_KEY
    }
    response = requests.post(url, json=data, headers=headers)
    print(response)
    # Print response
    print("Status Code:", response.status_code)
    try:
        print("Response JSON:", response.json())
    except json.JSONDecodeError:
        print("Invalid JSON response:", response.text)

# Example usage
send_request("D:/projects/ocr-fastapi/example.jpg", "Extract the content from this image and convert it to latex?")




