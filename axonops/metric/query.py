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
from typing import Optional, List

from axonops.queryconfig import Rename
from axonops.util.apiconfig import get_axonops_org_id, get_axonops_dash_url, get_headers
from axonops.logger import setup_logger
from urllib.parse import quote
import requests
import time
import math

logger = setup_logger(__name__)

org_id = get_axonops_org_id()
dash_url = get_axonops_dash_url()

# Question - what do I do about these extra args- extrapolate=false or true? &sampleResolution=5&bucketResolution=1&maxResult=2048
__base_url = "^DASH_URL^/^ORG_ID^/api/v1/query_range?start=^START_DATE^&end=^END_DATE^&query="


def _generate_url(cluster_name, start_date, end_date, query):
    # Find the position to insert the new values
    insert_position = query.find("}")  # Find the first closing brace
    # Create the new part of the query
    additional_params = f",org='{org_id}',type='cassandra',cluster='{cluster_name}'"
    # Concatenate to form the modified query
    modified_query = query[:insert_position] + additional_params + query[insert_position:]

    # URL-encode the modified query
    encoded_query = quote(modified_query, safe='')

    url = __base_url+encoded_query
    url = (url.replace('^DASH_URL^', dash_url)
           .replace('^ORG_ID^', org_id)
           .replace('^CLUSTER_NAME^', cluster_name)
           .replace('^START_DATE^', str(start_date))
           .replace('^END_DATE^', str(end_date))
           )
    return url


def query_api(description, unit, axon_query, start_date, end_date, cluster_name, field_renames: Optional[List[Rename]] = None):
    url = None
    try:
        url = _generate_url(cluster_name, start_date, end_date, axon_query)
        # Make the GET request with headers
        start_time = time.time()  # Record the start time
        response = requests.get(url, headers=get_headers())
        # Raise an exception if the request was unsuccessful
        response.raise_for_status()
        end_time = time.time()  # Record the end time
        # Calculate the duration in milliseconds and log it
        duration_ms = math.ceil((end_time - start_time) * 1000)
        status_code = response.status_code
        logger.info(f'{cluster_name} - HTTP Code {status_code} - {duration_ms} ms time taken for API request to {url}')
        # Log the HTTP response headers
        logger.info(f'{cluster_name} - HTTP Response Headers: {response.headers}')
        data = response.json()
        #logger.info(f"Paylod {data}")


        # Add description and unit to each metric
        for result in data['data']['result']:
            result['metric']['axonops_org'] = org_id
            result['metric']['cluster_name'] = cluster_name
            result['metric']['description'] = description
            result['metric']['unit'] = unit
            result['metric']['axonops_query'] = axon_query

            if field_renames:
                for r in field_renames:
                    old_name = r.rename
                    new_name = r.value
                    if old_name in result['metric']:
                        result['metric'][new_name] = result['metric'].pop(old_name)

        return data

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"{cluster_name} - HTTP error occurred: {http_err} for URL {url}")
        raise RuntimeError(f"{cluster_name} - HTTP error occurred: {http_err} for URL {url}") from http_err
    except requests.exceptions.RequestException as err:
        logger.error(f"{cluster_name} - A requests error occurred: {err} for URL {url}")
        raise RuntimeError(f"{cluster_name} - An error occurred: {err} for URL {url}") from err
    except ValueError as json_err:
        logger.error(f"{cluster_name} - JSON decode error: {json_err} for URL {url}")
        raise RuntimeError(f"{cluster_name} - JSON decode error: {json_err} for URL {url}") from json_err


def _execute_query(description, unit, axon_query, cluster_name, start_date, end_date, field_renames=None):
    url = _generate_url(cluster_name, start_date, end_date, axon_query)
    logger.debug(f'Query {axon_query} API url generated for {cluster_name} -> {url}')
    result = query_api(description, unit, axon_query, url, start_date, end_date, cluster_name, field_renames)
    logger.info(f'Query {axon_query} executed for {cluster_name}')
    return result



