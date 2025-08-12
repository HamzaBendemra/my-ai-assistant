# pages/1_📊_Dashboard.py
import streamlit as st
from datetime import datetime
from utils.auth import check_password

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

if not check_password():
    st.stop()

st.title("📊 Dashboard")
st.caption(f"Updated: {datetime.now().strftime('%I:%M %p')}")

# Placeholder for calendar
st.subheader("📅 Today's Schedule")
with st.container():
    st.info("Calendar integration coming soon...")
    
# Placeholder for budget
st.subheader("💰 Budget Overview")
with st.container():
    st.info("YNAB integration coming soon...")