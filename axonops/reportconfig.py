from axonops.logger import setup_logger
import json
from typing import List, Optional

logger = setup_logger(__name__)

class Rename:
    def __init__(self, rename: str, value: str):
        self.rename = rename
        self.value = value

    def __repr__(self):
        return f"Rename(rename={self.rename}, value={self.value})"


class Query:
    def __init__(self, description: str, unit: str, axon_query: str, file_prefix: str,
                 field_renames: Optional[List[Rename]] = None):
        self.description = description
        self.unit = unit
        self.axon_query = axon_query
        self.file_prefix = file_prefix
        self.field_renames = field_renames or []

    def __repr__(self):
        return (f"Query(description={self.description}, unit={self.unit}, "
                f"axon_query={self.axon_query}, file_prefix={self.file_prefix}, "
                f"field_renames={self.field_renames})")


class QueryData:
    def __init__(self, clusters: List[str], queries: List[Query]):
        self.clusters = clusters
        self.queries = queries

    def __repr__(self):
        return f"QueryData(clusters={self.clusters}, queries={self.queries})"


def load_report_config(file_path: str) -> QueryData:
    logger.info(f"Loading report config from {file_path}")
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        logger.error(f"The file at path '{file_path}' does not exist.")
        raise FileNotFoundError(f"The file at path '{file_path}' does not exist.")
    except json.JSONDecodeError:
        logger.error(f"The file at path '{file_path}' contains invalid JSON.")
        raise ValueError(f"The file at path '{file_path}' contains invalid JSON.")

    clusters = data.get('clusters', [])
    if not clusters or len(clusters) < 1:
        logger.error("The 'clusters' field is missing or has fewer than 1 element.")
        raise ValueError("The 'clusters' field is missing or has fewer than 1 element.")

    # Check if there are any queries defined
    queries_data = data.get('queries', [])
    if not queries_data or len(queries_data) < 1:
        logger.error("The 'queries' field is missing or has fewer than 1 element.")
        raise ValueError("The 'queries' field is missing or has fewer than 1 element.")

    queries = []
    for query in queries_data:
        # Check for mandatory fields
        mandatory_fields = ['description', 'unit', 'axon_query', 'file_prefix']
        missing_fields = [field for field in mandatory_fields if field not in query]

        if missing_fields:
            logger.error(f"Missing mandatory fields {missing_fields} in query definition.")
            raise ValueError(f"Missing mandatory fields {missing_fields} in query definition.")

        field_renames_data = query.get('field_renames', [])
        field_renames = [Rename(**rename) for rename in field_renames_data]

        queries.append(Query(
            description=query['description'],
            unit=query['unit'],
            axon_query=query['axon_query'],
            file_prefix=query['file_prefix'],
            field_renames=field_renames
        ))

    logger.debug(f"Finished loading report config from {file_path}")
    return QueryData(clusters=clusters, queries=queries)