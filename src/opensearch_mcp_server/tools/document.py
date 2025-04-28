import json

from opensearchpy import OpenSearch
from mcp.types import TextContent
from mcp.server.fastmcp import FastMCP


def register_tools(mcp: FastMCP, client: OpenSearch):

    @mcp.tool(description="Write multiple document operations with bulk")
    async def opensearch_bulk(operations: list[dict]) -> TextContent:
        """
        Write multiple document operations using bulk.

        :param operations: operations are added to the bulk
        :return: the result of the bulk
        """
        try:
            if len(operations) == 0:
                return TextContent(type="text", text="No operations provided")
            # the operations must be separated by a '\n' and the entire string must be a single line
            strs = [json.dumps(operation) for operation in operations]
            request_body = "\n".join(strs)
            response = client.bulk(body=request_body)
            return TextContent(type="text", text=str(response))
        except Exception as e:
            return TextContent(type="text", text=f"Error: {str(e)}")

    @mcp.tool(description="Get a document from the index")
    async def opensearch_get_document(index_name: str, document_id: str) -> TextContent:
        """
        Get a document from the index.

        :param index_name: the name of the index
        :param document_id: the id of the document
        :return: the content of the document or null if document does not exist
        """
        try:
            response = client.get(index=index_name, id=document_id)
            return TextContent(type="text", text=str(response))
        except Exception as e:
            return TextContent(type="text", text=f"Error: {str(e)}")
