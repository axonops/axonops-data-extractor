import axonops.metric.queryv2 as queryv2
from axonops.csv.jsontocsv import json_to_csv
from axonops.jsonresults import write_json_results_file, setup_results_directory
from axonops.logger import setup_logger
from axonops.reportconfig import load_report_config, Query
from axonops.util.time import datetime_to_unix

logger = setup_logger(__name__)

config_path = 'data/reportconfig/monthly_query.json'

start_day = "2024-09-01"
start_time = "00:00:00"
start_datetime = datetime_to_unix(start_day, start_time)
logger.debug(f"Start date for report is {start_datetime}")

end_day = "2024-10-01"
end_time = "00:00:00"
end_datetime = datetime_to_unix(end_day, end_time)
logger.debug(f"End date for report is {end_datetime}")


def main():
    query_data = load_report_config(config_path)
    logger.info(f"Report config is loaded from: {config_path}")
    logger.debug(f"Query data: {query_data}")

    results_dir = setup_results_directory()
    logger.info(f"Results directory setup completed: {results_dir}")

    # Iterate over the list of clusters and download the metrics
    for cluster in query_data.clusters:
        logger.info(f'Starting downloading metrics for Cassandra cluster: {cluster}')
        for q in query_data.queries:
            __process_cluster_data(results_dir, cluster, start_datetime, end_datetime, q)

    logger.info(f'Finished writing JSON results to {results_dir}')


def __process_cluster_data(results_dir, cluster_name, start_date, end_date, query_config: Query):
    description = query_config.description
    unit = query_config.unit
    axon_query = query_config.axon_query
    file_prefix = query_config.file_prefix
    field_renames = query_config.field_renames

    json_result = queryv2.query_api(description, unit, axon_query, start_date, end_date, cluster_name, field_renames)

    json_file = write_json_results_file(json_result, results_dir, file_prefix, cluster_name)
    logger.debug(f'JSON results written to: {json_file}')
    csv_file = json_to_csv(json_file)
    logger.info(f'Generated CSV: {csv_file}')


if __name__ == "__main__":
    main()
