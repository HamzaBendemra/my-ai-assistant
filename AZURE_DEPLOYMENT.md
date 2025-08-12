# Azure App Service Deployment Guide

## Environment Variables to Configure in Azure App Service

Configure these in **Azure Portal** → **App Service** → **Configuration** → **Application settings**:

```
APP_PASSWORD=your_password_here
SUPABASE_URL=your_supabase_url_here
SUPABASE_ANON_KEY=your_supabase_anon_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
YNAB_ACCESS_TOKEN=your_ynab_access_token_here
YNAB_DEFAULT_BUDGET_NAME=Your Budget Name Here
SCM_DO_BUILD_DURING_DEPLOYMENT=true
```

**Note**: Replace the placeholder values above with your actual credentials from your `.env` file.

## Azure App Service Configuration

### General Settings
- **Stack**: Python 3.12
- **Startup Command**: `bash startup.sh`
- **Always On**: Enabled (recommended for production)
- **Platform**: 64 Bit

### Path Mappings
- No custom path mappings needed

### Deployment
- **Source**: GitHub Actions (automated via workflow)
- **Repository**: HamzaBendemra/my-ai-assistant
- **Branch**: main

## GitHub Actions Secrets

These should already be configured in your repository:
- `AZUREAPPSERVICE_CLIENTID_ADCAAAF23C0041F0AFD89BC400EF5F5B`
- `AZUREAPPSERVICE_TENANTID_C38E7AB3151340AEBCBB3054F5396E5B`
- `AZUREAPPSERVICE_SUBSCRIPTIONID_E86275723B4347F19140A20AE28F011B`

## Deployment Process

1. **Push to main branch** triggers GitHub Actions
2. **Build phase** installs dependencies and prepares deployment package
3. **Deploy phase** authenticates with Azure and deploys the app
4. **Health check** verifies deployment success

## Monitoring

- **Application URL**: https://my-ai-assistant-a7b0h4ctdaemh0fq.westeurope-01.azurewebsites.net/
- **Log Stream**: Available in Azure Portal
- **Health Check**: App includes built-in health monitoring
- **Metrics**: CPU, Memory, and Request metrics in Azure Portal

## Troubleshooting

### Common Issues
1. **Infinite Loading**: Usually environment variables not set
2. **Import Errors**: Dependencies not installed correctly
3. **Port Issues**: Startup command configuration problems

### Debug Steps
1. Check Application Logs in Azure Portal
2. Verify Environment Variables are set
3. Test health check endpoint
4. Review GitHub Actions deployment logs

### Health Check
The app includes a health check at `/health` that verifies:
- Dependencies are importable
- Environment variables are set
- Python version information
