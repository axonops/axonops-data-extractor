from axonops.util.apiconfig import get_axonops_org_id, get_axonops_dash_url, get_headers
from axonops.logger import setup_logger
from urllib.parse import quote
import requests

logger = setup_logger(__name__)

org_id = get_axonops_org_id()
dash_url = get_axonops_dash_url()

# Question - what do I do about these extra args- extrapolate=false or true? &sampleResolution=5&bucketResolution=1&maxResult=2048
__base_url = "^DASH_URL^/^ORG_ID^/api/v1/query_range?start=^START_DATE^&end=^END_DATE^&extrapolate=false&maxResult=256&getDeletedMetrics=false&query="


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


def _query_api(description, unit, axon_query, url, cluster_name):
    try:
        # Make the GET request with headers
        response = requests.get(url, headers=get_headers())
        logger.debug(f'API response code for {cluster_name} -> {response.status_code}')
        # Raise an exception if the request was unsuccessful
        response.raise_for_status()

        data = response.json()

        # Add description and unit to each metric
        for result in data['data']['result']:
            result['metric']['description'] = description
            result['metric']['unit'] = unit
            result['metric']['axonops_query'] = axon_query

        return data

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
    except ValueError as json_err:
        print(f"JSON decode error: {json_err}")


def _execute_query(description, unit, axon_query, cluster_name, start_date, end_date):
    url = _generate_url(cluster_name, start_date, end_date, axon_query)
    logger.debug(f'Query {axon_query} API url generated for {cluster_name} -> {url}')
    result = _query_api(description, unit, axon_query, url, cluster_name)
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

    axon_query = "sum(cas_Table_CoordinatorReadLatency{axonfunction='rate',function=~'Count',keyspace!~'system|system_auth|system_distributed|system_schema|system_traces'}) by (dc,keyspace,scope)"
    return _execute_query(description, unit, axon_query, cluster_name, start_date, end_date)


def get_total_coordinator_table_range_reads_per_dc(cluster_name, start_date, end_date):
    description = "Total Coordinator Range Reads by DC and Keyspace"
    unit = "rps"

    axon_query = "sum(cas_Table_CoordinatorScanLatency{axonfunction='rate',function=~'Count',keyspace!~'system|system_auth|system_distributed|system_schema|system_traces'}) by (dc,keyspace,scope)"
    return _execute_query(description, unit, axon_query, cluster_name, start_date, end_date)


def get_total_coordinator_table_writes_per_dc(cluster_name, start_date, end_date):
    description = "Total Coordinator Writes by DC and Keyspace"
    unit = "wps"

    axon_query = "sum(cas_Table_CoordinatorWriteLatency{axonfunction='rate',function=~'Count',keyspace!~'system|system_auth|system_distributed|system_schema|system_traces'}) by (dc,keyspace,scope)"
    return _execute_query(description, unit, axon_query, cluster_name, start_date, end_date)
