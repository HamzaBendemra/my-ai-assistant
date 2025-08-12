# pages/2_💬_Chat.py
import os
import streamlit as st
from utils.auth import check_password
from services.claude_service import ClaudeService
from services.supabase_client import SupabaseService
from services.ynab_service import YNABService

st.set_page_config(
    page_title="Chat",
    page_icon="💬"
)

if not check_password():
    st.stop()

# Initialize services
@st.cache_resource
def init_services():
    return {
        "claude": ClaudeService(),
        "supabase": SupabaseService(),
        "ynab": YNABService(default_budget_name=os.getenv("YNAB_DEFAULT_BUDGET_NAME"))
    }

services = init_services()

st.title("💬 Chat Assistant")

# Sidebar info
with st.sidebar:
    st.subheader("Connected Services")
    
    # Check YNAB connection
    if services["ynab"].is_connected:
        budget_context = services["ynab"].get_budget_context_for_llm()
        if "Budget information not available" not in budget_context:
            st.success("✅ YNAB Connected")
        else:
            st.warning("⚠️ YNAB Token Invalid")
    else:
        st.info("➕ Add YNAB token in .env")
    
    st.divider()
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    # Show context that Claude has
    if st.checkbox("Show Assistant Context"):
        st.text_area("Budget Context", services["ynab"].get_budget_context_for_llm(), height=200)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Load recent history from Supabase
    recent_chats = services["supabase"].get_chat_history(5)
    for chat in reversed(recent_chats):  # Reverse to get chronological order
        st.session_state.messages.append({
            "role": "user", 
            "content": chat["user_message"]
        })
        st.session_state.messages.append({
            "role": "assistant", 
            "content": chat["assistant_response"]
        })

# Display messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about your budget, schedule, or anything else..."):
    # Add user message to UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get context for Claude
    context = {}
    
    # Add budget context if asking about money/budget
    budget_keywords = ["budget", "money", "spend", "spending", "expense", "cost", "afford", "save", "saving"]
    if any(keyword in prompt.lower() for keyword in budget_keywords):
        context["budget"] = services["ynab"].get_budget_context_for_llm()
    
    # Get Claude's response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = services["claude"].get_response(
                user_message=prompt,
                context=context if context else None,
                chat_history=st.session_state.messages[-10:]  # Send last 5 exchanges
            )
            st.markdown(response)
    
    # Add assistant response to session
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Save to Supabase
    services["supabase"].save_chat(prompt, response)