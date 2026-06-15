# Use official lightweight Python runtime
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download the spaCy NLP model inside the container
RUN python -m spacy download en_core_web_sm

# Copy the rest of the application code
COPY . .

# Expose the API port
EXPOSE 8000

# Command to boot the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
