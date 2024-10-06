from datetime import datetime
import pytz


def datetime_to_unix(date_str, time_str, timezone='UTC'):
    """
    Converts a given date, time, and timezone into a Unix timestamp.

    Parameters:
    - date_str: A string representing the date in 'YYYY-MM-DD' format.
    - time_str: A string representing the time in 'HH:MM:SS' 24-hour format.
    - timezone: An optional string representing the timezone (default is 'UTC').

    Returns:
    - An integer Unix timestamp.
    """

    # Combine date and time strings into one datetime string
    dt_str = f'{date_str} {time_str}'

    # Parse the datetime string into a naive datetime object
    naive_dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')

    # Set the appropriate timezone using pytz
    local_tz = pytz.timezone(timezone)

    # Localize the naive datetime object to the specified timezone
    localized_dt = local_tz.localize(naive_dt)

    # Convert the localized datetime to UTC
    utc_dt = localized_dt.astimezone(pytz.UTC)

    # Return the Unix timestamp as an integer
    return int(utc_dt.timestamp())