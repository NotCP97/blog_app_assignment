FROM python:3.11-slim

WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

RUN apt-get update && apt-get install -y curl

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
