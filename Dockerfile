FROM python:3.10

WORKDIR /app
COPY requirements.txt .
# Install dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install torch transformers huggingface_hub pillow runpod python-dotenv
RUN pip install -r requirements.txt
# Define environment variables
ENV MODEL_PATH="/app/model"

# Download the model during the build process
RUN mkdir -p $MODEL_PATH && \
    python -c "from transformers import AutoModel, AutoTokenizer, AutoProcessor; \
               model_name='openbmb/MiniCPM-V-2_6-int4'; \
               AutoModel.from_pretrained(model_name, trust_remote_code=True).save_pretrained('$MODEL_PATH'); \
               AutoTokenizer.from_pretrained(model_name, trust_remote_code=True).save_pretrained('$MODEL_PATH'); \
               AutoProcessor.from_pretrained(model_name, trust_remote_code=True).save_pretrained('$MODEL_PATH')"

# Copy project files
COPY . /app

# Run the serverless handler
CMD ["python", "server.py"]
