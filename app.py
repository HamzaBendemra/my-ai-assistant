# app.py
import streamlit as st
import os
import sys
from dotenv import load_dotenv
from utils.auth import check_password
from datetime import datetime

# Load environment variables (for local development)
load_dotenv()

# Health check route (for Azure monitoring)
if len(sys.argv) > 1 and sys.argv[1] == "health":
    try:
        # Basic health check
        import anthropic
        import supabase
        print("OK")
        sys.exit(0)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

# Azure App Service compatibility
st.set_page_config(
    page_title="Life Assistant",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def main():
    # Authentication
    if not check_password():
        st.stop()
    
    # Main page
    st.title("🏠 Life Assistant")
    st.caption(f"Last updated: {datetime.now().strftime('%I:%M %p')}")
    
    # Environment indicator
    if 'WEBSITE_HOSTNAME' in os.environ:
        st.success("🟢 Running on Azure App Service")
        hostname = os.environ.get('WEBSITE_HOSTNAME', 'Unknown')
        st.caption(f"Hostname: {hostname}")
    else:
        st.info("🔵 Running locally")
    
    # Simple welcome message
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Budget", "Loading...", "")
    
    with col2:
        st.metric("Next Event", "Loading...", "")
    
    with col3:
        st.metric("Tasks", "Loading...", "")
    
    st.divider()
    
    st.info("👈 Use the sidebar to navigate between Dashboard and Chat")
    
    # Quick status
    with st.container():
        st.subheader("Quick Status")
        st.write("✅ App is running")
        st.write("✅ Authentication working")
        
        # Check environment variables
        env_vars = [
            "APP_PASSWORD",
            "SUPABASE_URL", 
            "SUPABASE_ANON_KEY",
            "ANTHROPIC_API_KEY",
            "YNAB_ACCESS_TOKEN",
            "YNAB_DEFAULT_BUDGET_NAME"
        ]
        
        missing_vars = [var for var in env_vars if not os.getenv(var)]
        
        if missing_vars:
            st.error(f"❌ Missing environment variables: {', '.join(missing_vars)}")
            st.info("Configure these in Azure App Service → Configuration → Application settings")
        else:
            st.success("✅ All environment variables configured")

        # Show deployment info
        if 'WEBSITE_HOSTNAME' in os.environ:
            with st.expander("🔍 Deployment Info"):
                st.write(f"**Site Name:** {os.environ.get('WEBSITE_SITE_NAME', 'Unknown')}")
                st.write(f"**Resource Group:** {os.environ.get('WEBSITE_RESOURCE_GROUP', 'Unknown')}")
                st.write(f"**Subscription ID:** {os.environ.get('WEBSITE_OWNER_NAME', 'Unknown')}")

if __name__ == "__main__":
    main()