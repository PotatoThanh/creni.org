# Dockerfile for Python 3.9
FROM python:3.9-slim-bullseye

# Working_dir
WORKDIR /app

# Set up Python environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code to dockerfile:
COPY main.py .
# COPY src .
