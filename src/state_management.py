"""
state_management.py
----------------
Author: Nida Anis
Date: 03/05/2025
----------------
Description:
-> Handles event storage and removal
"""

import streamlit as st
import os

from datetime import datetime

def initialise_session_state():
    """Make sure that session state variables exist."""
    if "events" not in st.session_state:
        st.session_state["events"] = []

    if "error_messages" not in st.session_state:
        st.session_state["error_messages"] = []
    
    if "team_logo" not in st.session_state:
        st.session_state["team logo"] = None
    
def save_uploaded_file(uploaded_file):
    """Saves the uploaded file to a designated folder, updates session state."""
    os.makedirs("assets", exist_ok=True)
    file_path = os.path.join("assets", "team_logo.png")

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.session_state["team_logo"] = file_path

def remove_past_events():
    """Removes past events from session state."""
    if "events" in st.session_state:
        st.session_state["events"] = [
            event for event in st.session_state["events"] if event["end"] > datetime.now()
        ]
