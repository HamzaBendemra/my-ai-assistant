# pages/1_📊_Dashboard.py
import os
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from utils.auth import check_password
from services.ynab_service import YNABService
from services.supabase_client import SupabaseService

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

if not check_password():
    st.stop()

# Initialize services
@st.cache_resource
def init_services():
    return {
        "ynab": YNABService(default_budget_name=os.getenv("YNAB_DEFAULT_BUDGET_NAME")),
        "supabase": SupabaseService()
    }

services = init_services()

st.title("📊 Dashboard")
st.caption(f"Updated: {datetime.now().strftime('%I:%M %p')}")

# Top metrics
col1, col2, col3 = st.columns(3)

# Get budget data (with caching)
@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_budget_summary():
    # Try cache first
    cached = services["supabase"].get_cached_data("budget_summary", max_age_minutes=5)
    if cached:
        return cached
    
    # Get fresh data
    summary = services["ynab"].get_current_month_budget()
    if summary:
        # Cache it
        services["supabase"].set_cached_data("budget_summary", summary, ttl_minutes=5)
    return summary

budget_data = get_budget_summary()

with col1:
    if budget_data:
        st.metric(
            "Budget Remaining",
            f"${budget_data['remaining']:,.0f}",
            f"-${budget_data['spent']:,.0f} spent"
        )
    else:
        st.metric("Budget", "Not connected", "Connect YNAB →")

with col2:
    st.metric("Next Event", "Coming soon", "Calendar integration pending")

with col3:
    recent_chats = services["supabase"].get_chat_history(1)
    if recent_chats:
        st.metric("Last Chat", "Active", "✅ Claude connected")
    else:
        st.metric("Chat Status", "Ready", "Start chatting →")

st.divider()

# Budget Details
if budget_data:
    st.subheader("💰 Budget Overview")
    
    # Create gauge chart
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = budget_data['remaining'],
        title = {'text': "Budget Remaining"},
        delta = {'reference': budget_data['budgeted']},
        gauge = {
            'axis': {'range': [None, budget_data['budgeted']]},
            'bar': {'color': "green" if budget_data['remaining'] > 0 else "red"},
            'steps': [
                {'range': [0, budget_data['budgeted']*0.5], 'color': "lightgray"},
                {'range': [budget_data['budgeted']*0.5, budget_data['budgeted']*0.8], 'color': "gray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': budget_data['budgeted'] * 0.1
            }
        }
    ))
    fig.update_layout(height=250)
    st.plotly_chart(fig, use_container_width=True)
    
    # Top categories
    st.subheader("Top Spending Categories")
    for cat in budget_data.get('categories', []):
        progress = cat['spent'] / cat['budgeted'] if cat['budgeted'] > 0 else 0
        st.progress(
            min(progress, 1.0),  # Cap at 100%
            text=f"{cat['name']}: ${cat['spent']:,.0f} / ${cat['budgeted']:,.0f}"
        )
else:
    st.info("👉 Add your YNAB access token to see budget data")

# Add this to pages/1_📊_Dashboard.py after the metrics section:

# Quick Actions Section
st.subheader("⚡ Quick Actions")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("💬 Ask about budget", use_container_width=True):
        st.switch_page("pages/2_💬_Chat.py")

with col2:
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

with col3:
    if st.button("📊 View Full Budget", use_container_width=True):
        st.info("This will open YNAB web app")
        st.markdown("[Open YNAB →](https://app.youneedabudget.com)")

with col4:
    if st.button("📅 Today's Events", use_container_width=True):
        st.info("Calendar integration coming soon")

st.divider()
