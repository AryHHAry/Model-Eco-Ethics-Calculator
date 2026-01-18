# DEPLOYMENT.md

# Deployment Guide

## Local Development

### Prerequisites
- Python 3.11+
- pip

### Setup
```bash
# Clone or download files
cd ai-eco-calculator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

Access at: http://localhost:8501

## Cloud Deployment

### Option 1: Streamlit Community Cloud (Recommended)

1. Push code to GitHub repository
2. Go to https://streamlit.io/cloud
3. Click "New app"
4. Select repository and branch
5. Set main file: `app.py`
6. Click "Deploy"

**Pros:** Free, optimized for Streamlit, auto-deploy on push
**Cons:** Public only (for private need paid plan)

### Option 2: Render.com

1. Create account at https://render.com
2. Click "New +" → "Web Service"
3. Connect GitHub repository
4. Render auto-detects `render.yaml`
5. Click "Create Web Service"

**Pros:** Free tier available, supports private repos
**Cons:** Free tier sleeps after inactivity

### Option 3: Railway.app

1. Create account at https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Select repository
4. Railway auto-detects Python app
5. Add environment variable: `PORT=8501`
6. Deploy

**Pros:** $5 free credit monthly, fast deployments
**Cons:** Requires credit card after trial

### Option 4: Docker + Any Cloud
```bash
# Build image
docker build -t ai-eco-calculator .

# Run locally
docker run -p 8501:8501 ai-eco-calculator

# Deploy to cloud (AWS ECS, GCP Cloud Run, Azure Container Instances, etc.)
```

## Environment Variables

Optional environment variables:
```bash
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

## Custom Domain

### Streamlit Cloud
1. Go to app settings
2. Add custom domain
3. Update DNS CNAME record

### Render/Railway
1. Go to settings → Custom Domain
2. Add domain
3. Update DNS records as instructed

## Monitoring

### Streamlit Cloud
- Built-in analytics dashboard
- View logs in web interface

### Self-hosted
- Use application logs
- Monitor with tools like Sentry, DataDog, or custom logging

## Scaling Considerations

**Current version supports:**
- ~100 concurrent users (Streamlit Cloud free tier)
- Stateless calculations (no database)
- No persistent data storage

**For production scale:**
- Add caching with `@st.cache_data`
- Implement rate limiting
- Use Redis for session management
- Load balancer for multiple instances

## Security

**Recommendations:**
- Enable HTTPS (automatic on major platforms)
- Add rate limiting for API abuse prevention
- Sanitize user inputs (already implemented)
- Regular dependency updates

## Backup & Recovery

**Code:**
- Version controlled in Git
- Regular commits and tags

**Data:**
- No persistent data in current version
- Export functionality for users

## Support

For issues:
1. Check logs in deployment platform
2. Review error messages
3. Contact: aryhharyanto@proton.me