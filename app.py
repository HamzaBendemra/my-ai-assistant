# app.py
import streamlit as st
import os
from dotenv import load_dotenv
from utils.auth import check_password
from datetime import datetime

# Load environment variables
load_dotenv()

# Page config
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
    
    # Simple welcome message for now
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
        st.write("⏳ Services not yet connected")

if __name__ == "__main__":
    main()