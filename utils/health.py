# utils/health.py
import os
import sys
import json

def health_check():
    """Simple health check for Azure App Service"""
    try:
        # Check if main dependencies are available
        import anthropic  # noqa: F401
        import supabase  # noqa: F401
        
        # Check environment variables
        required_vars = [
            "APP_PASSWORD",
            "SUPABASE_URL", 
            "SUPABASE_ANON_KEY",
            "ANTHROPIC_API_KEY"
        ]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            return {"status": "unhealthy", "missing_vars": missing_vars}
        
        return {"status": "healthy", "python_version": sys.version}
    
    except ImportError as e:
        return {"status": "unhealthy", "error": str(e)}

if __name__ == "__main__":
    # This can be called directly for health checks
    print(json.dumps(health_check()))
