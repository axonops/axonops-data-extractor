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


def _query_api(description, unit, axon_query, url, cluster_name, field_renames=None):
    try:
        # Make the GET request with headers
        start_time = time.time()  # Record the start time
        response = requests.get(url, headers=get_headers())
        # Raise an exception if the request was unsuccessful
        response.raise_for_status()
        end_time = time.time()  # Record the end time
        # Calculate the duration in milliseconds and log it
        duration_ms = math.ceil((end_time - start_time) * 1000)
        logger.info(f'{duration_ms} ms time taken for API request to {url}')

        data = response.json()

        # Add description and unit to each metric
        for result in data['data']['result']:
            result['metric']['axonops_org'] = org_id
            result['metric']['cluster_name'] = cluster_name
            result['metric']['description'] = description
            result['metric']['unit'] = unit
            result['metric']['axonops_query'] = axon_query

            # Rename fields based on field_renames dictionary
            if field_renames:
                for old_field, new_field in field_renames.items():
                    if old_field in result['metric']:
                        result['metric'][new_field] = result['metric'].pop(old_field)

        return data

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err} for URL {url}")
        raise RuntimeError(f"HTTP error occurred: {http_err} for URL {url}") from http_err
    except requests.exceptions.RequestException as err:
        logger.error(f"An requests error occurred: {err} for URL {url}")
        raise RuntimeError(f"An error occurred: {err} for URL {url}") from err
    except ValueError as json_err:
        logger.error(f"JSON decode error: {json_err} for URL {url}")
        raise RuntimeError(f"JSON decode error: {json_err} for URL {url}") from json_err


def _execute_query(description, unit, axon_query, cluster_name, start_date, end_date, field_renames=None):
    url = _generate_url(cluster_name, start_date, end_date, axon_query)
    logger.debug(f'Query {axon_query} API url generated for {cluster_name} -> {url}')
    result = _query_api(description, unit, axon_query, url, cluster_name, field_renames)
    logger.info(f'Query {axon_query} executed for {cluster_name}')
    return result


# Client Capacity Dashboard metrics
def get_live_disk_space_per_keyspace(cluster_name, start_date, end_date):
    description = "Live Disk Space Used by DC and Keyspace"
    unit = "bytes (SI)"

    # axon_query = "sum(cas_Table_LiveDiskSpaceUsed{function='Count',keyspace=~'.*',scope!=''}) by (dc, keyspace)"
    axon_query = "sum(cas_Table_LiveDiskSpaceUsed{function='Count',keyspace!~'system|system_auth|system_distributed|system_schema|system_traces',scope!=''}) by (dc, keyspace)"
    return _execute_query(description, unit, axon_query, cluster_name, start_date, end_date)


def get_live_disk_space_per_dc(cluster_name, start_date, end_date):
    description = "Live Disk Space Used by DC"
    unit = "bytes (SI)"

    axon_query = "sum(cas_Table_LiveDiskSpaceUsed{function='Count',keyspace!~'system|system_auth|system_distributed|system_schema|system_traces',scope!=''}) by (dc)"
    return _execute_query(description, unit, axon_query, cluster_name, start_date, end_date)


def get_average_coordinator_table_reads_per_second_per_keyspace(cluster_name, start_date, end_date):
    description = "Average Coordinator reads by Keyspace"
    unit = "rps"

    axon_query = "sum(cas_Table_CoordinatorReadLatency{axonfunction='rate',function=~'Count',keyspace!~'system|system_auth|system_distributed|system_schema|system_traces'}) by (keyspace)"
    return _execute_query(description, unit, axon_query, cluster_name, start_date, end_date)


# Additional metrics
def get_total_coordinator_table_reads_per_dc(cluster_name, start_date, end_date):
    description = "Total Coordinator Reads by DC and Keyspace"
    unit = "rps"

    field_renames = {
        "scope": "table",
    }

    axon_query = "sum(cas_Table_CoordinatorReadLatency{axonfunction='rate',function=~'Count',keyspace!~'system|system_auth|system_distributed|system_schema|system_traces'}) by (dc,keyspace,scope)"
    return _execute_query(description, unit, axon_query, cluster_name, start_date, end_date, field_renames)


def get_total_coordinator_table_range_reads_per_dc(cluster_name, start_date, end_date):
    description = "Total Coordinator Range Reads by DC and Keyspace"
    unit = "rps"

    field_renames = {
        "scope": "table",
    }

    axon_query = "sum(cas_Table_CoordinatorScanLatency{axonfunction='rate',function=~'Count',keyspace!~'system|system_auth|system_distributed|system_schema|system_traces'}) by (dc,keyspace,scope)"
    return _execute_query(description, unit, axon_query, cluster_name, start_date, end_date, field_renames)


def get_total_coordinator_table_writes_per_dc(cluster_name, start_date, end_date):
    description = "Total Coordinator Writes by DC and Keyspace"
    unit = "wps"

    field_renames = {
        "scope": "table",
    }

    axon_query = "sum(cas_Table_CoordinatorWriteLatency{axonfunction='rate',function=~'Count',keyspace!~'system|system_auth|system_distributed|system_schema|system_traces'}) by (dc,keyspace,scope)"
    return _execute_query(description, unit, axon_query, cluster_name, start_date, end_date, field_renames)


def get_write_counts(cluster_name, start_date, end_date):
    description = "Total Write Counts by node and table"
    unit = "wps"

    field_renames = {
        "scope": "table",
    }

    axon_query = "cas_Table_CoordinatorWriteLatency{function=~'Count',keyspace!~'system|system_auth|system_distributed|system_schema|system_traces'}"
    return _execute_query(description, unit, axon_query, cluster_name, start_date, end_date, field_renames)


def get_read_counts(cluster_name, start_date, end_date):
    description = "Total Read Counts by node and table"
    unit = "wps"

    field_renames = {
        "scope": "table",
    }

    axon_query = "cas_Table_CoordinatorReadLatency{function=~'Count',keyspace!~'system|system_auth|system_distributed|system_schema|system_traces'}"
    return _execute_query(description, unit, axon_query, cluster_name, start_date, end_date, field_renames)


def get_read_scan_counts(cluster_name, start_date, end_date):
    description = "Total Read Scan Counts by node and table"
    unit = "wps"

    field_renames = {
        "scope": "table",
    }

    axon_query = "cas_Table_CoordinatorScanLatency{function=~'Count',keyspace!~'system|system_auth|system_distributed|system_schema|system_traces'}"
    return _execute_query(description, unit, axon_query, cluster_name, start_date, end_date, field_renames)
