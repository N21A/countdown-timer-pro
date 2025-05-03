"""
ui_themes.py
----------------
Author: Nida Anis
Date: 03/05/2025
----------------
Description:
-> Handles UI theming and customisation
"""

import streamlit as st
import json
import base64

from src.display import adjust_brightness

# Define available themes
DEFAULT_THEMES = {
    "light": {
        "name": "Light",
        "description": "Clean light theme",
        "primary_colour": "#4C78AF",
        "secondary_colour": "#FFD700",
        "background_colour": "#FFFFFF",
        "text_colour": "#262730",
        "font": "sans-serif",
        "clock_background": "#F0F2F6",  # Light grey background for the clock in light mode
        "clock_text": "#262730",         # Dark text for clock in light mode
        "active_event_colour": "#FF8C00",  # Orange for active events
        "next_event_colour": "#3B82F6"     # Blue for next events
    },
    "dark": {
        "name": "Dark",
        "description": "Dark theme for low light conditions",
        "primary_colour": "#3B82F6",
        "secondary_colour": "#F59E0B",
        "background_colour": "#121212",
        "text_colour": "#E5E7EB",
        "font": "sans-serif",
        "clock_background": "#1E1E1E",  # Dark grey background for clock in dark mode
        "clock_text": "#FFFFFF",         # White text for clock in dark mode
        "active_event_colour": "#F59E0B",  # Amber for active events
        "next_event_colour": "#60A5FA"     # Light blue for next events
    }
}

def initialise_themes():
    """Initialise themes in session state."""
    if "themes" not in st.session_state:
        st.session_state["themes"] = DEFAULT_THEMES.copy()
    
    if "active_theme" not in st.session_state:
        st.session_state["active_theme"] = "light"
        
    if "custom_themes" not in st.session_state:
        st.session_state["custom_themes"] = {}

    if "show_theme_editor" not in st.session_state:
        st.session_state["show theme editor"] = False

def get_active_theme():
    """Get the currently active theme."""
    initialise_themes()

    theme_id = st.session_state["active_theme"]

    # Check custom themes first
    if theme_id in st.session_state["custom_themes"]:
        return st.session_state["custom_themes"][theme_id]
    
    # Then check default themes
    if theme_id in st.session_state["themes"]:
        return st.session_state["themes"][theme_id]
    
    # Fallback to light theme
    return st.session_state["themes"]["light"]

def apply_theme():
    """Apply the active theme to the Streamlit UI."""
    theme = get_active_theme()

    # Apply theme using CSS
    st.markdown(
        f"""
        <style>
            /* Base styles */
            body {{
                color: {theme["text_colour"]};
                font-family: {theme["font"]};
                background-color: {theme["background_colour"]};
            }}

            /* Headings */
            h1, h2, h3, h4, h5, h6 {{
                color: {theme["primary_colour"]};
            }}

            /* Links */
            a {{
                color: {theme["primary_colour"]};
            }}

            /* Buttons */
            .stButton > button {{
                background-color: {theme["primary_colour"]};
                color: white;
                border-radius: 8px;
                font-weight: 500;
                border: none;
                transition: all 0.3s ease;
            }}

            .stButton > button:hover {{
                background-color: {theme["secondary_colour"]};
                color: {theme["text_colour"]};
                transform: translateY(-2px);
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}

            /* Input fields */
            div[data-baseweb="input"] input {{
                border-color: {theme["primary_colour"]};
            }}

            /* Sidebar */
            [data-testid="stSidebar"] {{
                background-color: {adjust_brightness(theme["background_colour"], -10)};
            }}

            /* Clock styles */
            .clock-container {{
                background-color: {theme["clock_background"]};
                color: {theme["clock_text"]};
            }}

            .active-event {{
                color: {theme["active_event_colour"]};
            }}

            .next-event {{
                color: {theme["next_event_colour"]};
            }}
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Return these colours for use in components
    return theme
