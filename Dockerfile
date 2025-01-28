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

# Command to run your Flask app
CMD ["python", "/agri/src/run.py"]
