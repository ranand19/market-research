# Deploy Market Research App to Google Cloud Run

This guide walks you through deploying your Market Research App to Google Cloud Run. The app includes a FastAPI backend with LangChain agents and a React frontend.

## Prerequisites

1. **Google Cloud Account** with billing enabled
2. **Google Cloud CLI** installed and configured
3. **Docker** installed and running
4. **OpenAI API Key** from [OpenAI Platform](https://platform.openai.com/api-keys)

## Quick Start

### 1. Install Google Cloud CLI

```bash
# macOS
brew install google-cloud-sdk

# Or download from: https://cloud.google.com/sdk/docs/install
```

### 2. Authenticate and Setup

```bash
# Login to Google Cloud
gcloud auth login

# Set your project ID (replace with your actual project ID)
export GOOGLE_CLOUD_PROJECT="your-project-id"
gcloud config set project $GOOGLE_CLOUD_PROJECT

# Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### 3. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your actual values
# - Set your OpenAI API key
# - Set your Google Cloud project ID
```

### 4. Deploy with One Command

```bash
# Run the deployment script
./deploy.sh
```

That's it! Your app will be built and deployed to Cloud Run.

## Manual Deployment (Step by Step)

### 1. Build the Docker Image

```bash
# Build with Cloud Build (recommended)
gcloud builds submit --tag gcr.io/$GOOGLE_CLOUD_PROJECT/market-research-app .

# Or build locally and push
docker build -t gcr.io/$GOOGLE_CLOUD_PROJECT/market-research-app .
docker push gcr.io/$GOOGLE_CLOUD_PROJECT/market-research-app
```

### 2. Deploy to Cloud Run

```bash
gcloud run deploy market-research-app \
    --image gcr.io/$GOOGLE_CLOUD_PROJECT/market-research-app \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 2 \
    --timeout 300 \
    --concurrency 80 \
    --max-instances 10 \
    --set-env-vars="LLM_MODEL=gpt-4,LLM_TEMPERATURE=0.7,LLM_MAX_TOKENS=2000" \
    --port 8080
```

### 3. Secure Your OpenAI API Key

Instead of setting environment variables directly, use Google Secret Manager:

```bash
# Create a secret
echo -n "your-openai-api-key" | gcloud secrets create openai-api-key --data-file=-

# Update the service to use the secret
gcloud run services update market-research-app \
    --region=us-central1 \
    --update-secrets="OPENAI_API_KEY=openai-api-key:latest"
```

## Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key (required) | - |
| `LLM_MODEL` | OpenAI model to use | `gpt-4` |
| `LLM_TEMPERATURE` | Model temperature | `0.7` |
| `LLM_MAX_TOKENS` | Max tokens per request | `2000` |
| `PORT` | Server port | `8080` |

### Resource Limits

- **Memory**: 2Gi (adjustable based on needs)
- **CPU**: 2 vCPUs (adjustable)
- **Timeout**: 300 seconds
- **Concurrency**: 80 requests per instance
- **Max Instances**: 10 (auto-scaling)

## Monitoring and Maintenance

### View Logs

```bash
# Real-time logs
gcloud logs tail --service=market-research-app --region=us-central1

# Historical logs
gcloud logs read --service=market-research-app --region=us-central1 --limit=100
```

### Update the Service

```bash
# Build new image
gcloud builds submit --tag gcr.io/$GOOGLE_CLOUD_PROJECT/market-research-app .

# Deploy update (Cloud Run will automatically use the new image)
gcloud run deploy market-research-app \
    --image gcr.io/$GOOGLE_CLOUD_PROJECT/market-research-app \
    --region us-central1
```

### Health Checks

- Health endpoint: `https://your-service-url/health`
- Research types: `https://your-service-url/research/types`
- Available tools: `https://your-service-url/tools/list`

## Custom Domain (Optional)

### 1. Verify Domain Ownership

```bash
gcloud domains verify yourdomain.com
```

### 2. Create Domain Mapping

```bash
gcloud run domain-mappings create \
    --service market-research-app \
    --domain yourdomain.com \
    --region us-central1
```

### 3. Configure DNS

Add the DNS records shown in the output to your domain provider.

## Troubleshooting

### Common Issues

1. **Build Fails**
   - Check Docker is running
   - Ensure all files are present
   - Check build logs: `gcloud builds log [BUILD_ID]`

2. **Deployment Fails**
   - Check project permissions
   - Verify APIs are enabled
   - Check resource quotas

3. **Service Errors**
   - Check logs: `gcloud logs read --service=market-research-app`
   - Verify environment variables
   - Test health endpoint

### Performance Optimization

1. **Cold Starts**: Use minimum instances
   ```bash
   gcloud run services update market-research-app \
       --region=us-central1 \
       --min-instances=1
   ```

2. **Memory Optimization**: Adjust based on usage
   ```bash
   gcloud run services update market-research-app \
       --region=us-central1 \
       --memory=4Gi
   ```

## Security Best Practices

1. **Use Secret Manager** for API keys
2. **Enable IAM** for sensitive endpoints
3. **Use HTTPS** (enabled by default)
4. **Regular Updates** for dependencies
5. **Monitor Access Logs** for unusual activity

## Cost Optimization

- Use **minimum instances** only if needed
- Set appropriate **CPU and memory** limits
- Monitor usage with **Cloud Monitoring**
- Use **request-based pricing** advantage

## Next Steps

1. Set up monitoring and alerting
2. Configure custom domain
3. Add authentication for admin features
4. Set up CI/CD pipeline
5. Add database for persistent storage

For more information, see the [Google Cloud Run documentation](https://cloud.google.com/run/docs).