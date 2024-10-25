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
import os
import uuid
import datetime
import json

from axonops.logger import setup_logger
from axonops.util.apiconfig import get_axonops_org_id

logger = setup_logger(__name__)

org_id = get_axonops_org_id()


def setup_results_directory(base_directory, querymonth):
    directory_name = f'{querymonth}-{uuid.uuid4()}'
    new_directory_path = os.path.join(base_directory, directory_name)

    os.makedirs(new_directory_path, exist_ok=True)

    return new_directory_path


def write_json_results_file(json_result, directory, suffix, cluster_name, keyspace_name=None):
    if keyspace_name is not None:
        file_name = f'{org_id}-{cluster_name}-{keyspace_name}-{suffix}.json'
    else:
        file_name = f'{org_id}-{cluster_name}-{suffix}.json'

    file_path = os.path.join(directory, file_name)
    # Check if the file exists
    if os.path.exists(file_path):
        raise FileExistsError(f"{cluster_name} - The file {file_path} already exists.")

    # Write JSON data to the file
    logger.info(f"{cluster_name} - Writing {file_path} with JSON")
    with open(file_path, 'w') as file:
        json.dump(json_result, file, indent=4)

    return file_path
