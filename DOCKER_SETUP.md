# Docker Hub Setup Guide

This guide will walk you through setting up automated Docker image builds and pushes to Docker Hub using GitHub Actions.

## Prerequisites

1. A Docker Hub account
2. A GitHub repository for your project
3. Your project pushed to GitHub

## Step 1: Create Docker Hub Access Token

1. Go to [Docker Hub](https://hub.docker.com/)
2. Sign in to your account
3. Click on your username (top right) → **Account Settings**
4. Go to **Security** tab
5. Click **New Access Token**
6. Give it a name like "GitHub Actions"
7. Select **Read, Write, Delete** permissions
8. Click **Generate**
9. **Copy the token immediately** - you won't be able to see it again!

## Step 2: Add Secrets to GitHub Repository

1. Go to your GitHub repository
2. Click **Settings** tab
3. Go to **Secrets and variables** → **Actions**
4. Click **New repository secret**
5. Add these secrets:

   - **Name**: `DOCKERHUB_USERNAME`
   - **Value**: Your Docker Hub username

   - **Name**: `DOCKERHUB_TOKEN`
   - **Value**: The access token you created in Step 1

## Step 3: Update Repository Name

1. Edit `.github/workflows/docker-build-push.yml`
2. Update the `IMAGE_NAME` environment variable if needed:
   ```yaml
   env:
     REGISTRY: docker.io
     IMAGE_NAME: your-dockerhub-username/your-repo-name
   ```

## Step 4: Update Dependabot Configuration

1. Edit `.github/dependabot.yml`
2. Replace `your-username` with your GitHub username

## Step 5: Commit and Push

```bash
git add .
git commit -m "feat: add Docker Hub CI/CD pipeline with security scanning"
git push origin main
```

## Step 6: Verify the Workflow

1. Go to your GitHub repository
2. Click **Actions** tab
3. You should see the workflow running
4. After it completes successfully, check Docker Hub for your image

## Image Tags

The workflow automatically creates these tags:

- `latest` - Latest build from main branch
- `develop` - Builds from develop branch
- `v1.0.0` - Specific version tags (when you create Git tags)
- `main` - Branch name tags

## Security Features

✅ **Multi-platform builds** (AMD64 + ARM64)  
✅ **Vulnerability scanning** with Trivy  
✅ **Build attestations** for supply chain security  
✅ **Non-root user** in Docker container  
✅ **Minimal attack surface** with slim base image  
✅ **Automated dependency updates** with Dependabot

## Using in Kubernetes

Once your image is on Docker Hub, you can use it in your K3s cluster:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prism-api
  namespace: default
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
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 512Mi
          livenessProbe:
            httpGet:
              path: /
              port: 80
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /
              port: 80
            initialDelaySeconds: 5
            periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: prism-api-service
spec:
  selector:
    app: prism-api
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: ClusterIP
```

## Troubleshooting

### Build Failed

- Check that your Docker Hub credentials are correct
- Verify the repository name matches your Docker Hub repository
- Check the build logs in GitHub Actions

### Image Not Found

- Make sure the repository exists on Docker Hub
- Check that the workflow completed successfully
- Verify the image name and tag

### Permission Denied

- Ensure your Docker Hub token has write permissions
- Check that the token hasn't expired

## Next Steps

1. Set up monitoring for your application
2. Add integration tests to the CI pipeline
3. Configure deployment automation to your K3s cluster
4. Set up log aggregation and monitoring
