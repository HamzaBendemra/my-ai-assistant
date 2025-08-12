import streamlit as st
import hmac
import os


def check_password():
    """Simple password authentication with Azure support"""

    def password_entered():
        """Check if entered password is correct"""
        entered_password = st.session_state["password"]
        # Get password from environment (Azure App Service or local)
        correct_password = os.getenv("APP_PASSWORD")
        
        if not correct_password:
            st.error("APP_PASSWORD environment variable not set!")
            return
            
        if hmac.compare_digest(entered_password, correct_password):
            st.session_state["authenticated"] = True
            del st.session_state["password"]
        else:
            st.session_state["authenticated"] = False

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        # Show environment info for debugging
        if st.checkbox("Show debug info"):
            st.write(f"Running on Azure: {'WEBSITE_HOSTNAME' in os.environ}")
            st.write(f"Environment variables available: {len([k for k in os.environ.keys() if not k.startswith('_')])}")
        
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        if not st.session_state.get("authenticated"):
            st.error("Incorrect password")
        return False

    return True