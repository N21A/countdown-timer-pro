
"""
theme_controls.py
----------------
Author: Nida Anis
Date: 03/05/2025
----------------
Description:
-> UI controls for theme management
"""

import streamlit as st
import json
import base64
from src.ui_themes import (
    initialise_themes,
    get_active_theme,
    set_theme,
    save_custom_theme,
    export_themes,
    import_themes
)

def dark_mode_toggle():
    """Add a simple dark/light mode toggle switch in the sidebar."""
    initialise_themes()
    
    # Get current theme status
    is_dark_mode = st.session_state["active_theme"] == "dark"
    
    # Create a container for the toggle and customization button
    container = st.sidebar.container()
    
    with container:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            cols = st.columns([1, 3, 1])
            
            with cols[0]:
                st.write("☀️")
            
            with cols[1]:
                # Use a toggle for the theme
                is_dark_mode = st.toggle("Dark Mode", value=is_dark_mode)
            
            with cols[2]:
                st.write("🌙")
        
        with col2:
            # Add palette button for customization
            if st.button("🎨", help="Customize theme"):
                st.session_state["show_theme_editor"] = not st.session_state.get("show_theme_editor", False)
    
    # Change theme if toggle state changed
    if is_dark_mode and st.session_state["active_theme"] != "dark":
        st.session_state["active_theme"] = "dark"
        st.rerun()
    elif not is_dark_mode and st.session_state["active_theme"] == "dark":
        st.session_state["active_theme"] = "light"
        st.rerun()
    
    # Show theme editor if requested
    if st.session_state.get("show_theme_editor", False):
        show_theme_editor()

def show_theme_editor():
    """Display the theme editor in a pop-up container."""
    with st.sidebar.expander("Theme customisation", expanded=True):
        st.markdown("### Create custom theme")

        # Get current theme as a base
        current_theme = get_active_theme()

        # Theme name
        theme_name = st.text_input("Theme name", value="Custom theme")

        # Colour pickers with two column
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Primary colours")
            primary_colour = st.color_picker("Primary colour", value=current_theme["primary_colour"])
            secondary_colour = st.color_picker("Secondary colour", value=current_theme["secondary_colour"])
            text_colour = st.color_picker("Text colour", value=current_theme["text_colour"])
            background_colour = st.color_picker("Background colour", value=current_theme["background_colour"])

        with col2:
            st.markdown("#### Clock and events")
            clock_background = st.color_picker("Clock background", value=current_theme["clock_background"])
            clock_text = st.color_picker("Clock text", value=current_theme["clock_text"])
            active_event_colour = st.color_picker("Active event", value=current_theme["active_event"])
            next_event_colour = st.color_picker("Next event", value=current_theme["next_event_colour"])

        # Font selection
        font_options = {
            "sans-serif": "Sans serif",
            "serif": "Serif",
            "monospace": "Monospace",
            "cursive": "Cursive",
        }

        font = st.selection(
            "Font family",
            options=list(font_options.keys()),
            index=list(font_options.keys()).index(current_theme.get("font", "sans-serif")),
            format_func=lambda x: font_options[x]
        )

        # Theme data dictionary
        theme_data = {
            "primary_colour": primary_colour,
            "secondary_colour": secondary_colour,
            "background_colour": background_colour,
            "text_colour": text_colour,
            "font": font,
            "clock_background": clock_background,
            "clock_text": clock_text,
            "active_event_colour": active_event_colour,
            "next_event_colour": next_event_colour
        }

        # Buttons for actions
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Save theme"):
                theme_id = save_custom_theme(theme_data, theme_name)

                # Set as active theme
                set_theme(theme_id)

                st.success(f"Saved theme: {theme_name}")
                st.rerun()

        with col2:
            if st.button("Apply"):
                # Create temporary theme
                temp_theme = {
                    "name": "Temporary",
                    "description": "Temporary theme",
                    **theme_data
                }

                # Use a special ID for temporary themes
                theme_id = "temp_theme"

                # Add to custom themes
                st.session_state["custom_themes"][theme_id] = temp_theme

                # Set as active theme
                set_theme(theme_id)

                st.rerun()

        with col3:
            if st.button("Cancel"):
                st.session_state["show_theme_editor"] = False
                st.rerun()

        # Theme management
        st.markdown("---")
        st.markdown("### Manage theme")

        # Show existing custom themes
        if st.session_state["custom_themes"]:
            theme_to_load = st.selectbox(
                "Load custom theme",
                options=[""] + list(st.session_state["custom_themes"].keys()),
                format_func=lambda x: st.session_state["custom_themes"][x]["name"] if x else "Select a theme"
            )

            if theme_to_load:
                st.button("Load selected theme")
                set_theme(theme_to_load)
                st.rerun()
        
        else:
            st.info("No custom themes have been created yet.")

        # Export / import themes
        st.markdown("---")
        st.markdown("### Export/import themes")

        if st.button("Export all themes"):
            json_str = export_themes()
            b64 = base64.b64encode(json_str.encode()).decode()
            href = f'<a href="data:application/json;base64,{b64}" download="countdown_themes.json">Download themes</a>'
            st.markdown(href, unsafe_allow_html=True)

        uploaded_file = st.file_uploader("Import themes", type=["json"])
        if uploaded_file:
            try:
                imported_data = json.load(uploaded_file)

                if import_themes(imported_data):
                    st.success("Successfully imported themes.")
                    st.rerun()
                
                else:
                    st.error("Invalid theme file format.")

            except Exception as e:
                st.error(f"Error importing themes {str(e)}")
                