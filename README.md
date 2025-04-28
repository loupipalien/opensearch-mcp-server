# OpenSearch MCP Server
Interact with your OpenSearch cluster through natural language directly from any MCP Client (like Cursor, Cline) using the Model Context Protocol (MCP).  
This server provides the abilities of analyzing cluster health status, bulking documents to indices, getting index mappings, searching documents and so on through a set of tools.

## Tools
### Cluster
- `opensearch_cluster_health`: get cluster health status
- `opensearch_cluster_stats`: get cluster statistics information
### Document
- `opensearch_bulk`: write multiple document operations with bulk
- `opensearch_get_document`: get a document from the index
### Index
- `opensearch_list_indices`: list indices in the cluster
- `opensearch_create_index`: create index with specified configs
- `opensearch_delete_index`: delete index by index name
- `opensearch_get_index`: get information about index
### Search
- `opensearch_search`: query index using the provided query dsl

## Prerequisites
Before using this mcp server, you need to install the following components:
- python 3.10+ or higher
- [uv](https://github.com/astral-sh/uv) installed

## Usage
Select any of the following config to add to your mcp settings file. Then set your opensearch cluster hosts (separated by commas when multiple hosts), username and password to mcp server config.

### Run using remote repo
```json
{
  "mcpServers": {
    "opensearch-mcp-server": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/loupipalien/opensearch-mcp-server",
        "opensearch-mcp-server"
      ],
      "env": {
        "OPENSEARCH_HOSTS": "your_opensearch_cluster_hosts",
        "OPENSEARCH_USERNAME": "your_opensearch_cluster_username",
        "OPENSEARCH_PASSWORD": "your_opensearch_cluster_password"
      }
    }
  }
}
```
### Run using local repo
```json
{
  "mcpServers": {
    "opensearch-mcp-server": {
      "command": "uv",
      "args": [
        "--directory",
        "path/to/repo/src/opensearch_mcp_server",
        "run",
        "server.py"
      ],
      "env": {
        "OPENSEARCH_HOSTS": "your_opensearch_cluster_hosts",
        "OPENSEARCH_USERNAME": "your_opensearch_cluster_username",
        "OPENSEARCH_PASSWORD": "your_opensearch_cluster_password"
      }
    }
  }
}
```

## Start OpenSearch Cluster
If you don't have an OpenSearch cluster, you can run the following command in your local repository root directory to start one. More details can be found in [here](https://docs.opensearch.org/docs/latest/install-and-configure/install-opensearch/docker/).  
It will create a 2-node cluster and a dashboards. The default username is `admin` and password is `your_opensearch_cluster_password`. You can access the cluster from `https://localhost:9200` and access the dashboards from `http://localhost:5601`
```shell
export OPENSEARCH_INITIAL_ADMIN_PASSWORD=your_opensearch_cluster_password

docker-compose up -d
```
Stop the cluster and dashboards
```shell
docker-compose down -v
```

## License
This project is licensed under the [Apache v2.0 License](LICENSE.txt).