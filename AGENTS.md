# AGENTS.md

本文件为 Codex 等自动化协作代理提供本仓库的工作约定。作用范围为仓库根目录及其所有子目录。

## 项目概览

- 这是一个基于 FastMCP 的 OpenAPI/Swagger MCP Server。
- 核心包位于 `swagger_mcp/`：
  - `server.py` 定义 MCP 工具与服务实例。
  - `parser.py` 负责加载、验证和解析 OpenAPI 3.0 / Swagger 2.0 文档。
  - `models.py` 定义 Pydantic 数据模型。
- 测试位于 `test/`，使用 `pytest` 与 `pytest-asyncio`。

## 常用命令

- 安装依赖：`pip install -r requirements.txt`
- 运行测试：`pytest`
- 本地启动：`python swagger_mcp/server.py`
- FastMCP 启动：`fastmcp run swagger_mcp/server.py`
- 启动时预加载文档：`python swagger_mcp/server.py --swagger-uri <url-or-file>`

## 代码风格

- Python 代码保持简洁直接，优先修复根因，不做无关重构。
- 现有代码包含中英文注释与文档字符串；新增说明可沿用相邻文件语言风格。
- 公共返回值应保持当前 MCP 工具的字典结构：`success`、`error`、`message`、数据字段。
- 避免在导入阶段引入重型副作用；启动时预加载文档应通过 `--swagger-uri` 参数完成。
- 新增模型字段时，同步检查 `parser.py` 的解析逻辑与 `server.py` 的工具返回值。

## 测试约定

- 修改解析逻辑、模型或 MCP 工具时，优先添加或更新 `test/` 下的相关测试。
- 测试应尽量避免依赖外部网络；如需 OpenAPI 样例，优先使用内联 fixture 或本地临时文件。
- 提交前建议运行 `pytest`。如果测试失败且与当前改动无关，请在最终说明中明确指出。

## 协作注意事项

- 不要提交密钥、私有 Swagger 地址或本地绝对路径。
- 不要主动执行 `git commit` 或创建分支，除非用户明确要求。
- 保持改动聚焦在用户请求范围内，避免顺手改动 README、Dockerfile 或依赖版本。
