# Deploy to Alternative Cloud Platforms (No gcloud required)

## 1. Railway.app (Easiest - No Configuration Needed)

### Steps:
1. Push your code to GitHub
2. Go to [Railway.app](https://railway.app)
3. Click "Start a New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway automatically detects the Dockerfile and deploys
6. Add environment variable `OPENAI_API_KEY` in Railway dashboard
7. Your app will be live at `https://yourapp.up.railway.app`

### Cost: 
- $5/month for the Hobby plan
- Includes 512MB RAM, shared CPU

---

## 2. Render.com (Great Free Tier)

### Steps:
1. Push code to GitHub
2. Go to [Render.com](https://render.com)
3. Click "New" → "Web Service"
4. Connect your GitHub repo
5. Configure:
   - **Build Command**: `docker build -t app .`
   - **Start Command**: `docker run -p 10000:8080 app`
   - **Environment**: Docker
6. Add environment variables in Render dashboard
7. Deploy automatically

### Cost:
- Free tier available (with limitations)
- $7/month for starter plan

---

## 3. DigitalOcean App Platform

### Steps:
1. Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
2. Click "Create App"
3. Connect your GitHub repository
4. DigitalOcean detects Dockerfile automatically
5. Configure resources and environment variables
6. Deploy with one click

### Cost:
- $5/month for basic plan

---

## 4. Heroku (Classic Choice)

### Steps:
1. Create account at [Heroku.com](https://heroku.com)
2. Install Heroku CLI or use Git deployment
3. Create new app in Heroku dashboard
4. Connect GitHub repository
5. Enable automatic deployments
6. Set environment variables in app settings

### Cost:
- $7/month per dyno (no free tier anymore)

---

## 5. Google Cloud Console Only (No CLI)

### Method 1: Cloud Shell in Browser
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click the terminal icon (Cloud Shell) - it's free!
3. Upload your project files using the upload button
4. Run these commands in Cloud Shell:
```bash
# Enable APIs
gcloud services enable cloudbuild.googleapis.com run.googleapis.com

# Build and deploy
gcloud builds submit --tag gcr.io/$GOOGLE_CLOUD_PROJECT/market-research-app
gcloud run deploy market-research-app \
  --image gcr.io/$GOOGLE_CLOUD_PROJECT/market-research-app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Method 2: Cloud Build + Manual Console Deploy
1. Go to [Cloud Build](https://console.cloud.google.com/cloud-build)
2. Click "Submit Build"
3. Upload your source code as ZIP
4. Use this build config:
```yaml
steps:
- name: 'gcr.io/cloud-builders/docker'
  args: ['build', '-t', 'gcr.io/$PROJECT_ID/market-research-app', '.']
- name: 'gcr.io/cloud-builders/docker'
  args: ['push', 'gcr.io/$PROJECT_ID/market-research-app']
```
5. After build completes, go to [Cloud Run](https://console.cloud.google.com/run)
6. Click "Create Service"
7. Select the built image
8. Configure and deploy

---

## 6. GitHub Actions (Automated)

Just push to GitHub and it deploys automatically! 
(Files already created: `.github/workflows/deploy.yml`)

### Setup:
1. Go to your GitHub repo settings
2. Add these secrets:
   - `GCP_PROJECT_ID`: Your Google Cloud project ID
   - `GCP_SA_KEY`: Service account JSON key
   - `OPENAI_API_KEY`: Your OpenAI API key
3. Push to main branch → automatic deployment!

---

## Recommended No-CLI Options:

### For Simplicity: **Railway.app**
- Zero configuration
- Just connect GitHub repo
- Automatic deployments
- Built-in monitoring

### For Free Tier: **Render.com**
- Good free tier
- Easy setup
- Dockerfile support

### For Google Cloud: **Cloud Shell**
- No local CLI installation
- Full Google Cloud features
- Free Cloud Shell environment
- Professional deployment pipeline

### Quick Comparison:

| Platform | Setup Time | Cost/Month | Auto Deploy | Custom Domain |
|----------|------------|------------|-------------|----------------|
| Railway  | 5 min      | $5         | ✅          | ✅            |
| Render   | 10 min     | Free/$7    | ✅          | ✅            |
| DigitalOcean | 10 min | $5         | ✅          | ✅            |
| Cloud Shell | 15 min  | Pay-as-use | ⚠️          | ✅            |
| GitHub Actions | 20 min | Pay-as-use | ✅       | ✅            |

All these options eliminate the need to install gcloud CLI locally!