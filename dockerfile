# Use the official Python image as a base image
FROM python:3.11-slim

# Set environment variables to prevent Python from buffering outputs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt .

# Copy config into the container
COPY config.json .

# Update and install psycopg bin
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script into the container
COPY . .

# Set the command to run the Python script
CMD ["python", "main.py"]
