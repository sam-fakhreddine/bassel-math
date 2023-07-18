# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app
# Install openssl
RUN apt-get update && apt-get install -y openssl

# Generate a self-signed certificate
RUN openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj '/CN=www.bassel.lol'

# Install dependencies from requirements.txt
RUN pip install -r requirements.txt

# Install Gunicorn
RUN pip install gunicorn

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME World

# Run Gunicorn when the container launches
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--log-level", "debug", "app:app"]
