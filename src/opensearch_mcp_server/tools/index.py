from opensearchpy import OpenSearch
from mcp.types import TextContent
from mcp.server.fastmcp import FastMCP


def register_tools(mcp: FastMCP, client: OpenSearch):

    @mcp.tool(description="List indices")
    async def opensearch_list_indices(index_name: str) -> TextContent:
        """
        List indices.

        :param index_name: an index name, or index names that are separated by commas
        :return: the information about indices, such as the health, status, uuid, shards, docs, store, and so on
        """
        try:
            if not index_name:
                response = client.cat.indices(params={"v": "true"})
            else:
                response = client.cat.indices(index=index_name, params={"v": "true"})
            return TextContent(type="text", text=str(response))
        except Exception as e:
            return TextContent(type="text", text=f"Error: {str(e)}")

    @mcp.tool(description="Create index")
    async def opensearch_create_index(index_name: str, index_aliases: dict, index_mappings: dict,
                                      index_settings: dict) -> TextContent:
        """
        Create index.

        :param index_name: the name of the index
        :param index_aliases: the aliases of the index
        :param index_mappings: the mappings of the index
        :param index_settings: the settings of the index
        :return: the result of creating an index
        """
        try:
            request_body = {
                "aliases": index_aliases,
                "mappings": index_mappings,
                "settings": index_settings
            }
            response = client.indices.create(index=index_name, body=request_body)
            return TextContent(type="text", text=str(response))
        except Exception as e:
            return TextContent(type="text", text=f"Error: {str(e)}")

    @mcp.tool(description="Delete index")
    async def opensearch_delete_index(index_name: str) -> TextContent:
        """
        Delete index.

        :param index_name: the name of the index
        :return: the result of deleting an index
        """
        try:
            response = client.indices.delete(index=index_name)
            return TextContent(type="text", text=str(response))
        except Exception as e:
            return TextContent(type="text", text=f"Error: {str(e)}")

    @mcp.tool(description="Get index")
    async def opensearch_get_index(index_name: str) -> TextContent:
        """
        Get index.

        :param index_name: the name of the index
        :return: the aliases, mappings, and settings about the index
        """
        try:
            response = client.indices.get(index=index_name)
            return TextContent(type="text", text=str(response))
        except Exception as e:
            return TextContent(type="text", text=f"Error: {str(e)}")
