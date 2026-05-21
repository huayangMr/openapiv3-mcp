# Swagger MCP | OpenAPI/Swagger MCP Tool

An OpenAPI/Swagger document MCP tool built on [FastMCP](https://gofastmcp.com), providing clean and efficient document querying and analysis capabilities.

基于 [FastMCP](https://gofastmcp.com) 构建的 OpenAPI/Swagger MCP Server，用于让 Codex 等客户端更准确地查询接口、数据模型和分组文档。

## 支持的文档入口

- 单个 OpenAPI 3.x / Swagger 2.0 文档，例如 `/v3/api-docs`、`/v2/api-docs`
- Springdoc / Swagger UI 多服务配置，例如 `/v3/api-docs/swagger-config`
- Springfox Swagger 2.0 分组资源，例如 `/swagger-resources`

Springfox v2 分组资源会先读取分组列表，再通过分组名加载对应文档：

```text
http://127.0.0.1:10021/makeid-boot/swagger-resources
http://127.0.0.1:10021/makeid-boot/v2/api-docs?group=APP
```

## 安装依赖

```bash
git clone <repo-url>
cd swagger-mcp
pip install -r requirements.txt
```

## 启动方式一：HTTP MCP 服务

HTTP 模式需要先启动本项目的 MCP 服务，然后让 Codex 连接 MCP 服务地址。

### 预加载 OpenAPI 3 / Springdoc swagger-config

```bash
FASTMCP_TRANSPORT=streamable-http \
FASTMCP_HOST=127.0.0.1 \
FASTMCP_PORT=8000 \
python swagger_mcp/server.py \
  --swagger-uri http://127.0.0.1:8080/v3/api-docs/swagger-config
```

### 预加载 Swagger 2 / Springfox swagger-resources

```bash
FASTMCP_TRANSPORT=streamable-http \
FASTMCP_HOST=127.0.0.1 \
FASTMCP_PORT=8000 \
python swagger_mcp/server.py \
  --swagger-uri http://127.0.0.1:10021/makeid-boot/swagger-resources \
  --swagger-source-type swagger_resources
```

Codex 配置：

```toml
[mcp_servers.swagger-mcp]
url = "http://127.0.0.1:8000/mcp"
```

## 启动方式二：stdio MCP 服务

stdio 模式不需要手动启动 HTTP 监听，Codex 会按配置启动本项目。

### OpenAPI 3 / Springdoc swagger-config

```toml
[mcp_servers.swagger-mcp]
command = "python"
args = [
  "/Users/huayangchen/mycode/swagger-mcp/server_start.py",
  "--swagger-uri",
  "http://127.0.0.1:8080/v3/api-docs/swagger-config",
]
```

### Swagger 2 / Springfox swagger-resources

```toml
[mcp_servers.swagger-mcp]
command = "python"
args = [
  "/Users/huayangchen/mycode/swagger-mcp/server_start.py",
  "--swagger-uri",
  "http://127.0.0.1:10021/makeid-boot/swagger-resources",
  "--swagger-source-type",
  "swagger_resources",
]
```

## 使用流程

加载多分组入口后，先查看可用服务，再加载某个分组：

```text
list_swagger_services
load_swagger_service("APP")
list_apis
get_api_details(path="/xxx", method="GET")
```

如果加载的是单个文档，可以直接使用 `list_apis`、`search_apis`、`get_api_details`、`list_schemas` 等工具。

## 可用工具

| 工具名称 | 功能描述 |
| --- | --- |
| `load_swagger` | 加载 OpenAPI/Swagger 文档、swagger-config 或 swagger-resources |
| `list_swagger_services` | 列出 swagger-config / swagger-resources 中的服务或分组 |
| `load_swagger_service` | 按服务名或分组名加载具体接口文档 |
| `get_swagger_info` | 获取当前文档基本信息 |
| `list_apis` | 列出当前文档的 API 端点 |
| `get_api_details` | 获取指定 API 的详细信息 |
| `search_apis` | 搜索 API 端点 |
| `list_schemas` | 列出所有数据模型 |
| `get_schema_details` | 获取指定数据模型详情 |

## 注意事项

- Codex 配置里的 `url` 必须是 MCP Server 地址，例如 `http://127.0.0.1:8000/mcp`，不能直接填写业务 Swagger 地址。
- 业务 Swagger 地址应通过 `--swagger-uri` 传入，例如 `http://127.0.0.1:10021/makeid-boot/swagger-resources`。
- Swagger 2 / Springfox 的 `/swagger-resources` 建议显式加 `--swagger-source-type swagger_resources`，也可以在工具调用时使用 `source_type="swagger_resources"`。
- 如果使用 HTTP 模式，请确认业务服务和本 MCP 服务都已启动，且端口不同。
- 如果使用 stdio 模式，请把 `server_start.py` 路径改成你本机仓库的实际绝对路径。
- 多分组入口只会预加载分组列表；需要调用 `load_swagger_service("<分组名>")` 后，`list_apis` 等工具才会针对该分组文档工作。
- 测试建议运行 `pytest`，测试用例不依赖外部网络。

## 本地开发

```bash
pytest
python swagger_mcp/server.py --help
```

## License

See [LICENSE](./LICENSE).
