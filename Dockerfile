# Use the official MongoDB image from Docker Hub
FROM mongo:latest

# Expose the default MongoDB port (27017)
EXPOSE 27017

# Define a volume to persist data (recommended)
VOLUME /data/db

# Start the MongoDB server
CMD ["mongod"]