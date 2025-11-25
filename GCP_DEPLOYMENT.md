# Deploying Weft MCP Server to Google Cloud Platform (Cloud Run)

This guide will help you deploy your Weft MCP server to Google Cloud Run.

## Prerequisites

1. **Google Cloud Account**: [Create one here](https://cloud.google.com/free) (includes $300 free credit)
2. **Google Cloud CLI**: Install the `gcloud` command-line tool

### Install Google Cloud CLI

**macOS:**
```bash
brew install google-cloud-sdk
```

**Linux:**
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

**Windows:**
Download from: https://cloud.google.com/sdk/docs/install

## Initial Setup (One-Time)

### 1. Authenticate with Google Cloud
```bash
gcloud auth login
```

### 2. Create a New Project (or use existing)
```bash
# Create new project
gcloud projects create weft-mcp-server --name="Weft MCP Server"

# Set as active project
gcloud config set project weft-mcp-server
```

### 3. Enable Required APIs
```bash
# Enable Cloud Run API
gcloud services enable run.googleapis.com

# Enable Container Registry API
gcloud services enable containerregistry.googleapis.com

# Enable Cloud Build API (for building containers)
gcloud services enable cloudbuild.googleapis.com
```

### 4. Set Default Region (Optional)
```bash
# Choose a region close to you or your users
# Common options: us-central1, us-east1, europe-west1, asia-northeast1
gcloud config set run/region us-central1
```

## Deploying Your MCP Server

### Method 1: Deploy Directly (Recommended - Simplest)

From your project root directory:

```bash
cd /Users/lior/Documents/Development/Weft

# Deploy using Cloud Build
gcloud run deploy weft-mcp-server \
  --source mcp-server \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 512Mi \
  --cpu 1 \
  --timeout 60s \
  --max-instances 10
```

**What this does:**
- Automatically builds a container from your `mcp-server/` directory
- Deploys to Cloud Run
- Makes it publicly accessible
- Sets resource limits
- Auto-scales from 0 to 10 instances

### Method 2: Build and Deploy with Dockerfile

```bash
cd /Users/lior/Documents/Development/Weft/mcp-server

# Build the container
gcloud builds submit --tag gcr.io/weft-mcp-server/mcp-server

# Deploy the container
gcloud run deploy weft-mcp-server \
  --image gcr.io/weft-mcp-server/mcp-server \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 512Mi \
  --cpu 1
```

## After Deployment

After successful deployment, you'll see output like:

```
Service [weft-mcp-server] revision [weft-mcp-server-00001-abc] has been deployed and is serving 100 percent of traffic.
Service URL: https://weft-mcp-server-xxxxxxxxxx-uc.a.run.app
```

**Your MCP endpoint will be:**
```
https://weft-mcp-server-xxxxxxxxxx-uc.a.run.app/mcp
```

## Updating Your Deployment

Whenever you update your code or data:

```bash
cd /Users/lior/Documents/Development/Weft

# Redeploy (same command as initial deploy)
gcloud run deploy weft-mcp-server \
  --source mcp-server \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

Cloud Run will automatically:
- Build a new container
- Deploy with zero downtime
- Rollback if the deployment fails

## Viewing Logs

```bash
# Stream logs in real-time
gcloud run logs tail weft-mcp-server --region us-central1

# View logs in Cloud Console
gcloud run services describe weft-mcp-server --region us-central1
```

## Configuration Options

### Environment Variables

If you need to set environment variables:

```bash
gcloud run deploy weft-mcp-server \
  --source mcp-server \
  --set-env-vars "STORE_NAME=nitzat-haduvdevan,DEBUG=false"
```

### Custom Domain

To use your own domain (e.g., `mcp.yourdomain.com`):

```bash
# Map custom domain
gcloud run domain-mappings create \
  --service weft-mcp-server \
  --domain mcp.yourdomain.com \
  --region us-central1
```

Then add the DNS records shown in the output to your domain registrar.

### Resource Limits

Adjust CPU and memory based on usage:

```bash
gcloud run deploy weft-mcp-server \
  --source mcp-server \
  --memory 1Gi \
  --cpu 2 \
  --max-instances 20
```

## Cost Estimates

Cloud Run pricing (as of 2024):
- **First 2 million requests/month**: FREE
- **CPU**: $0.00002400 per vCPU-second
- **Memory**: $0.00000250 per GiB-second
- **Requests**: $0.40 per million requests

**Example monthly cost** (light usage):
- 100,000 requests/month
- Average 500ms request time
- 512MB memory
- **Cost: ~$1-2/month** (likely FREE with free tier)

## Useful Commands

### Check Service Status
```bash
gcloud run services describe weft-mcp-server --region us-central1
```

### List All Services
```bash
gcloud run services list
```

### Delete Service
```bash
gcloud run services delete weft-mcp-server --region us-central1
```

### View Service URL
```bash
gcloud run services describe weft-mcp-server --region us-central1 --format='value(status.url)'
```

## Troubleshooting

### Build Fails
- Check that `mcp-server/requirements.txt` exists
- Ensure `mcp-server/server.py` exists
- Check logs: `gcloud builds log --region=us-central1`

### Service Won't Start
- Check logs: `gcloud run logs tail weft-mcp-server --region us-central1`
- Ensure the server binds to `0.0.0.0:8080`
- Verify PORT environment variable is being read correctly

### 403 Forbidden
- Make sure `--allow-unauthenticated` was set
- Check IAM permissions

## Connecting to ChatGPT

Once deployed, use your Cloud Run URL in ChatGPT's MCP integration:

```
Endpoint: https://weft-mcp-server-xxxxxxxxxx-uc.a.run.app/mcp
```

## Next Steps

1. ✅ Deploy to Cloud Run (follow steps above)
2. ✅ Test the MCP endpoint
3. ✅ Connect to ChatGPT
4. ✅ Monitor usage in [GCP Console](https://console.cloud.google.com/run)

## Benefits vs Railway

✅ **Generous Free Tier**: 2M requests/month free
✅ **Better Scaling**: Auto-scales to zero (no cost when idle)
✅ **Global CDN**: Built-in
✅ **HTTPS**: Automatic SSL certificates
✅ **High Availability**: 99.95% uptime SLA
✅ **Simple Deployment**: One command to deploy/update

