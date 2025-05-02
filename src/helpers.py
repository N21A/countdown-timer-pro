"""
helpers.py
----------------
Author: Nida Anis
Date: 03/05/2025
----------------
Description:
-> Helper functions for formatting and validation
"""

from datetime import datetime

def format_remaining_time(remaining_time):
    """Formats remaining time as HH:MM:SS or 'now'."""
    if remaining_time.total_seconds() <= 0:
        return "now"

    hours, remainder = divmod(remaining_time.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    days = remaining_time.days

    if days > 0:
        return f"{days} days {hours:02}{minutes:02}"
    elif hours > 0:
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    else:
        return f"{minutes:02}:{seconds:02}"
    
def validate_time_input(event_time_str):
    """Validates time input in HH:MM:SS format. Returns a time object."""
    if event_time_str == "":
        return None
    
    try:
        return datetime.strptime(event_time_str, "%H:%M").time()
    except ValueError:
        return "error"
