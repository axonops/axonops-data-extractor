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
from dotenv import load_dotenv
from axonops.logger import setup_logger

logger = setup_logger(__name__)

# Load the .env file
load_dotenv('.env')

# Accessing the variables
__axonops_dash_url = os.getenv('AXONOPS_DASH_URL', 'https://dash.axonops.cloud')
__axonops_cloud_api_token_secret = os.getenv('AXONOPS_API_SECRET_TOKEN')
__axonops_org_id = os.getenv('AXONOPS_ORG_ID')


def log_env_setup():
    logger.info(f'AXONOPS_DASH_URL: {__axonops_dash_url}')
    logger.info(f'AXONOPS_ORG_ID: {__axonops_org_id}')
    logger.info(f"AXONOPS_API_SECRET_TOKEN: {__axonops_cloud_api_token_secret[:4] + '*' * (len(__axonops_cloud_api_token_secret) - 4)}")


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
    headers = {
        "Authorization": f"Bearer {__axonops_cloud_api_token_secret}",
        "x-grafana-org-i": "axonops-report",
        "x-axonops-app-id": "axonops-report"
    }
    return headers
