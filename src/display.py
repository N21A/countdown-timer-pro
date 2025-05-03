"""
display.py
----------------
Author: Nida Anis
Date: 03/05/2025
----------------
Description:
-> Handles display elements
"""

import streamlit as st
import os
import base64

from datetime import datetime
from streamlit_autorefresh import st_autorefresh

from src.helpers import format_remaining_time
from src.state_management import remove_past_events, initialise_session_state
from src.ui_themes import get_active_theme

def display_clock():
    """Displays a large digital clock that highlights active events."""
    # Get theme colours
    theme = get_active_theme()
    clock_bg = theme["clock_background"]
    clock_text = theme["clock_text"]
    active_event_colour = theme["active_event_colour"]
    next_event_colour = theme["next_event_colour"]

    clock_placeholder = st.empty()
    event_placeholder = st.empty()
    next_event_placeholder = st.empty()

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    
    remove_past_events()
    sorted_events = sorted(st.session_state.get("events", []), key=lambda x: x["start"])

    current_event = next((event for event in sorted_events if event["start"] <= now <= event["end"]), None)
    next_event = next((event for event in sorted_events if event["start"] > now), None)

    # Use theme-aware colours
    clock_html = f"""
    <div style ="
        background-color: {clock_bg};
        color: {clock_text};
        text-align: center;
        padding: 40px 0;
        font-size: 150px;
        font-weight: bold;
        border-radius: 10px;
        width: 100%;
        display: block;">
        {current_time}
    </div>
    """

    clock_placeholder.markdown(clock_html, unsafe_allow_html=True)

    if current_event:
        event_html = f"""
        <h2 style="
            text-align: center;
            font-size: 50px;
            color: {active_event_colour};
            margin-top: 20px;"
            Currently active: {current_event['name']}</h2>
        """
        event_placeholder.markdown(event_html, unsafe_allow_html=True)
    
    if next_event:
        next_event_html = f"""
        <h3 style="
            text-align: center;
            font-size: 30px;
            color: {next_event_colour};
            margin-top: 10px;">
            Next event: {next_event['name']} at {next_event['start'].strftime('%H:%M')}</h3>
        """
        next_event_placeholder.markdown(next_event_html, unsafe_allow_html=True)

def display_event_list():
    """Displays list of upcoming events with countdowns and remove buttons."""
    theme = get_active_theme()
    primary_colour = theme["primary_colour"]
    text_colour = theme["text_colour"]
    bg_colour = theme["background_colour"]

    st.subheader("Upcoming events")

    if not st.session_state.get("events"):
        st.info("No upcoming events. Add one in the sidebar.")
        return
    
    remove_past_events()
    sorted_events = sorted(st.session_state["events"], key=lambda x: x["start"])

    for i, event in enumerate(sorted_events):
        remaining_time = event["start"] - datetime.now()

        # Create a theme-aware card style
        card_bg = adjust_brightness(bg_colour, 10)

        with st.container():
            st.markdown(
                f"""
                <div style="
                    background-color: {card_bg};
                    color: {text_colour};
                    padding: 15px;
                    border-radius: 10px;
                    margin-bottom: 15px;
                    border-left: 5px solid {primary_colour}
                >"
                    <h3 style="color: {primary_colour};">{event['name']}</h3>
                    <p><strong>Start:</strong> {event['start'].strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p><strong>End:</strong> {event['end'].strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p><strong>Time until start:</strong> {format_remaining_time(remaining_time)}</p>
                    </div>
                """,
                unsafe_allow_html = True
            )

            if st.button(f"Remove {event['name']}", key=f"remove_{i}"):
                st.session_state["events"] = [e for e in st.session_state["events"] if e != event]
                st.rerun()

def display_team_logo(centered=False):
    """Displays the team logo within a sticky header."""
    initialise_session_state()

    # Get current theme colours
    theme = get_active_theme()
    primary_colour = theme["primary_colour"]
    text_colour = theme["text_colour"]

    logo_path = "assets/team_logo.png"

    if os.path.exists(logo_path):
        with open(logo_path, "rb") as img_f:
            encoded = base64.b64encode(img_f.read()).decode("utf-8")
            logo_html = f"""
            <img src="
            data:image/png;
            base64,{encoded}"
            style="height:100px;
            width:auto">
            """
        
    else:
        # Display theme-aware title text if no logo is available
        logo_html = f"""
        <h1 style="
        font-size: 2.5rem;
        font-weight: bold;
        color:{primary_colour};
        margin: 0;">
        Countdown Timer Pro</h1>
        """
    
    logo_display_html = f"""
    <style>
        .logo-container {{
            text-align: center;
            margin-top: 3px;
            margin-bottom: 3px;
            color: {text_colour};
        }}
        .logo-container img {{
            height: 100px;
            width: auto;
        }}
    </style>

    <div class="logo-container">
        {logo_html}
    </div>
    """

    # Display header
    st.markdown(logo_display_html, unsafe_allow_html=True)

def adjust_brightness(hex_colour, amount):
    """
    Adjust the brightness of a hex colour.
    
    Args:
    -> hex_colour: Hex colour code (e.g., '#FFFFFF')
    -> amount: Amount to adjust (-100 to +100)

    Returns:
    -> Adjusted hex colour
    """
    # Convert hex to RGB
    hex_colour = hex_colour.lstrip('#')
    r, g, b = tuple(int(hex_colour[i:i+2], 16) for i in (0, 2, 4))
    
    # Adjust brightness
    r = max(0, min(255, r + amount))
    g = max(0, min(255, g + amount))
    b = max(0, min(255, b + amount))

    # Convert back into hex
    return f"#{int(r):02x}{int(g):02x}{int(b):02x}"
