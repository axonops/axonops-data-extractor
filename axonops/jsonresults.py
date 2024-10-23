import os
import uuid
import datetime
import json

from axonops.logger import setup_logger
from axonops.util.apiconfig import get_axonops_org_id

logger = setup_logger(__name__)

org_id = get_axonops_org_id()


def setup_json_data_directory():
    today = datetime.datetime.now()
    formatted_date = today.strftime('%Y%m%d')
    directory_name = f'{formatted_date}-{uuid.uuid4()}'
    base_directory = 'data/results'
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
        raise FileExistsError(f"The file {file_path} already exists.")

    # Write JSON data to the file
    logger.info(f"Writing {file_path} with JSON")
    with open(file_path, 'w') as file:
        json.dump(json_result, file, indent=4)

    return file_path
