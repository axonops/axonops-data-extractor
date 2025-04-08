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
import os
import sys

from dotenv import load_dotenv
from axonops.logger import setup_logger

logger = setup_logger(__name__)

# Load the .env file
load_dotenv('.env')

# Accessing the variables
__axonops_dash_url = os.getenv('AXONOPS_DASH_URL', 'https://dash.axonops.cloud')
__axonops_cloud_api_token_secret = os.getenv('AXONOPS_API_SECRET_TOKEN')
__axonops_org_id = os.getenv('AXONOPS_ORG_ID')

def validate_env_variables():
    """
    Validates that all required environment variables are properly set.
    Raises a RuntimeError if any required variable is missing.
    """
    missing_vars = []

    # Check each required environment variable
    if not __axonops_dash_url:
        missing_vars.append("AXONOPS_DASH_URL")
    if not __axonops_cloud_api_token_secret:
        missing_vars.append("AXONOPS_API_SECRET_TOKEN")
    if not __axonops_org_id:
        missing_vars.append("AXONOPS_ORG_ID")

    # If any variables are missing, raise a RuntimeError with a helpful message
    if missing_vars:
        error_message = (
            f"The following required environment variables are missing: {', '.join(missing_vars)}. "
            "Please define them in the .env file or set them as environment variables."
        )
        logger.error(error_message)
        sys.exit(error_message)

    logger.info("All required environment variables are set.")


def log_env_setup():
    """
    Logs the environment variables, masking sensitive data, after they are validated.
    """
    validate_env_variables()

    if __axonops_cloud_api_token_secret:
        masked_token = __axonops_cloud_api_token_secret[:4] + '*' * (len(__axonops_cloud_api_token_secret) - 4)
    else:
        masked_token = "NOT SET"

    logger.info(f'AXONOPS_DASH_URL: {__axonops_dash_url}')
    logger.info(f'AXONOPS_ORG_ID: {__axonops_org_id or "NOT SET"}')
    logger.info(f"AXONOPS_API_SECRET_TOKEN: {masked_token}")


log_env_setup()


def get_axonops_org_id():
    if not __axonops_org_id:
        raise ValueError("The AxonOps Org is not set or is empty - please set AXONOPS_ORG_ID in the .env file or as an environment variable so it can be loaded")
    return __axonops_org_id


def get_axonops_dash_url():
    if not __axonops_dash_url:
        raise ValueError("The AxonOps Dash Url is not set or is empty - please set AXONOPS_DASH_URL in the .env file or as an environment variable so it can be loaded")
    return __axonops_dash_url


def get_headers():
    """
    Retrieve the headers for authorization, ensuring token exists.
    """
    if not __axonops_cloud_api_token_secret:
        raise ValueError(
            "The AxonOps API Secret Token is missing - "
            "please set AXONOPS_API_SECRET_TOKEN in the .env file or as an environment variable."
        )

    headers = {
        "Authorization": f"Bearer {__axonops_cloud_api_token_secret}",
        "x-grafana-org-i": "axonops-report",
        "x-axonops-app-id": "axonops-report"
    }
    return headers
