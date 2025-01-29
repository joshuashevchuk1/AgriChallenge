# Use an official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /agri

# Copy everything from the current directory (including subfolders like 'src') into the container's working directory
COPY . .

# Set the PYTHONPATH environment variable to include the 'src' directory
ENV PYTHONPATH=/agri/src:$PYTHONPATH

# Install Python dependencies from the requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask application port
EXPOSE 9020
# Use the official MongoDB image from Docker Hub
FROM mongo:latest

# Expose the default MongoDB port (27017)
EXPOSE 27017

# Define a volume to persist data (recommended)
VOLUME /data/db

# Start the MongoDB server
CMD ["mongod"]
# Command to run your Flask api
CMD ["python", "/agri/src/run.py"]
