from opensearchpy import OpenSearch
from mcp.types import TextContent
from mcp.server.fastmcp import FastMCP


def register_tools(mcp: FastMCP, client: OpenSearch):

    async def _opensearch_search(index_name: str, query_dsl: dict,
                                 offset: int = 0, limit: int = 10, **kwargs) -> TextContent:
        # from + size
        request_params = {
            "from_": query_dsl.get("from", offset),
            "size": query_dsl.get("size", limit)
        }
        # source includes
        source = query_dsl.get("_source")
        output_fields = kwargs.get("output_fields")
        if isinstance(source, list):
            request_params["_source_includes"] = ",".join(source)
        elif isinstance(source, dict) and source.get("includes"):
            includes = source.get("includes")
            request_params["_source_includes"] = ",".join(includes)
        elif output_fields:
            request_params["_source_includes"] = ",".join(output_fields)
        # search pipeline
        search_pipeline = kwargs.get("search_pipeline")
        if search_pipeline:
            request_params["search_pipeline"] = search_pipeline

        try:
            response = client.search(index=index_name, body=query_dsl, params=request_params)
            return TextContent(type="text", text=str(response))
        except Exception as e:
            return TextContent(type="text", text=f"Error: {str(e)}")

    @mcp.tool(description="Query index using the provided query dsl")
    async def opensearch_search(index_name: str, query_dsl: dict, offset: int = 0, limit: int = 10) -> TextContent:
        """
        Query index using the provided query dsl.

        :param index_name: the name of the index
        :param query_dsl: the query dsl
        :param offset: the offset of the search
        :param limit: the limit of the search
        :return: the result of the search
        """
        return await _opensearch_search(index_name, query_dsl, offset, limit)

    @mcp.tool(description="Query index using full text search")
    async def opensearch_full_text_search(index_name: str, text_field: str, query_text: str,
                                          term_filters: dict = None, output_fields: list = None,
                                          offset: int = 0, limit: int = 10) -> TextContent:
        """
        Query index using full text search.

        :param index_name: the name of the index
        :param text_field: the name of text field
        :param query_text: the text content is used to full text search
        :param term_filters: the term filters are applied to filter documents
        :param output_fields: the fields to return
        :param offset: the start offset to return
        :param limit: the limit size to return
        :return: the results of the search
        """
        conditions = [{
            "match": {
                text_field: query_text
            }
        }]
        # term_filters
        if term_filters:
            for field, value in term_filters.items():
                conditions.append({
                    "term": {
                        field: value
                    }
                })

        query_dsl = {
            "query": {
                "bool": {
                    "must": conditions
                }
            }
        }
        return await _opensearch_search(index_name, query_dsl, offset, limit, output_fields=output_fields)

    @mcp.tool(description="Query index using vector search")
    async def opensearch_vector_search(index_name: str, vector_field: str, vector: list, k: int = 5,
                                       output_fields: list = None, offset: int = 0, limit: int = 10) -> TextContent:
        """
        Query index using vector search.

        :param index_name: the name of the index
        :param vector_field: the name of vector field
        :param vector: the vector elements are used to vector search
        :param k: the number of nearest neighbors
        :param output_fields: the fields to return
        :param offset: the start offset to return
        :param limit: the limit size to return
        :return: the results of the search
        """
        query_dsl = {
            "query": {
                "knn": {
                    vector_field: {
                        "vector": vector,
                        "k": k
                    }
                }
            }
        }
        return await _opensearch_search(index_name, query_dsl, offset, limit, output_fields=output_fields)

    @mcp.tool(description="Query index using hybrid search")
    async def opensearch_hybrid_search(index_name: str, text_field: str, query_text: str,
                                       vector_field: str, vector: list, k: int = 5, search_pipeline: str = None,
                                       output_fields: list = None, offset: int = 0, limit: int = 10) -> TextContent:
        """
        Query index using hybrid search.

        :param index_name: the name of the index
        :param text_field: the name of text field
        :param query_text: the text content is used to full text search
        :param vector_field: the name of vector field
        :param vector: the vector elements are used to vector search
        :param k: the number of nearest neighbors
        :param search_pipeline: the name of search pipeline that is used to normalization
        :param output_fields: the fields to return
        :param offset: the start offset to return
        :param limit: the limit size to return
        :return: the results of the search
        """
        query_dsl = {
            "query": {
                "hybrid": {
                    "queries": [
                        {
                            "match": {
                                text_field: query_text
                            }
                        },
                        {
                            "knn": {
                                vector_field: {
                                    "vector": vector,
                                    "k": k
                                }
                            }
                        }
                    ]
                }
            }
        }
        return await _opensearch_search(index_name, query_dsl, offset, limit,
                                        output_fields=output_fields, search_pipeline=search_pipeline)
