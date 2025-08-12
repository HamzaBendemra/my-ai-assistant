# app.py
import streamlit as st
import os
import sys
from dotenv import load_dotenv
from utils.auth import check_password
from datetime import datetime

# Load environment variables (for local development only)
if 'WEBSITE_HOSTNAME' not in os.environ:
    load_dotenv()

# Health check route (for Azure monitoring)
if len(sys.argv) > 1 and sys.argv[1] == "health":
    try:
        # Basic health check
        import anthropic  # noqa: F401
        import supabase  # noqa: F401
        print("OK - All dependencies available")
        sys.exit(0)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

# Streamlit configuration
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
    
    # Navigation info
    st.info("👈 Use the sidebar to navigate between Dashboard and Chat")
    
    # Quick metrics preview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Go to Dashboard", use_container_width=True):
            st.switch_page("pages/1_📊_Dashboard.py")
    
    with col2:
        if st.button("💬 Start Chat", use_container_width=True):
            st.switch_page("pages/2_💬_Chat.py")
    
    with col3:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    st.divider()
    
    # System status
    with st.container():
        st.subheader("🔧 System Status")
        
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
        
        # Quick dependency check
        try:
            import anthropic  # noqa: F401
            import supabase  # noqa: F401
            st.success("✅ All dependencies loaded successfully")
        except ImportError as e:
            st.error(f"❌ Dependency error: {e}")

        # Show Azure deployment info
        if 'WEBSITE_HOSTNAME' in os.environ:
            with st.expander("🔍 Azure Deployment Info"):
                st.write(f"**Site Name:** {os.environ.get('WEBSITE_SITE_NAME', 'Unknown')}")
                st.write(f"**Resource Group:** {os.environ.get('WEBSITE_RESOURCE_GROUP', 'Unknown')}")
                st.write(f"**Instance ID:** {os.environ.get('WEBSITE_INSTANCE_ID', 'Unknown')}")
                st.write(f"**Python Version:** {sys.version}")

if __name__ == "__main__":
    main()