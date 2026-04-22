# Swagger MCP | OpenAPI/Swagger MCP Tool

---

An OpenAPI/Swagger document mcp tool built on [FastMCP](https://gofastmcp.com), providing clean and efficient document querying and analysis capabilities.

基于 [FastMCP](https://gofastmcp.com) 构建的 OpenAPI/Swagger MCP server, 更好更准确的编写前端代码和调用接口。

### 🚀 Quick Start | 快速开始

#### Method 1: Local Run | 本地运行

```bash
# Install dependencies
git clone 
cd swagger-mcp
pip install -r requirements.txt

# Run server
# First
##http注册模式，需要启动服务监听，命令如下
FASTMCP_TRANSPORT=streamable-http \
FASTMCP_HOST=127.0.0.1 \
FASTMCP_PORT=8000 \
python swagger_mcp/server.py --swagger-uri http://127.0.0.1:8080/v3/api-docs/swagger-config

##codex注册方式
[mcp_servers.swagger-mcp]
url = "http://127.0.0.1:8000/mcp"

# Seccond
##stdin/out注册模式,直接在codex使用即可
[mcp_servers.swagger-mcp]
command = "python"
args = [
  "/Users/huayangchen/mycode/swagger-mcp/server_start.py",
  "--swagger-uri",
  "http://127.0.0.1:8080/v3/api-docs/swagger-config",
]


### 🛠️ Available Tools | 可用工具

| Tool Name            | Description                    |
|----------------------|--------------------------------|
| `load_swagger`       | Load OpenAPI/Swagger documents |
| `get_swagger_info`   | Get document basic information |
| `list_apis`          | List all API endpoints         |
| `get_api_details`    | Get specific API details       |
| `search_apis`        | Search API endpoints           |
| `list_schemas`       | List all data models           |
| `get_schema_details` | Get specific model details     |


### 🛠️ 可用工具

| 工具名称                 | 功能描述                  |
|----------------------|-----------------------|
| `load_swagger`       | 加载 OpenAPI/Swagger 文档 |
| `get_swagger_info`   | 获取文档基本信息              |
| `list_apis`          | 列出所有 API 端点           |
| `get_api_details`    | 获取特定 API 详情           |
| `search_apis`        | 搜索 API 端点             |
| `list_schemas`       | 列出所有数据模型              |
| `get_schema_details` | 获取特定模型详情              |

---

**Developed by Vibe Coding** 🚀 
