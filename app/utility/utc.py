# app/utility/utc.py

import pytz
from datetime import datetime

# Define Cambodia timezone
CAMBODIA_TZ = pytz.timezone('Asia/Phnom_Penh')

# Function to convert UTC to Cambodia Time
def convert_utc_to_cambodia(utc_time: datetime) -> datetime:
    """
    Convert a UTC datetime to Cambodia time.
    :param utc_time: A datetime object in UTC.
    :return: A datetime object in Cambodia time.
    """
    if utc_time.tzinfo is None:
        # If the input datetime is naive (no timezone info), make it timezone-aware in UTC
        utc_time = pytz.utc.localize(utc_time)
    return utc_time.astimezone(CAMBODIA_TZ)

# Function to get current time in Cambodia Time
def get_current_cambodia_time() -> datetime:
    """
    Get the current time in Cambodia (Asia/Phnom_Penh).
    :return: A datetime object in Cambodia time.
    """
    return datetime.now(CAMBODIA_TZ)

# Function to convert Cambodia time to UTC
def convert_cambodia_to_utc(cambodia_time: datetime) -> datetime:
    """
    Convert Cambodia time to UTC.
    :param cambodia_time: A datetime object in Cambodia time.
    :return: A datetime object in UTC.
    """
    if cambodia_time.tzinfo is None:
        # If the input datetime is naive (no timezone info), make it timezone-aware
        cambodia_time = CAMBODIA_TZ.localize(cambodia_time)
    return cambodia_time.astimezone(pytz.utc)
