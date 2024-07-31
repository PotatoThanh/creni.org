# Dockerfile for Python 3.9
FROM python:3.9-slim-bullseye

# Working_dir
WORKDIR /app

# Install dependencies:
RUN apt-get update
RUN apt-get install -y python3-opencv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code to dockerfile:
COPY main.py .
# COPY src .

CMD [ "python", "main.py" ] 
