# Deploy to Google Cloud Run via Web Console

## Method 1: Direct Console Deployment

### Step 1: Build and Push Docker Image Manually

You can build locally and push to Google Container Registry:

```bash
# Build the image locally
docker build -t gcr.io/reasoning-eng/market-research-app .

# Configure Docker to use gcloud as credential helper (one-time setup)
# Alternative: Use Docker Desktop with Google Cloud integration
docker tag gcr.io/reasoning-eng/market-research-app gcr.io/YOUR-PROJECT-ID/market-research-app:latest
```

### Step 2: Push via Docker Desktop or Alternative Tools

**Option A: Docker Desktop with Google Cloud**
1. Install Google Cloud extension for Docker Desktop
2. Configure authentication through Docker Desktop
3. Push directly: `docker push gcr.io/YOUR-PROJECT-ID/market-research-app`

**Option B: Use Google Cloud Console Cloud Shell**
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Open Cloud Shell (terminal icon in top right)
3. Upload your project files using the upload button
4. Run build commands in Cloud Shell

### Step 3: Deploy via Web Console

1. Go to [Cloud Run Console](https://console.cloud.google.com/run)
2. Click "Create Service"
3. Choose "Deploy one revision from an existing container image"
4. Select your image: `gcr.io/YOUR-PROJECT-ID/market-research-app`
5. Configure:
   - Service name: `market-research-app`
   - Region: `us-central1`
   - CPU allocation: `1 CPU`
   - Memory: `2Gi`
   - Port: `8080`
   - Maximum requests per container: `80`
   - Maximum instances: `10`
6. Under "Environment Variables" add:
   - `LLM_MODEL`: `gpt-4`
   - `LLM_TEMPERATURE`: `0.7`
   - `LLM_MAX_TOKENS`: `2000`
7. Under "Security" → "Authentication": Allow unauthenticated invocations
8. Click "Create"

## Method 2: GitHub Actions (Automated CI/CD)

Create `.github/workflows/deploy.yml` in your repository:

```yaml
name: Deploy to Cloud Run

on:
  push:
    branches: [ main ]

env:
  PROJECT_ID: ${{ secrets.GCP_PROJECT_ID }}
  SERVICE_NAME: market-research-app
  REGION: us-central1

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Setup Google Cloud CLI
      uses: google-github-actions/setup-gcloud@v1
      with:
        service_account_key: ${{ secrets.GCP_SA_KEY }}
        project_id: ${{ secrets.GCP_PROJECT_ID }}
    
    - name: Configure Docker
      run: gcloud auth configure-docker
    
    - name: Build and Push Docker image
      run: |
        docker build -t gcr.io/$PROJECT_ID/$SERVICE_NAME .
        docker push gcr.io/$PROJECT_ID/$SERVICE_NAME
    
    - name: Deploy to Cloud Run
      run: |
        gcloud run deploy $SERVICE_NAME \
          --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
          --platform managed \
          --region $REGION \
          --allow-unauthenticated \
          --memory 2Gi \
          --cpu 2 \
          --set-env-vars="LLM_MODEL=gpt-4,LLM_TEMPERATURE=0.7,LLM_MAX_TOKENS=2000"
```

## Method 3: Cloud Build Trigger (Git-based)

1. Go to [Cloud Build Console](https://console.cloud.google.com/cloud-build/triggers)
2. Click "Create Trigger"
3. Connect your GitHub/GitLab repository
4. Configure:
   - Name: `deploy-market-research-app`
   - Event: Push to branch `main`
   - Configuration: Cloud Build configuration file
   - Cloud Build configuration file location: `cloudbuild.yaml`

Create `cloudbuild.yaml`:

```yaml
steps:
  # Build the container image
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/market-research-app', '.']
  
  # Push the container image
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/market-research-app']
  
  # Deploy to Cloud Run
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
    - 'run'
    - 'deploy'
    - 'market-research-app'
    - '--image'
    - 'gcr.io/$PROJECT_ID/market-research-app'
    - '--region'
    - 'us-central1'
    - '--platform'
    - 'managed'
    - '--allow-unauthenticated'
    - '--memory'
    - '2Gi'
    - '--cpu'
    - '2'
    - '--set-env-vars'
    - 'LLM_MODEL=gpt-4,LLM_TEMPERATURE=0.7,LLM_MAX_TOKENS=2000'

images:
  - 'gcr.io/$PROJECT_ID/market-research-app'
```

## Method 4: VS Code Extension

1. Install "Cloud Code" extension for VS Code
2. Sign in to Google Cloud
3. Right-click on your `Dockerfile`
4. Select "Deploy to Cloud Run"
5. Follow the guided setup

## Method 5: Alternative Cloud Platforms

### Deploy to Railway (Simplified)
1. Connect your GitHub repo to [Railway](https://railway.app)
2. Railway auto-detects Dockerfile
3. Set environment variables in dashboard
4. Deploy with one click

### Deploy to Render
1. Connect repo to [Render](https://render.com)
2. Choose "Web Service"
3. Render detects Dockerfile automatically
4. Configure environment variables
5. Deploy

### Deploy to Heroku Container Registry
```bash
# Install Heroku CLI
heroku login
heroku create market-research-app
heroku container:login
heroku container:push web -a market-research-app
heroku container:release web -a market-research-app
```

## Recommended Approach for No-CLI Setup:

**Use Google Cloud Console + Cloud Shell:**
1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Open Cloud Shell (free, browser-based terminal)
3. Upload your project files
4. Run the deploy.sh script in Cloud Shell
5. Manage everything through the web interface

This gives you the power of CLI tools without installing anything locally!