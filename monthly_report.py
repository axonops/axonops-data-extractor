import axonops.metric.query as query
from axonops.logger import setup_logger
from axonops.jsonresults import write_json_results_file, setup_results_directory
from axonops.util.apiconfig import get_axonops_org_cassandra_clusters
from axonops.util.time import datetime_to_unix
from axonops.csv.jsontocsv import json_to_csv
import time


logger = setup_logger(__name__)


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

    # Define a list of queries and their corresponding descriptions and file prefixes
    queries = [
        (query.get_live_disk_space_per_keyspace, 'get_live_disk_per_keyspace', 'live_disk_per_keyspace'),
        (query.get_live_disk_space_per_dc, 'get_live_disk_space_per_dc', 'live_disk_space_per_dc'),
        (query.get_average_coordinator_table_reads_per_second_per_keyspace,
         'get_average_coordinator_table_reads_per_second_per_keyspace',
         'average_coordinator_table_reads_per_second_per_keyspace'),
        (query.get_total_coordinator_table_reads_per_dc, 'get_total_coordinator_table_reads_per_dc',
         'total_coordinator_table_reads_per_dc'),
        (query.get_total_coordinator_table_range_reads_per_dc, 'get_total_coordinator_table_range_reads_per_dc',
         'total_coordinator_table_range_reads_per_dc'),
        (query.get_total_coordinator_table_writes_per_dc, 'get_total_coordinator_table_writes_per_dc',
         'total_coordinator_table_writes_per_dc'),
        (query.get_write_counts, 'get_write_counts', 'write_counts'),
        (query.get_read_counts, 'get_read_counts', 'read_counts'),
        (query.get_read_scan_counts, 'get_read_scan_counts', 'read_scan_counts')
    ]

    # Iterate over the list of clusters and download the metrics
    for cluster in org_cassandra_clusters:
        logger.info(f'Starting downloading metrics for Cassandra cluster: {cluster}')
        # Process each query using the helper function
        for query_function, description, file_prefix in queries:
            __process_cluster_data(results_dir, cluster, start_datetime, end_datetime, query_function, description, file_prefix)

    logger.info(f'Finished writing JSON results to {results_dir}')


def __process_cluster_data(results_dir, cluster, start_datetime, end_datetime, query_function, description, file_prefix):
    logger.info(f'Processing {description} for Cassandra cluster: {cluster}')
    json_result = query_function(cluster, start_datetime, end_datetime)
    json_file = write_json_results_file(json_result, results_dir, file_prefix, cluster)
    csv_file = json_to_csv(json_file)
    logger.info(f'Finished {description} for Cassandra cluster: {cluster} to CSV file: {csv_file}')


if __name__ == "__main__":
    main()
