# 🚀 FastAPI Microservice - Docker Image

This repository contains a FastAPI-based microservice packaged as a Docker image.  
Follow the instructions below to pull the image, run it locally, and test the endpoints.

---

## 🐳 Prerequisites
- Install [Docker](https://docs.docker.com/get-docker/) on your machine.
- Ensure Docker daemon is running.

---

## 📥 Pull the Docker Image
Replace `<your-dockerhub-username>` and `<image-name>` with your actual values.

```bash
# Pull the latest image
docker pull <your-dockerhub-username>/<image-name>:latest



# Run the container in detached mode
docker run -d -p 8000:8000 --name fastapi-ms <your-dockerhub-username>/<image-name>:latest
