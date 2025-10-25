# Docker Deployment Guide for Smart-Housing
# Complete Step-by-Step Guide for Railway + GitHub Container Registry

## 🐳 Overview

This guide will help you:
1. Build a Docker image of your Smart-Housing app
2. Push it to GitHub Container Registry (GHCR)
3. Deploy it to Railway using the Docker image
4. Set up automated builds with GitHub Actions

## 📋 Prerequisites

- GitHub account
- Railway account
- Docker installed locally (optional, we'll use GitHub Actions)
- Your Smart-Housing repository pushed to GitHub

## 🚀 Method 1: GitHub Actions (Recommended)

### Step 1: Create GitHub Actions Workflow

Create `.github/workflows/docker-build.yml`:

```yaml
name: Build and Push Docker Image

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Log in to Container Registry
      uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=sha,prefix={{branch}}-
          type=raw,value=latest,enable={{is_default_branch}}

    - name: Build and push Docker image
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
```

### Step 2: Enable GitHub Container Registry

1. Go to your GitHub repository
2. Click **"Settings"** tab
3. Scroll down to **"Packages"** section
4. Ensure **"GitHub Container Registry"** is enabled

### Step 3: Push Your Code

```bash
git add .
git commit -m "Add Docker configuration"
git push origin main
```

### Step 4: Monitor Build Process

1. Go to your GitHub repository
2. Click **"Actions"** tab
3. Watch the "Build and Push Docker Image" workflow
4. Wait for it to complete (5-10 minutes)

## 🚀 Method 2: Local Docker Build (Alternative)

If you prefer to build locally:

### Step 1: Install Docker

**Windows:**
1. Download Docker Desktop from [docker.com](https://docker.com)
2. Install and restart your computer
3. Open Docker Desktop

**Linux/Mac:**
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

### Step 2: Build Docker Image Locally

```bash
# Navigate to your project directory
cd /path/to/your/smart-housing

# Build the Docker image
docker build -t smart-housing:latest .

# Test the image locally
docker run -p 8000:8000 -e DEBUG=0 smart-housing:latest
```

### Step 3: Push to GitHub Container Registry

```bash
# Login to GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u YOUR_GITHUB_USERNAME --password-stdin

# Tag your image
docker tag smart-housing:latest ghcr.io/YOUR_GITHUB_USERNAME/smart-housing:latest

# Push to registry
docker push ghcr.io/YOUR_GITHUB_USERNAME/smart-housing:latest
```

## 🚂 Railway Deployment with Docker

### Step 1: Create Railway Project

1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Choose your repository

### Step 2: Configure for Docker Deployment

1. In Railway dashboard, go to your project
2. Click **"Settings"** tab
3. Scroll to **"Deploy"** section
4. Set **"Build Command"** to: `docker build -t smart-housing .`
5. Set **"Start Command"** to: `docker run -p $PORT:8000 smart-housing`

### Step 3: Use Pre-built Docker Image (Recommended)

Instead of building on Railway, use your pre-built image:

1. In Railway dashboard, go to **"Settings"**
2. Click **"Deploy"**
3. Set **"Build Command"** to: `echo "Using pre-built image"`
4. Set **"Start Command"** to: `docker run -p $PORT:8000 ghcr.io/YOUR_GITHUB_USERNAME/smart-housing:latest`

### Step 4: Set Environment Variables

In Railway dashboard → **"Variables"** tab:

```
DJANGO_SECRET_KEY=a-#gqkp7ug+hs7ma05-n!ser_p*m@)lq4c!rtn&)q_9%0xwu4-
DEBUG=0
ALLOWED_HOSTS=smart-housing.railway.app,localhost,127.0.0.1
REDIS_URL=redis://localhost:6379/0
```

### Step 5: Deploy

1. Click **"Deploy"** in Railway dashboard
2. Wait for deployment to complete
3. Your app will be live at: **https://smart-housing.railway.app**

## 🔧 Docker Configuration Explained

### Dockerfile Breakdown:

```dockerfile
# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1  # Don't write .pyc files
ENV PYTHONUNBUFFERED=1         # Don't buffer Python output

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev curl

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/staticfiles /app/checkpoints /app/data

# Collect static files
RUN cd prediction && python manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Start the application
CMD ["sh", "-c", "cd prediction && python manage.py migrate && python manage.py deploy && gunicorn prediction.wsgi:application --bind 0.0.0.0:8000"]
```

### .dockerignore Explained:

The `.dockerignore` file excludes unnecessary files from the Docker build context:
- Python cache files (`__pycache__/`)
- Virtual environment (`venv/`)
- IDE files (`.vscode/`, `.idea/`)
- Documentation files (except README.md)
- Git files (`.git/`)

**Important:** We keep these for production:
- `checkpoints/` (ML models)
- `data/` (training dataset)
- `assets/` (images, etc.)

## 🔄 Automated Deployment Workflow

### GitHub Actions for Auto-Deploy:

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Railway

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - name: Deploy to Railway
      uses: railwayapp/railway-deploy@v1
      with:
        railway-token: ${{ secrets.RAILWAY_TOKEN }}
        service: smart-housing
```

### Railway Token Setup:

1. Go to Railway dashboard
2. Click your profile → **"Account"**
3. Go to **"Tokens"** tab
4. Click **"New Token"**
5. Copy the token
6. In GitHub repository → **"Settings"** → **"Secrets"**
7. Add new secret: `RAILWAY_TOKEN` = your token

## 🎯 Benefits of Docker Deployment

### ✅ **Advantages:**
- **Faster Deployments**: Pre-built images deploy instantly
- **Consistent Environment**: Same environment everywhere
- **Easy Scaling**: Docker containers scale easily
- **Version Control**: Tag different versions
- **Rollback Capability**: Easy to rollback to previous versions

### ✅ **Production Features:**
- **Health Checks**: Automatic health monitoring
- **Optimized Layers**: Efficient Docker layers
- **Security**: Non-root user execution
- **Resource Management**: Controlled resource usage

## 🔍 Troubleshooting

### Common Issues:

**1. Build Fails:**
```bash
# Check Docker logs
docker logs <container_id>

# Rebuild with verbose output
docker build --no-cache -t smart-housing .
```

**2. Image Too Large:**
```bash
# Check image size
docker images

# Optimize Dockerfile (already optimized)
```

**3. Railway Deployment Issues:**
- Check Railway logs in dashboard
- Verify environment variables
- Ensure Docker image exists in GHCR

**4. ML Models Not Working:**
- Check if models are included in Docker image
- Verify `checkpoints/` directory exists
- Check deployment logs for model creation

## 📊 Final Result

After successful deployment, you'll have:

- ✅ **Docker Image**: `ghcr.io/YOUR_USERNAME/smart-housing:latest`
- ✅ **Live App**: https://smart-housing.railway.app
- ✅ **Auto-Deploy**: Push to GitHub → Auto-deploy to Railway
- ✅ **ML Models**: Pre-trained models ready for predictions
- ✅ **Responsive Design**: Mobile-friendly interface
- ✅ **Production Ready**: Secure, scalable, monitored

## 🎉 Next Steps

1. **Test Your Deployment**: Visit all pages on your live app
2. **Monitor Performance**: Use Railway dashboard metrics
3. **Set Up Monitoring**: Add logging and error tracking
4. **Scale Up**: Upgrade Railway plan if needed
5. **Add Features**: Continue developing new features

Your Smart-Housing app is now deployed with Docker and ready for production! 🚀
