#!/bin/bash

# Exit script on any error
set -e

# Check if version is passed as a parameter
if [ -z "$1" ]; then
  echo "Usage: ./deploy.sh <VERSION>"
  exit 1
fi

VERSION=$1
GCP_PATH=$2

# Step 1: Build Docker image
echo "Building Docker image with version $VERSION..."
docker build . -t portfolio-tracker:$VERSION --platform linux/amd64

# Step 2: Tag the Docker image for GCP
echo "Tagging Docker image for GCP..."
GCP_IMAGE="$GCP_PATH/portfolio-tracker/portfolio-tracker:$VERSION"
docker tag portfolio-tracker:$VERSION $GCP_IMAGE

# Step 3: Push the Docker image to GCP
echo "Pushing Docker image to GCP..."
docker push $GCP_IMAGE

echo "Deployment complete! Image $GCP_IMAGE has been pushed successfully."
