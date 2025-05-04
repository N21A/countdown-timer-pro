
"""
database.py
----------------
Author: Nida Anis
Date: 03/05/2025
----------------
Description:
-> Simple JSON-based database for persistence
"""

import streamlit as st
import json
import os
from datetime import datetime
from src.state_management import initialise_session_state

DATA_DIR = "data"
EVENTS_FILE = os.path.join(DATA_DIR, "events.json")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")
THEMES_FILE = os.path.join(DATA_DIR, "themes.json")

def initialise_db():
    """Initialise database and load saved data."""
    initialise_session_state()

    # Ensure data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)

    # Load events
    if os.path.exists(EVENTS_FILE):
        try:
            with open(EVENTS_FILE, "r") as f:
                events_data = json.load(f)
                for event in events_data:
                    event["start"] = datetime.fromisoformat(event["start"])
                    event["end"] = datetime.fromisoformat(event["end"])
                st.session_state["events"] = events_data
        
        except Exception as e:
            st.warning(f"Could not load saved events: {str(e)}")
        
    # Load settings
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                settings_data = json.load(f)
                st.session_state["active_theme"] = settings_data.get("active_theme", "light")
                st.session_state["team_logo"] = settings_data.get("team logo")
            
        except Exception as e:
            st.warning(f"Could not load saved settings: {str(e)}")
    
    # Load custom themes:
    if os.path.exists(THEMES_FILE):
        try:
            with open(THEMES_FILE,"r") as f:
                themes_data = json.load(f)
                st.session_state["custom_themes"] = themes_data
        
        except Exception as e:
            st.warning(f"Could not load saved themes: {str(e)}")

def save_session_data():
    """Save current session data to files."""
    try:
        # Ensure data directory exists
        os.makedirs(DATA_DIR, exist_ok=True)

        # Save events
        events_data = []
        for event in st.session_state.get("events", []):
            event_copy = event.copy()
            event_copy["start"] = event_copy["start"].isoformat()
            event_copy["end"] = event_copy["end"].isoformat()
            events_data.append(event_copy)

        with open(EVENTS_FILE, "w") as f:
            json.dump(events_data, f, indent=2)
        
        # Save settings
        settings_data = {
            "active_theme": st.session_state.get("active_theme", "light"),
            "team_logo": st.session_state.get("team_logo")
        }

        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings_data, f, indent=2)
        
        # Save custom themes
        if st.session_state.get("custom_themes"):
            with open(THEMES_FILE, "w") as f:
                json.dump(st.session_state["custom_themes"], f, indent=2)
        
    except Exception as e:
        st.error(f"Error saving data: {str(e)}")

def clear_all_data():
    """Clear all saved data."""
    try:
        if os.path.exists(EVENTS_FILE):
            os.remove(EVENTS_FILE)
        if os.path.exists(SETTINGS_FILE):
            os.remove(SETTINGS_FILE)
        if os.path.exists(THEMES_FILE):
            os.remove(THEMES_FILE)
        
        st.session_state["events"] = []
        st.session_state["custom_themes"] = []
        st.session_state["active_theme"] = []
        st.session_state["team_logo"] = None

        st.success("All data has been cleared successfully.")
    
    except Exception as e:
        st.error(f"Error clearing data: {str(e)}")
        