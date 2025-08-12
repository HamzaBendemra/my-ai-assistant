# utils/auth.py
import streamlit as st
import hashlib
import hmac
import os
from datetime import datetime


def check_password():
    """Simple password authentication"""

    def password_entered():
        """Check if entered password is correct"""
        entered_password = st.session_state["password"]
        correct_password = os.getenv("APP_PASSWORD", "changethis")

        if hmac.compare_digest(entered_password, correct_password):
            st.session_state["authenticated"] = True
            del st.session_state["password"]
        else:
            st.session_state["authenticated"] = False

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        if not st.session_state.get("authenticated"):
            st.error("Incorrect password")
        return False

    return True
