#!/bin/bash

# Variables
DOCKER_IMAGE_NAME="stewiedocker46/web-app-flappy"
EXE_FILE_NAME="flappy_bird.exe"

# Build Docker image
echo "Building Docker image..."
docker build -t $DOCKER_IMAGE_NAME .

# Create executable with PyInstaller
echo "Building executable with PyInstaller..."
pyinstaller --onefile src/flappy_bird.py

# Move the executable to a known location
mv dist/flappy_bird.exe $EXE_FILE_NAME

# Push Docker image to Docker Hub
echo "Pushing Docker image to Docker Hub..."
docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD
docker push $DOCKER_IMAGE_NAME

# Upload executable to S3
echo "Uploading executable to S3..."
aws s3 cp $EXE_FILE_NAME s3://athena-bucket-oregon/$EXE_FILE_NAME
