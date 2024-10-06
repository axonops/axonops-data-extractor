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
__axonops_org_cassandra_clusters = os.getenv('AXONOPS_ORG_CASSANDRA_CLUSTERS')


def log_env_setup():
    logger.info(f'AXONOPS_DASH_URL: {__axonops_dash_url}')
    logger.info(f'AXONOPS_ORG_ID: {__axonops_org_id}')
    logger.info(f'AXONOPS_ORG_CASSANDRA_CLUSTERS: {__axonops_org_cassandra_clusters}')
    logger.info(f'AXONOPS_API_SECRET_TOKEN: {__axonops_cloud_api_token_secret[:4] + '*' * (len(__axonops_cloud_api_token_secret) - 4)}')


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
        "Cache-Control": "no-cache",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
    }
    return headers


def get_axonops_org_cassandra_clusters():
    if not __axonops_org_cassandra_clusters:
        raise ValueError("The AxonOps Org Clusters is not set or is empty - please set AXONOPS_ORG_CLUSTERS in the .env file or as an environment variable so it can be loaded")
    return __axonops_org_cassandra_clusters.split(',')
