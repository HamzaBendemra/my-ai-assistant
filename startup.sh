#!/bin/bash

# Azure App Service startup script for Streamlit
echo "Starting Streamlit application..."

# Set default port if not provided by Azure
if [ -z "$PORT" ]; then
    export PORT=8000
fi

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    python -m pip install --upgrade pip
    pip install -r requirements.txt
fi

# Start Streamlit with Azure-optimized settings
echo "Starting Streamlit on port $PORT..."
python -m streamlit run app.py \
    --server.port=$PORT \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --browser.gatherUsageStats=false \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false \
    --server.enableWebsocketCompression=false