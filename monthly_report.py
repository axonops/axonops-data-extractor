import axonops.metric.query as query
from axonops.logger import setup_logger
from axonops.jsonresults import write_json_results_file, setup_json_data_directory
from axonops.util.apiconfig import get_axonops_org_cassandra_clusters
from axonops.util.time import datetime_to_unix

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

    directory = setup_json_data_directory()

    org_cassandra_clusters = get_axonops_org_cassandra_clusters()
    # Iterate over the list of clusters and download the metrics
    for cluster in org_cassandra_clusters:
        logger.info(f'Starting downloading metrics for Cassandra cluster: {cluster}')

        logger.info(f'Processing get_live_disk_per_keyspace for Cassandra cluster: {cluster}')
        json_result = query.get_live_disk_space_per_keyspace(cluster, start_datetime, end_datetime)
        write_json_results_file(json_result, directory, "live_disk_per_keyspace", cluster)
        logger.info(f'Finished get_live_disk_per_keyspace for Cassandra cluster: {cluster}')

        logger.info(f'Processing get_live_disk_space_per_dc for Cassandra cluster: {cluster}')
        json_result = query.get_live_disk_space_per_dc(cluster, start_datetime, end_datetime)
        write_json_results_file(json_result, directory, "live_disk_space_per_dc", cluster)
        logger.info(f'Finished get_live_disk_space_per_dc for Cassandra cluster: {cluster}')

        logger.info(f'Processing get_average_coordinator_table_reads_per_second_per_keyspace for Cassandra cluster: {cluster}')
        json_result = query.get_average_coordinator_table_reads_per_second_per_keyspace(cluster, start_datetime, end_datetime)
        write_json_results_file(json_result, directory, "average_coordinator_table_reads_per_second_per_keyspace", cluster)
        logger.info(f'Finished get_average_coordinator_table_reads_per_second_per_keyspace for Cassandra cluster: {cluster}')

        logger.info(f'Processing get_total_coordinator_table_reads_per_dc for Cassandra cluster: {cluster}')
        json_result = query.get_total_coordinator_table_reads_per_dc(cluster, start_datetime, end_datetime)
        write_json_results_file(json_result, directory, "total_coordinator_table_reads_per_dc", cluster)
        logger.info(f'Finished get_total_coordinator_table_reads_per_dc for Cassandra cluster: {cluster}')

        logger.info(f'Processing get_total_coordinator_table_range_reads_per_dc for Cassandra cluster: {cluster}')
        json_result = query.get_total_coordinator_table_range_reads_per_dc(cluster, start_datetime, end_datetime)
        write_json_results_file(json_result, directory, "total_coordinator_table_range_reads_per_dc", cluster)
        logger.info(f'Finished get_total_coordinator_table_range_reads_per_dc for Cassandra cluster: {cluster}')

        logger.info(f'Processing get_total_coordinator_table_writes_per_dc for Cassandra cluster: {cluster}')
        json_result = query.get_total_coordinator_table_writes_per_dc(cluster, start_datetime, end_datetime)
        write_json_results_file(json_result, directory, "total_coordinator_table_writes_per_dc", cluster)
        logger.info(f'Finished get_total_coordinator_table_writes_per_dc for Cassandra cluster: {cluster}')

    logger.info(f'Finished writing JSON results to {directory}')


if __name__ == "__main__":
    main()
