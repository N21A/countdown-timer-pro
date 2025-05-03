"""
streamlit_app.py
----------------
Author: Nida Anis
Date: 03/05/2025
----------------
Description:
-> Countdown Timer Pro main program
"""

import streamlit as st
import os

from datetime import datetime

from src.state_management import initialise_session_state
from src.display import display_clock, display_event_list, display_team_logo
from src.forms import add_event_form, edit_event_form, upload_logo_form
from src.calendar_view import display_calendar_view
from src.export_events import display_export_options
from src.import_events import display_import_options
from src.ui_themes import initialise_themes, apply_theme
from src.theme_controls import dark_mode_toggle
from src.database import initialise_db, save_session_data

def configure_page():
    """Configure streamlit page settings."""
    st.set_page_config(
        page_title="Countdown Timer Pro",
        page_icon="⏳",
        layout="wide",
        initial_sidebar_state="auto"
    )

def apply_styles():
    """Apply custom styles and themes."""
    # Initialise and apply theme
    initialise_themes()
    theme = apply_theme()

    # Additional custom CSS
    custom_css = """
    <style>
        /* Hide app header */
        header.stAppHeader {
            visibility: hidden;
            height: 0px;
        }

        /* Reset padding */
        .block-container{
            padding-top: 0px !important;
        }

        /* Improved button styling */
        .stButton > button {
            border-radius: 8px;
            font-weight: 500;
            transition: all 0.3s ease;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 4px 4px 0px 0px;
            padding: 10px 20px;
        }
    </style>
    """

    st.markdown(custom_css, unsafe_allow_html=True)

    return theme

def main():
    """Main Countdown Timer Pro program."""
    # Configure page and initialise session state
    configure_page()
    initialise_session_state()

    # Initialise database and load savefd data
    initialise_db()

    # Apply styles and get theme settings
    theme = apply_styles()
    
    # Display logo
    display_team_logo()

    # Display clock
    display_clock()

    # Create tabs for different views
    tabs = st.tabs([
        "Upcoming events",
        "Calendar view",
        "Import/export"
    ])

    with tabs[0]:
        st.subheader("Upcoming events")

        # Display events list
        display_event_list()
    
    with tabs[1]:
        st.subheader("Calendar view")

        # Display calendar
        display_calendar_view()

    with tabs[2]:
        col1, col2 = st.columns(2)

        with col1:
            # Show import options
            display_import_options()
        
        with col2:
            # Show export options
            display_export_options()

    # Sidebar
    with st.sidebar:
        st.title("Settings")

        # Dark mode toggle
        dark_mode_toggle()

        # Determine which form to show
        if st.session_state.get("show_edit_form", False):
            edit_event_form()
        
        else:
            # Add a new event form
            add_event_form()
        
        # Team logo upload
        upload_logo_form()

        # About section
        with st.expander("About"):
            st.markdown("""
            # Countdown Timer Pro
            
            A professional event management and countdown timer application.
                        
            **Features:**
            - Digital clock with active event highlighting
            - Calendar view for visual scheduling
            - Import/export scheduled events
            - Light/dark mode support
            - Custom theme editor

            Version 0.0.1 © Nida Anis, 2025     
            """)

    # Save session data to database when app refreshes
    save_session_data()

if __name__ == "__main__":
    # Ensure directory structure exists
    os.makedirs("assets", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    main()
    