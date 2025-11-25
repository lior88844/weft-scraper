#!/bin/bash
# Deploy Weft MCP Server to Google Cloud Run
# Usage: ./deploy-to-gcp.sh <PROJECT_ID>

set -e  # Exit on error

# Check if project ID provided
if [ -z "$1" ]; then
    echo "❌ Please provide your GCP project ID"
    echo "Usage: ./deploy-to-gcp.sh <PROJECT_ID>"
    echo ""
    echo "Find your project ID at: https://console.cloud.google.com"
    exit 1
fi

PROJECT_ID="$1"
SERVICE_NAME="weft-mcp-server"
REGION="us-central1"

echo "🚀 Deploying Weft MCP Server to Google Cloud Run"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Project ID: $PROJECT_ID"
echo "Service: $SERVICE_NAME"
echo "Region: $REGION"
echo ""

# Set project
echo "📋 Setting active project..."
gcloud config set project "$PROJECT_ID"

# Enable required APIs
echo "🔧 Enabling required APIs (this may take a minute)..."
gcloud services enable run.googleapis.com --quiet
gcloud services enable cloudbuild.googleapis.com --quiet
gcloud services enable containerregistry.googleapis.com --quiet

echo "✅ APIs enabled"
echo ""

# Set region
echo "🌍 Setting default region..."
gcloud config set run/region "$REGION"

echo ""
echo "🏗️  Building and deploying (this will take 2-3 minutes)..."
echo ""

# Deploy from source
cd "$(dirname "$0")"
gcloud run deploy "$SERVICE_NAME" \
  --source mcp-server \
  --platform managed \
  --region "$REGION" \
  --allow-unauthenticated \
  --port 8080 \
  --memory 512Mi \
  --cpu 1 \
  --timeout 60s \
  --max-instances 10 \
  --quiet

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Deployment Complete!"
echo ""

# Get service URL
SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" \
  --region "$REGION" \
  --format='value(status.url)')

echo "🎉 Your MCP server is live!"
echo ""
echo "Service URL: $SERVICE_URL"
echo "MCP Endpoint: $SERVICE_URL/mcp"
echo ""
echo "📊 View logs:"
echo "   gcloud run logs tail $SERVICE_NAME --region $REGION"
echo ""
echo "🔄 To update your deployment later, just run this script again!"

