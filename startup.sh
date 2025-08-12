#!/bin/bash

# Azure App Service startup script for Streamlit
echo "Starting Streamlit application on Azure App Service..."

# Azure App Service sets PORT automatically, fallback to 8000
if [ -z "$PORT" ]; then
    export PORT=8000
fi

echo "Using port: $PORT"

# Verify Python and dependencies
python --version
pip list | grep streamlit

# Start Streamlit with Azure-optimized settings
echo "Starting Streamlit server..."
exec python -m streamlit run app.py \
    --server.port=$PORT \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --browser.gatherUsageStats=false \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false \
    --server.enableWebsocketCompression=false