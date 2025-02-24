FROM python:3.10

WORKDIR /app
COPY requirements.txt .
# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app

# Run the serverless handler
CMD ["python3","-u", "/app/server.py"]