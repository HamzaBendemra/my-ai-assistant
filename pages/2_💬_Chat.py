# pages/2_💬_Chat.py
import streamlit as st
from utils.auth import check_password
from services.claude_service import ClaudeService
from services.supabase_client import SupabaseService

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
        "supabase": SupabaseService()
    }

services = init_services()

st.title("💬 Chat Assistant")

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
if prompt := st.chat_input("Ask me anything..."):
    # Add user message to UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get Claude's response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = services["claude"].get_response(
                user_message=prompt,
                chat_history=st.session_state.messages[-10:]  # Send last 5 exchanges
            )
            st.markdown(response)
    
    # Add assistant response to session
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Save to Supabase
    services["supabase"].save_chat(prompt, response)

# Sidebar with chat controls
with st.sidebar:
    st.subheader("Chat Controls")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.caption("💡 Tip: Ask me about your schedule, budget, or any general questions!")