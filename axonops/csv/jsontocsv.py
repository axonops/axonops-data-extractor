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
import json
import pandas as pd
import csv
import os

from yaspin import yaspin

from axonops.logger import setup_logger

logger = setup_logger(__name__)


def json_to_csv(json_file, deletejson: bool = True):
    # Load JSON data
    data = __load_and_validate_json(json_file)

    csv_file = __rename_json_to_csv(json_file)

    # Prepare lists for DataFrame columns
    all_data = []

    with yaspin(text=f"Converting JSON to CSV") as spinner:
        # Check if 'result' is part of the data
        if 'data' in data and 'result' in data['data']:
            # Iterate over each metric result
            for result in data['data']['result']:
                # Skip metrics with no values
                if 'values' not in result or not result['values']:
                    continue

                # Extract all available metric information dynamically
                metric_info = result.get('metric', {})

                # Loop through each timestamp-value pair
                for pair in result['values']:
                    if len(pair) == 2:
                        timestamp, value = pair
                        # Combine metric info with timestamp-value pair
                        all_data.append({
                            **metric_info,  # Include all metric fields dynamically
                            'unix_timestamp': timestamp,
                            'value': value
                        })

        # Create a DataFrame from the list of dictionaries
        all_data_df = pd.DataFrame(all_data)

        # Save DataFrame to CSV with proper quoting, excluding an index
        all_data_df.to_csv(csv_file, index=False, quotechar='"', quoting=csv.QUOTE_ALL)

        spinner.ok("✔")

    if deletejson:
        os.remove(json_file)
        logger.debug(f"JSON File '{json_file}' has been deleted.")

    return csv_file


def __rename_json_to_csv(file_path):
    # Check if the file path ends with .json
    if file_path.endswith('.json'):
        # Change the extension to .csv
        new_file_path = file_path[:-5] + '.csv'
        return new_file_path
    else:
        # Raise an error if the file does not end with .json
        raise ValueError("The file path does not end with '.json'")


def __load_and_validate_json(file_path):
    try:
        logger.debug(f"Loading and validating JSON {file_path}")
        # Load JSON data from the file
        with open(file_path, 'r') as file:
            json_data = json.load(file)

        # Check for the existence of the 'data' key
        if 'data' not in json_data:
            raise ValueError("The 'data' key is missing from the JSON.")

        # Validate the contents of the 'data' key
        if not isinstance(json_data['data'], dict):
            raise ValueError("The 'data' key is not an object.")
        if 'result' not in json_data['data']:
            raise ValueError("The 'result' key is missing within 'data'.")

        return json_data

    except FileNotFoundError:
        raise ValueError(f"File not found: {file_path}")
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format.")