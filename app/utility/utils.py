import pytz
from datetime import datetime, timedelta

# Define the UTC+07:00 timezone (Bangkok time)
UTC_7 = pytz.timezone('Asia/Bangkok')

# Utility function to get current datetime in UTC+07:00
def get_current_time_utc_7() -> datetime:
    return datetime.now(UTC_7)

# Utility function to convert a given datetime to UTC+07:00 timezone
def convert_to_utc_7(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        dt = UTC_7.localize(dt)
    return dt.astimezone(UTC_7)


