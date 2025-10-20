# Prism API

My FastAPI for my Kubernetes cluster.

## 🐳 Docker

This application is containerized and automatically built and pushed to Docker Hub via GitHub Actions.

### Local Development

```bash
# Build the image locally
docker build -t prism-api .

# Run the container
docker run -p 8000:80 prism-api
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prism-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: prism-api
  template:
    metadata:
      labels:
        app: prism-api
    spec:
      containers:
        - name: prism-api
          image: your-dockerhub-username/k3s-api:latest
          ports:
            - containerPort: 80
```

## 🚀 Development

This project uses [uv](https://docs.astral.sh/uv/) for fast Python package management.

```bash
# Install dependencies
uv sync

# Run development server
uv run fastapi dev app/main.py

# Run with hot reload
uv run fastapi dev app/main.py --reload
```
