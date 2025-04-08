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
    parser = argparse.ArgumentParser(description="AxonOps Hourly CSV Extractor")

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
        '-h', '--hourofofyear',
        type=validate_hour_of_year,
        required=True,
        help="The hour of year in format YYYYMMDDHH for which data will be extracted to CSV. This can not be in the future nor the current hour"
    )

    parser.add_argument(
        '-d', '--deletejson',
        action='store_false',
        default=True,
        help="If set, the downloaded JSON will be kept in the output directory. By default it is automatically deleted after being converted to CSV."
    )

    args = parser.parse_args()

    # Unpack hour of year into two separate variables
    start_timestamp, end_timestamp, queryhour = args.hourofofyear

    return args.outputdir, args.queryconfig, start_timestamp, end_timestamp, queryhour, args.deletejson


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


def validate_hour_of_year(value):
    """Validate the hour of year format and calculate Unix timestamps."""
    try:
        # Parse the input as YYYYMMDDHH
        date = datetime.datetime.strptime(value, "%Y%m%d%H")
    except ValueError:
        raise argparse.ArgumentTypeError(f"Hour of year '{value}' is not in the format YYYYMMDDHH.")

    # Get the current date and time rounded to the hour
    current_date_time = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)

    # Ensure the input hour is at least one hour before the current hour
    if date >= current_date_time:
        raise argparse.ArgumentTypeError(
            "Hour of year cannot be in the current or future hour. "
            "Provide an hour in the past (at least one hour before the current time)."
        )

    # Calculate Unix timestamps for the start of the given hour
    start_of_hour = int(time.mktime(date.timetuple()))
    end_of_hour = start_of_hour + 3600 - 1  # Add 1 hour minus 1 second for the end timestamp

    # Convert the provided hour into an integer for easy return
    queryhour = int(value)

    # Return start and end of the hour, as well as the queryhour
    return start_of_hour, end_of_hour, queryhour



def main():
    # Parse arguments first
    outputdir, queryconfig, start_timestamp, end_timestamp, queryhour, deletejson = parse_arguments()

    # Now you can use these variables for your application logic
    logger.debug(f"Output Directory: {outputdir}")
    logger.debug(f"Query Config: {queryconfig}")
    logger.debug(f"Start Unix Timestamp: {start_timestamp}")
    logger.debug(f"End Unix Timestamp: {end_timestamp}")
    logger.debug(f"Query Month: {queryhour}")
    logger.debug(f"Delete JSON: {deletejson}")

    query_data = load_query_config(queryconfig)
    logger.info(f"Query config is loaded from: {queryconfig}")
    logger.debug(f"Query data: {query_data}")

    results_dir = setup_results_directory(outputdir, queryhour)
    logger.info(f"CSV output directory setup completed: {results_dir}")

    # Iterate over the list of clusters and download the metrics
    for cluster in query_data.clusters:
        logger.info(f'Starting downloading metrics for Cassandra cluster: {cluster}')
        for q in query_data.queries:
            __process_cluster_data(results_dir, cluster, start_timestamp, end_timestamp, q)

    logger.info(f'Finished writing JSON results to {results_dir}')


if __name__ == "__main__":
    main()