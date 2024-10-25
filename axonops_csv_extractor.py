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
import axonops.metric.query as query
import argparse
import datetime
import os
import time
from axonops.csv.jsontocsv import json_to_csv
from axonops.jsonresults import write_json_results_file, setup_results_directory
from axonops.logger import setup_logger
from axonops.queryconfig import load_query_config, Query

logger = setup_logger(__name__)


def parse_arguments():
    """Parse and validate command line arguments."""
    parser = argparse.ArgumentParser(description="AxonOps CSV Extractor")

    parser.add_argument(
        '-o', '--outputdir',
        type=validate_output_dir,
        default="data/results",
        required=True,
        help="The file path to a directory for outputting the CSV data."
    )

    parser.add_argument(
        '-q', '--queryconfig',
        type=validate_query_config,
        required=True,
        help="File path to the JSON configuration file listing the queries to run and extract to CSV. See the README.md for more information on this configuration file."
    )

    parser.add_argument(
        '-m', '--monthofyear',
        type=validate_month_of_year,
        required=True,
        help="The month of year in format YYYYMM for which data will be extracted to CSV. This can not be in the future nor the current month"
    )

    parser.add_argument(
        '-d', '--deletejson',
        action='store_false',
        default=True,
        help="If set, the downloaded JSON will be kept in the output directory. By default it is automatically deleted after being converted to CSV."
    )

    args = parser.parse_args()

    # Unpack monthofyear into two separate variables
    start_timestamp, end_timestamp, querymonth = args.monthofyear

    return args.outputdir, args.queryconfig, start_timestamp, end_timestamp, querymonth, args.deletejson


def __process_cluster_data(results_dir, cluster_name, start_date, end_date, query_config: Query,
                           deletejson: bool = True):
    description = query_config.description
    unit = query_config.unit
    axon_query = query_config.axon_query
    logger.info(f"{cluster_name} - About to run AxonQuery {axon_query}")
    file_prefix = query_config.file_prefix
    field_renames = query_config.field_renames

    json_result = query.query_api(description, unit, axon_query, start_date, end_date, cluster_name, field_renames)

    json_file = write_json_results_file(json_result, results_dir, file_prefix, cluster_name)
    logger.debug(f'{cluster_name} - JSON results written to: {json_file}')
    csv_file = json_to_csv(json_file, deletejson)
    logger.info(f'{cluster_name} - Generated CSV: {csv_file}')


def validate_output_dir(path):
    """Validate that the output directory exists and is writable."""
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError(f"Output directory '{path}' does not exist.")
    if not os.access(path, os.W_OK):
        raise argparse.ArgumentTypeError(f"Output directory '{path}' is not writable.")
    return path


def validate_query_config(path):
    """Validate that the query configuration file exists and is readable."""
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError(f"Query configuration file '{path}' does not exist.")
    if not os.access(path, os.R_OK):
        raise argparse.ArgumentTypeError(f"Query configuration file '{path}' is not readable.")
    return path


def validate_month_of_year(value):
    """Validate the month of year format and calculate Unix timestamps."""
    try:
        date = datetime.datetime.strptime(value, "%Y%m")
    except ValueError:
        raise argparse.ArgumentTypeError(f"Month of year '{value}' is not in the format YYYYMM.")

    # Get current date
    current_date = datetime.datetime.now()
    current_month_start = datetime.datetime(current_date.year, current_date.month, 1)

    # Check if the date is in the future or the current month
    if date >= current_month_start:
        raise argparse.ArgumentTypeError("Month of year cannot be in the future or the current month.")

    # Calculate Unix timestamps
    start_of_month = int(time.mktime(date.timetuple()))
    next_month = (date.replace(day=28) + datetime.timedelta(days=4)).replace(day=1)
    start_of_next_month = int(time.mktime(next_month.timetuple()))

    querymonth = int(value)

    return start_of_month, start_of_next_month, querymonth

def main():
    # Parse arguments first
    outputdir, queryconfig, start_timestamp, end_timestamp, querymonth, deletejson = parse_arguments()

    # Now you can use these variables for your application logic
    logger.debug(f"Output Directory: {outputdir}")
    logger.debug(f"Query Config: {queryconfig}")
    logger.debug(f"Start Unix Timestamp: {start_timestamp}")
    logger.debug(f"End Unix Timestamp: {end_timestamp}")
    logger.debug(f"Query Month: {querymonth}")
    logger.debug(f"Delete JSON: {deletejson}")

    query_data = load_query_config(queryconfig)
    logger.info(f"Query config is loaded from: {queryconfig}")
    logger.debug(f"Query data: {query_data}")

    results_dir = setup_results_directory(outputdir, querymonth)
    logger.info(f"CSV output directory setup completed: {results_dir}")

    # Iterate over the list of clusters and download the metrics
    for cluster in query_data.clusters:
        logger.info(f'Starting downloading metrics for Cassandra cluster: {cluster}')
        for q in query_data.queries:
            __process_cluster_data(results_dir, cluster, start_timestamp, end_timestamp, q)

    logger.info(f'Finished writing JSON results to {results_dir}')


if __name__ == "__main__":
    main()