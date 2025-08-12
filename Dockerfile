# Dockerfile
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Configure Poetry: Don't create virtual environment, disable interaction
RUN poetry config virtualenvs.create false \
    && poetry config virtualenvs.in-project false \
    && poetry config installer.parallel true

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock* ./

# Install dependencies using Poetry 
RUN poetry install --no-root

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 streamlit && chown -R streamlit:streamlit /app
USER streamlit

# Azure App Service expects port 8000 by default
EXPOSE 8000

# Run Streamlit on port 8000
CMD ["streamlit", "run", "app.py", "--server.port=8000", "--server.address=0.0.0.0"]