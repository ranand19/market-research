#!/bin/bash

# Test script for Market Research App deployment
# Usage: ./test-deployment.sh [SERVICE_URL]

set -e

# Get service URL from argument or prompt
if [ $# -eq 0 ]; then
    echo "Enter your Cloud Run service URL:"
    read SERVICE_URL
else
    SERVICE_URL=$1
fi

# Remove trailing slash if present
SERVICE_URL=${SERVICE_URL%/}

echo "🧪 Testing Market Research App deployment at: $SERVICE_URL"

# Test 1: Health Check
echo "1. Testing health endpoint..."
if curl -f -s "$SERVICE_URL/health" | jq . > /dev/null 2>&1; then
    echo "   ✅ Health check passed"
    curl -s "$SERVICE_URL/health" | jq .
else
    echo "   ❌ Health check failed"
    exit 1
fi

echo ""

# Test 2: Research Types
echo "2. Testing research types endpoint..."
if curl -f -s "$SERVICE_URL/research/types" | jq . > /dev/null 2>&1; then
    echo "   ✅ Research types endpoint working"
    echo "   Available research types:"
    curl -s "$SERVICE_URL/research/types" | jq -r '.research_types[] | "   - \(.id): \(.name)"'
else
    echo "   ❌ Research types endpoint failed"
    exit 1
fi

echo ""

# Test 3: Tools List
echo "3. Testing tools list endpoint..."
if curl -f -s "$SERVICE_URL/tools/list" | jq . > /dev/null 2>&1; then
    echo "   ✅ Tools list endpoint working"
    echo "   Available tools:"
    curl -s "$SERVICE_URL/tools/list" | jq -r '.tools[] | "   - \(.name): \(.description)"'
else
    echo "   ❌ Tools list endpoint failed"
    exit 1
fi

echo ""

# Test 4: Simple Research Request
echo "4. Testing research execution..."
research_payload='{
    "query": "AI market trends",
    "research_type": "market_overview",
    "company_name": "Test Company"
}'

if curl -f -s -X POST "$SERVICE_URL/research/execute" \
    -H "Content-Type: application/json" \
    -d "$research_payload" | jq . > /dev/null 2>&1; then
    echo "   ✅ Research execution working"
    echo "   Sample research result:"
    curl -s -X POST "$SERVICE_URL/research/execute" \
        -H "Content-Type: application/json" \
        -d "$research_payload" | jq -r '.summary'
else
    echo "   ❌ Research execution failed"
    echo "   This might be due to missing OpenAI API key"
fi

echo ""

# Test 5: Frontend (if available)
echo "5. Testing frontend..."
if curl -f -s "$SERVICE_URL/" | grep -q "<!DOCTYPE html>" > /dev/null 2>&1; then
    echo "   ✅ Frontend is served correctly"
else
    echo "   ⚠️  Frontend may not be available (this is OK for API-only deployment)"
fi

echo ""
echo "🎉 Deployment test completed!"
echo ""
echo "Your app is available at:"
echo "🌐 Frontend: $SERVICE_URL"
echo "📊 Health Check: $SERVICE_URL/health"
echo "🔍 API Docs: $SERVICE_URL/docs"
echo ""
echo "To monitor your service:"
echo "📋 gcloud logs tail --service=market-research-app --region=us-central1"