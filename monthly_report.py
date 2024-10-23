import axonops.metric.query as query
from axonops.logger import setup_logger
from axonops.jsonresults import write_json_results_file, setup_results_directory
from axonops.util.apiconfig import get_axonops_org_cassandra_clusters
from axonops.util.time import datetime_to_unix
from axonops.csv.jsontocsv import json_to_csv
import time
import json

logger = setup_logger(__name__)

config_path = 'data/reportconfig/monthly.json'

def main():
    start_day = "2024-09-01"
    start_time = "00:00:00"
    start_datetime = datetime_to_unix(start_day, start_time)
    logger.debug(f"Start date for report is {start_datetime}")

    end_day = "2024-10-01"
    end_time = "00:00:00"
    end_datetime = datetime_to_unix(end_day, end_time)
    logger.debug(f"End date for report is {end_datetime}")

    results_dir = setup_results_directory()

    org_cassandra_clusters = get_axonops_org_cassandra_clusters()

    queries = __load_queries_from_config(config_path)

    # Iterate over the list of clusters and download the metrics
    for cluster in org_cassandra_clusters:
        logger.info(f'Starting downloading metrics for Cassandra cluster: {cluster}')
        # Process each query using the helper function
        for query_function, file_prefix in queries:
            __process_cluster_data(results_dir, cluster, start_datetime, end_datetime, query_function, file_prefix)

    logger.info(f'Finished writing JSON results to {results_dir}')


def __process_cluster_data(results_dir, cluster, start_datetime, end_datetime, query_function, file_prefix):
    json_result = query_function(cluster, start_datetime, end_datetime)
    json_file = write_json_results_file(json_result, results_dir, file_prefix, cluster)
    logger.debug(f'JSON results written to: {json_file}')
    csv_file = json_to_csv(json_file)
    logger.info(f'Generated CSV: {csv_file}')


def __load_queries_from_config(config_file):
    with open(config_file, 'r') as file:
        config = json.load(file)

    queries = []
    for item in config['queries']:
        function_name = item['function']
        file_prefix = item['file_prefix']

        # Dynamically get the function from the query module
        query_function = getattr(query, function_name)

        queries.append((query_function, file_prefix))

    return queries


if __name__ == "__main__":
    main()
