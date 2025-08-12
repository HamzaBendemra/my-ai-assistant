# pages/2_💬_Chat.py
import streamlit as st
from utils.auth import check_password

st.set_page_config(
    page_title="Chat",
    page_icon="💬"
)

if not check_password():
    st.stop()

st.title("💬 Chat Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # For now, just echo back
    response = f"You said: {prompt} (Claude integration coming soon)"
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)