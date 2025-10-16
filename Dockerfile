# Use official Python 3.10 base image (works for Rasa)
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . /app

# Install system deps
RUN apt-get update && apt-get install -y build-essential git

# Upgrade pip + install requirements
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5005 for Rasa and 5055 for actions
EXPOSE 5005
EXPOSE 5055

# Train the model at build time
RUN rasa train

# Start both action server + rasa server
CMD ["bash", "-c", "rasa run actions --port 5055 & rasa run --enable-api --cors '*' --port 5005"]
