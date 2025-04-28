import argparse
import logging

from mcp.server.fastmcp import FastMCP

from opensearch_mcp_server.client import create_opensearch_client
from opensearch_mcp_server.tools import cluster, index, document, search

# logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class MCPServerOpenSearch:
    def __init__(self):
        self.name = "opensearch-mcp-server"
        self.mcp = FastMCP(self.name)

        self._register_tools()

    def _register_tools(self):
        """
        Register some tools.
        """
        client = create_opensearch_client()
        cluster.register_tools(mcp=self.mcp, client=client)
        index.register_tools(mcp=self.mcp, client=client)
        document.register_tools(mcp=self.mcp, client=client)
        search.register_tools(mcp=self.mcp, client=client)


def main():
    parser = argparse.ArgumentParser(description="Run the OpenSearch MCP Server")
    parser.add_argument(
        "--transport",
        "-t",
        choices=["sse", "stdio"],
        default="stdio",
        help="Transport protocol to use (sse or stdio)",
    )
    args = parser.parse_args()

    logger.info("Starting the OpenSearch MCP Server with %s transport", args.transport)
    server = MCPServerOpenSearch()
    server.mcp.run(transport=args.transport)


if __name__ == "__main__":
    main()
