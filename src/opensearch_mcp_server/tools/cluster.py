from opensearchpy import OpenSearch
from mcp.types import TextContent
from mcp.server.fastmcp import FastMCP


def register_tools(mcp: FastMCP, client: OpenSearch):

    @mcp.tool(description="Get cluster health status")
    async def opensearch_cluster_health() -> list[TextContent]:
        """
        Get cluster health status.

        :return: the information about the health of cluster, includes the number of nodes, the active shards, etc.
        """
        try:
            response = client.cluster.health()
            return [TextContent(type="text", text=str(response))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]

    @mcp.tool(description="Get cluster statistics information")
    async def opensearch_cluster_stats() -> list[TextContent]:
        """
        Get cluster statistics information.

        :return: the information about the statistics of cluster, includes statistics of indices,
        heap usage and threads of jvm, load and memory of os, disk usage of fs, etc.
        """
        try:
            response = client.cluster.stats()
            return [TextContent(type="text", text=str(response))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]
