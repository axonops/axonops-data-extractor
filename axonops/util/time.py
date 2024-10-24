#  © 2024 AxonOps Limited. All rights reserved.

#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at

#      http://www.apache.org/licenses/LICENSE-2.0

#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
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
