import os

from dotenv import load_dotenv
from opensearchpy import OpenSearch


def create_opensearch_client() -> OpenSearch:
    """
    Create an opensearch client.
    """
    load_dotenv()

    config = {
        "hosts": os.getenv("OPENSEARCH_HOSTS"),
        "username": os.getenv("OPENSEARCH_USERNAME"),
        "password": os.getenv("OPENSEARCH_PASSWORD"),
    }

    return OpenSearch(
        hosts=config["hosts"],
        http_auth=(config["username"], config["password"]),
        verify_certs=False,
        ssl_show_warn=False,
    )
