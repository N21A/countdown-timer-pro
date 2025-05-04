"""
forms.py
----------------
Author: Nida Anis
Date: 03/05/2025
----------------
Description:
-> Handles user input forms
"""

import streamlit as st

from datetime import datetime, timedelta
from src.helpers import validate_time_input
from src.state_management import initialise_session_state, save_uploaded_file
from src.database import save_session_data

def add_event_form():
    """Displays sidebar form for adding events."""
    initialise_session_state()

    st.sidebar.subheader("Add an event")
    with st.sidebar.form("add_event_form"):
        event_name = st.text_input("Event name", placeholder="Enter event name")
        event_date = st.date_input("Event date", min_value=datetime.now().date())
        event_time_str = st.text_input("Event time (HH:MM)", placeholder="12:34")
        event_duration = st.number_input("Duration (minutes)", min_value=1, value=60)
        submit_button = st.form_submit_button("Add event")

        st.session_state["error_messages"] = []

        if submit_button:
            if not event_name:
                st.session_state["error_messages"].append("Please enter an event name.")
            
            event_time = validate_time_input(event_time_str)
            if event_time == "error":
                st.session_state["error_messages"].append("Please enter the time in HH:MM format.")

            if st.session_state["error_messages"]:
                for error in st.session_state["error_messages"]:
                    st.error(error)
            
            else:
                event_start = datetime.combine(event_date, event_time)
                event_end = event_start + timedelta(minutes=event_duration)

                st.session_state["events"].append({
                    "name": event_name,
                    "start": event_start,
                    "end": event_end,
                    "duration": event_duration
                })

                st.success(f"Event '{event_name}' added.")
                st.rerun()

def edit_event_form():
    """Displays form for editing an existing event."""
    initialise_session_state()
    
    # Check if there is an event to edit
    if st.session_state.get("event_to_edit") is None:
        st.sidebar.info("Select an event to edit from the list:")
        # Add a "Back" button to return to the add event form
        if st.sidebar.button("Back"):
            st.session_state["show_edit_form"] = False
            st.session_state["event_to_edit"] = None
            st.rerun()
        return

    event_index = st.session_state["event_to_edit"]

    # Validate the event index
    if event_index >= len(st.session_state["events"]):
        st.sidebar.error("Invalid event selection.")
        st.session_state["show_event_form"] = False
        st.session_state["event_to_edit"] = None
        st.rerun()
        return

    event = st.session_state["events"][event_index]

    st.sidebar.subheader(f"Edit: {event['name']}")

    with st.sidebar.form("edit_event_form"):
        event_name = st.text_input("Event name", value=event["name"])
        event_date = st.date_input("Event date", value=event["start"].date())
        event_time_str = st.text_input("Event time (HH:MM)", value=event["start"].strftime("%H:%M"))
        event_duration = st.number_input("Duration (minutes)", min_value=1, value=event["duration"])

        col1, col2 = st.columns(2)
        with col1:
            save_button = st.form_submit_button("Save")
        with col2:
            cancel_button = st.form_submit_button("Cancel")

        if save_button:
            st.session_state["error_messages"] = []

            if not event_name:
                st.session_state["error_messages"].append("Please enter an event name.")

                event_time = validate_time_input(event_time_str)
                if event_time == "error":
                    st.session_state["error_messages"].append("Please enter the time in HH:MM format.")
                
                if st.session_state["error_messages"]:
                    for error in st.session_state["error_messages"]:
                        st.error(error)
                else:
                    event_start = datetime.combine(event_date, event_time)
                    event_end = event_start + timedelta(minutes=event_duration)

                    # Update the event
                    st.session_state["events"][event_index] = {
                        "name": event_name,
                        "start": event_start,
                        "end": event_end,
                        "duration": event_duration
                    }

                    st.success(f"Event '{event_name} updated.")
                    st.session_state["show_edit_form"] = False
                    st.session_state["event_to_edit"] = None
                    save_session_data() # Make the change persistent
                    st.rerun()
        
        if cancel_button:
            st.session_state["show_edit_form"] = False
            st.session_state["event_to_edit"] = None
            st.rerun()

def upload_logo_form():
    """Allows users to upload and set a team logo."""
    st.sidebar.subheader("Upload team logo")

    allowed_extensions = ["png", "jpg", "jpeg"]

    uploaded_file = st.sidebar.file_uploader("Choose an image", type=allowed_extensions)

    if uploaded_file is not None:
        file_extension = uploaded_file.name.split(".")[-1].lower()

        if file_extension not in allowed_extensions:
            st.sidebar.error("Invalid file type. Please upload a .png, .jpg, or .jpeg file.")
        else:
            save_uploaded_file(uploaded_file)
            st.sidebar.success("Logo uploaded successfully.")
            save_session_data()
            st.rerun()
