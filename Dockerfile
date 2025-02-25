FROM python:3.10

WORKDIR /app
COPY requirements.txt /app

# Copy the model folder
COPY model /app/model

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY server.py /app/server.py
COPY test_input.json /app/test_input.json

# Run the serverless handler
CMD ["python3","-u", "/app/server.py"]