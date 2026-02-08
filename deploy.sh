#!/bin/bash

# Market Research App - Google Cloud Run Deployment Script
# This script builds and deploys the application to Google Cloud Run

set -e  # Exit on any error

# Configuration
PROJECT_ID=${GOOGLE_CLOUD_PROJECT:-"your-project-id"}
SERVICE_NAME="market-research-app"
REGION=${GOOGLE_CLOUD_REGION:-"us-central1"}
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "🚀 Deploying Market Research App to Google Cloud Run"
echo "Project ID: $PROJECT_ID"
echo "Service Name: $SERVICE_NAME"
echo "Region: $REGION"
echo "Image: $IMAGE_NAME"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Error: gcloud CLI is not installed. Please install it first."
    echo "Visit: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if docker is running
if ! docker info &> /dev/null; then
    echo "❌ Error: Docker is not running. Please start Docker first."
    exit 1
fi

# Authenticate with Google Cloud (if not already authenticated)
echo "🔑 Checking Google Cloud authentication..."
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q "."; then
    echo "Please authenticate with Google Cloud:"
    gcloud auth login
fi

# Set project (if PROJECT_ID is provided)
if [ "$PROJECT_ID" != "your-project-id" ]; then
    gcloud config set project $PROJECT_ID
fi

# Enable required APIs
echo "🔧 Enabling required Google Cloud APIs..."
gcloud services enable cloudbuild.googleapis.com --quiet
gcloud services enable run.googleapis.com --quiet
gcloud services enable containerregistry.googleapis.com --quiet

# Build the Docker image using Cloud Build
echo "🏗️  Building Docker image with Cloud Build..."
gcloud builds submit --tag $IMAGE_NAME .

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 2 \
    --timeout 300 \
    --concurrency 80 \
    --max-instances 10 \
    --set-env-vars="LLM_MODEL=gpt-4,LLM_TEMPERATURE=0.7,LLM_MAX_TOKENS=2000" \
    --port 8080

# Get the service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format='value(status.url)')

echo "✅ Deployment completed successfully!"
echo "🌐 Service URL: $SERVICE_URL"
echo "📋 Health check: $SERVICE_URL/health"
echo "🔧 Manage service: https://console.cloud.google.com/run/detail/$REGION/$SERVICE_NAME/metrics?project=$PROJECT_ID"

# Test the health endpoint
echo "🩺 Testing health endpoint..."
if curl -f "$SERVICE_URL/health" > /dev/null 2>&1; then
    echo "✅ Health check passed!"
else
    echo "⚠️  Health check failed. Check the logs:"
    echo "gcloud logs read --service=$SERVICE_NAME --region=$REGION"
fi

echo ""
echo "🎉 Your Market Research App is now live at: $SERVICE_URL"
echo ""
echo "Next steps:"
echo "1. Set up your OpenAI API key as a secret:"
echo "   gcloud secrets create openai-api-key --data-file=<(echo -n 'your-api-key')"
echo "   gcloud run services update $SERVICE_NAME --region=$REGION --set-secrets=/app/.env=openai-api-key:latest"
echo ""
echo "2. Set up a custom domain (optional):"
echo "   gcloud run domain-mappings create --service=$SERVICE_NAME --domain=yourdomain.com --region=$REGION"
echo ""
echo "3. Monitor your service:"
echo "   gcloud logs tail --service=$SERVICE_NAME --region=$REGION"