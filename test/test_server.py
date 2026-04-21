"""
基本 MCP 服务器测试
"""

import json

import pytest


class TestMCPServer:
    """测试 MCP 服务器基本功能"""
    
    @pytest.mark.unit
    def test_server_creation(self):
        """测试服务器创建"""
        from swagger_mcp.server import mcp
        
        assert mcp is not None
        assert mcp.name == "swagger-mcp"
    
    @pytest.mark.unit  
    def test_server_has_tools(self):
        """测试服务器包含所有工具"""
        from swagger_mcp import server
        
        expected_tools = [
            "load_swagger",
            "list_swagger_services",
            "load_swagger_service",
            "get_swagger_info", 
            "list_apis",
            "get_api_details",
            "search_apis",
            "list_schemas",
            "get_schema_details"
        ]
        
        for tool_name in expected_tools:
            assert hasattr(server, tool_name), f"Tool function {tool_name} not found"
            tool_obj = getattr(server, tool_name)
            assert tool_obj is not None, f"Tool {tool_name} is None"


@pytest.mark.mcp
class TestMCPComponents:
    """测试 MCP 组件"""
    
    def test_parser_import(self):
        """测试解析器导入"""
        from swagger_mcp.parser import parser
        assert parser is not None
    
    def test_models_import(self):
        """测试模型导入"""
        from swagger_mcp.models import SwaggerDocument
        assert SwaggerDocument is not None
    
    def test_server_module_import(self):
        """测试服务器模块导入"""
        from swagger_mcp import server
        assert server is not None


@pytest.fixture
def springdoc_fixture_file(tmp_path):
    """创建 springdoc OpenAPI 3.1 fixture 文件"""
    spec = {
        "openapi": "3.1.0",
        "info": {
            "title": "标题：RuoYi-Cloud-Plus微服务权限管理系统_接口文档",
            "description": "描述：微服务权限管理系统",
            "version": "版本号：系统版本..."
        },
        "servers": [{"url": "http://127.0.0.1:8080", "description": "Generated server url"}],
        "paths": {
            "/auth/register": {
                "post": {
                    "tags": ["token 控制"],
                    "summary": "用户注册",
                    "description": "用户注册",
                    "operationId": "register",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/RegisterBody"}
                            }
                        },
                        "required": True
                    },
                    "responses": {
                        "200": {
                            "description": "OK",
                            "content": {
                                "*/*": {
                                    "schema": {"$ref": "#/components/schemas/RVoid"}
                                }
                            }
                        }
                    }
                }
            },
            "/auth/login": {
                "post": {
                    "tags": ["token 控制"],
                    "summary": "登录方法",
                    "description": "登录方法",
                    "operationId": "login",
                    "requestBody": {
                        "description": "登录信息",
                        "content": {
                            "application/json": {
                                "schema": {"type": "string"}
                            }
                        },
                        "required": True
                    },
                    "responses": {
                        "200": {
                            "description": "结果",
                            "content": {
                                "*/*": {
                                    "schema": {"$ref": "#/components/schemas/RLoginVo"}
                                }
                            }
                        }
                    }
                }
            },
            "/auth/binding/{source}": {
                "get": {
                    "tags": ["token 控制"],
                    "summary": "第三方登录请求",
                    "description": "第三方登录请求",
                    "operationId": "authBinding",
                    "parameters": [
                        {
                            "name": "source",
                            "in": "path",
                            "description": "登录来源",
                            "required": True,
                            "schema": {"type": "string"}
                        },
                        {
                            "name": "tenantId",
                            "in": "query",
                            "required": True,
                            "schema": {"type": "string"}
                        },
                        {
                            "name": "domain",
                            "in": "query",
                            "required": True,
                            "schema": {"type": "string"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "结果",
                            "content": {
                                "*/*": {
                                    "schema": {"$ref": "#/components/schemas/RString"}
                                }
                            }
                        }
                    }
                }
            },
            "/auth/unlock/{socialId}": {
                "delete": {
                    "tags": ["token 控制"],
                    "summary": "取消授权",
                    "description": "取消授权",
                    "operationId": "unlockSocial",
                    "parameters": [
                        {
                            "name": "socialId",
                            "in": "path",
                            "description": "socialId",
                            "required": True,
                            "schema": {"type": "integer", "format": "int64"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "OK",
                            "content": {
                                "*/*": {
                                    "schema": {"$ref": "#/components/schemas/RVoid"}
                                }
                            }
                        }
                    }
                }
            }
        },
        "components": {
            "schemas": {
                "RegisterBody": {
                    "type": "object",
                    "description": "用户注册对象",
                    "properties": {
                        "clientId": {"type": "string", "description": "客户端id", "minLength": 1},
                        "username": {"type": "string", "description": "用户名", "minLength": 1},
                        "password": {"type": "string", "description": "用户密码", "minLength": 1}
                    },
                    "required": ["clientId", "password", "username"]
                },
                "LoginVo": {
                    "type": "object",
                    "description": "登录验证信息",
                    "properties": {
                        "access_token": {"type": "string", "description": "授权令牌"}
                    }
                },
                "RLoginVo": {
                    "type": "object",
                    "description": "响应信息主体",
                    "properties": {
                        "code": {"type": "integer", "format": "int32", "description": "消息状态码"},
                        "data": {
                            "$ref": "#/components/schemas/LoginVo",
                            "description": "数据对象"
                        }
                    }
                },
                "TenantListVo": {
                    "type": "object",
                    "description": "租户列表",
                    "properties": {
                        "tenantId": {"type": "string", "description": "租户编号"}
                    }
                },
                "LoginTenantVo": {
                    "type": "object",
                    "description": "登录租户对象",
                    "properties": {
                        "voList": {
                            "type": "array",
                            "description": "租户对象列表",
                            "items": {"$ref": "#/components/schemas/TenantListVo"}
                        }
                    }
                },
                "RVoid": {
                    "type": "object",
                    "description": "响应信息主体",
                    "properties": {
                        "code": {"type": "integer", "format": "int32", "description": "消息状态码"}
                    }
                },
                "RString": {
                    "allOf": [
                        {"$ref": "#/components/schemas/RVoid"},
                        {
                            "type": "object",
                            "properties": {
                                "data": {
                                    "anyOf": [
                                        {"type": "string"},
                                        {"$ref": "#/components/schemas/LoginVo"}
                                    ]
                                }
                            }
                        }
                    ]
                },
                "ChoiceType": {
                    "oneOf": [
                        {"type": "string"},
                        {"type": "integer"}
                    ]
                }
            }
        }
    }

    fixture_file = tmp_path / "springdoc.json"
    fixture_file.write_text(json.dumps(spec), encoding="utf-8")
    return fixture_file


class TestSpringdocSupport:
    """测试 springdoc OpenAPI 3.1 支持"""

    @pytest.mark.unit
    def test_parser_loads_springdoc_request_body_and_content(self, springdoc_fixture_file):
        from swagger_mcp.parser import SwaggerParser

        parser = SwaggerParser()
        doc = parser.load_from_file(str(springdoc_fixture_file))

        assert doc.info.title == "标题：RuoYi-Cloud-Plus微服务权限管理系统_接口文档"

        register_api = next(api for api in doc.apis if api.path == "/auth/register" and api.method == "POST")
        assert register_api.request_body is not None
        assert register_api.request_body.required is True
        assert register_api.request_body.content_type == "application/json"
        assert register_api.request_body.schema == {"$ref": "#/components/schemas/RegisterBody"}
        assert register_api.responses[0].content is not None
        assert register_api.responses[0].content["*/*"]["schema"]["$ref"] == "#/components/schemas/RVoid"

        binding_api = next(api for api in doc.apis if api.path == "/auth/binding/{source}" and api.method == "GET")
        source_param = next(param for param in binding_api.parameters if param.name == "source")
        assert source_param.schema == {"type": "string"}
        assert source_param.type == "string"

        unlock_api = next(api for api in doc.apis if api.path == "/auth/unlock/{socialId}" and api.method == "DELETE")
        social_id_param = unlock_api.parameters[0]
        assert social_id_param.schema == {"type": "integer", "format": "int64"}
        assert social_id_param.type == "integer"

    @pytest.mark.unit
    def test_server_returns_springdoc_request_body_and_schema_fields(self, springdoc_fixture_file):
        from swagger_mcp.server import get_api_details, get_schema_details
        from swagger_mcp.parser import parser

        original_document = parser.current_document
        try:
            parser.load_from_file(str(springdoc_fixture_file))

            api_details = get_api_details("/auth/login", "POST")
            assert api_details["success"] is True
            assert api_details["api"]["request_body"]["description"] == "登录信息"
            assert api_details["api"]["request_body"]["content"]["application/json"]["schema"]["type"] == "string"
            assert api_details["api"]["responses"][0]["content"]["*/*"]["schema"]["$ref"] == "#/components/schemas/RLoginVo"

            binding_details = get_api_details("/auth/binding/{source}", "GET")
            source_param = next(param for param in binding_details["api"]["parameters"] if param["name"] == "source")
            assert source_param["schema"] == {"type": "string"}

            schema_details = get_schema_details("RLoginVo")
            data_prop = next(prop for prop in schema_details["schema"]["properties"] if prop["name"] == "data")
            assert data_prop["ref"] == "#/components/schemas/LoginVo"

            composed_schema = get_schema_details("RString")
            assert composed_schema["schema"]["all_of"] is not None

            choice_schema = get_schema_details("ChoiceType")
            assert choice_schema["schema"]["one_of"] is not None
        finally:
            parser.current_document = original_document


class MockResponse:
    def __init__(self, payload, content_type="application/json"):
        self._payload = payload
        self.headers = {"content-type": content_type}
        self.text = json.dumps(payload, ensure_ascii=False)

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


class TestSwaggerConfigSupport:
    """测试 swagger-config 多服务加载"""

    @pytest.fixture
    def swagger_config_payload(self):
        return {
            "configUrl": "/v3/api-docs/swagger-config",
            "oauth2RedirectUrl": "http://127.0.0.1:8080/swagger-ui/oauth2-redirect.html",
            "urls": [
                {"url": "/system/v3/api-docs", "name": "系统服务"},
                {"url": "/auth/v3/api-docs", "name": "认证服务"},
                {"url": "/facility/v3/api-docs", "name": "设施服务"},
                {"url": "/resource/v3/api-docs", "name": "资源服务"}
            ],
            "urls.primaryName": "认证服务",
            "validatorUrl": ""
        }

    @pytest.fixture
    def auth_service_payload(self):
        return {
            "openapi": "3.0.1",
            "info": {
                "title": "认证服务 API",
                "version": "1.0.0",
                "description": "认证服务文档"
            },
            "servers": [{"url": "http://127.0.0.1:8080"}],
            "paths": {
                "/auth/login": {
                    "post": {
                        "summary": "登录",
                        "responses": {
                            "200": {
                                "description": "OK"
                            }
                        }
                    }
                }
            },
            "components": {
                "schemas": {
                    "LoginRequest": {
                        "type": "object",
                        "properties": {
                            "username": {"type": "string"}
                        }
                    }
                }
            }
        }

    @pytest.mark.unit
    def test_load_swagger_config_and_list_services(self, monkeypatch, swagger_config_payload):
        from swagger_mcp.server import load_swagger, list_swagger_services
        from swagger_mcp.parser import parser

        original_document = parser.current_document
        original_config = parser.current_swagger_config

        def mock_get(url, timeout):
            assert url == "http://127.0.0.1:8080/v3/api-docs/swagger-config"
            assert timeout == 30
            return MockResponse(swagger_config_payload)

        monkeypatch.setattr("swagger_mcp.parser.requests.get", mock_get)

        try:
            result = load_swagger("http://127.0.0.1:8080/v3/api-docs/swagger-config")
            assert result["success"] is True
            assert result["primary_name"] == "认证服务"
            assert len(result["services"]) == 4
            assert parser.current_document == original_document

            services = list_swagger_services()
            assert services["success"] is True
            auth_service = next(item for item in services["services"] if item["name"] == "认证服务")
            assert auth_service["url"] == "/auth/v3/api-docs"
            assert auth_service["document_url"] == "http://127.0.0.1:8080/auth/v3/api-docs"
        finally:
            parser.current_document = original_document
            parser.current_swagger_config = original_config

    @pytest.mark.unit
    def test_load_swagger_service_by_name(self, monkeypatch, swagger_config_payload, auth_service_payload):
        from swagger_mcp.server import load_swagger, load_swagger_service, get_swagger_info
        from swagger_mcp.parser import parser

        original_document = parser.current_document
        original_config = parser.current_swagger_config

        def mock_get(url, timeout):
            assert timeout == 30
            if url == "http://127.0.0.1:8080/v3/api-docs/swagger-config":
                return MockResponse(swagger_config_payload)
            if url == "http://127.0.0.1:8080/auth/v3/api-docs":
                return MockResponse(auth_service_payload)
            raise AssertionError(f"Unexpected URL: {url}")

        monkeypatch.setattr("swagger_mcp.parser.requests.get", mock_get)

        try:
            config_result = load_swagger("http://127.0.0.1:8080/v3/api-docs/swagger-config")
            assert config_result["success"] is True

            service_result = load_swagger_service("认证服务")
            assert service_result["success"] is True
            assert service_result["info"]["title"] == "认证服务 API"

            info_result = get_swagger_info()
            assert info_result["success"] is True
            assert info_result["info"]["title"] == "认证服务 API"
            assert info_result["info"]["api_count"] == 1
        finally:
            parser.current_document = original_document
            parser.current_swagger_config = original_config

    @pytest.mark.unit
    def test_swagger_service_tools_fail_without_config(self):
        from swagger_mcp.server import list_swagger_services, load_swagger_service
        from swagger_mcp.parser import parser

        original_document = parser.current_document
        original_config = parser.current_swagger_config
        parser.current_document = None
        parser.current_swagger_config = None

        try:
            services = list_swagger_services()
            assert services["success"] is False

            load_result = load_swagger_service("认证服务")
            assert load_result["success"] is False
            assert "No Swagger config loaded" in load_result["error"]
        finally:
            parser.current_document = original_document
            parser.current_swagger_config = original_config

    @pytest.mark.unit
    def test_load_swagger_service_returns_error_for_unknown_service(self, monkeypatch, swagger_config_payload):
        from swagger_mcp.server import load_swagger, load_swagger_service
        from swagger_mcp.parser import parser

        original_document = parser.current_document
        original_config = parser.current_swagger_config

        def mock_get(url, timeout):
            assert url == "http://127.0.0.1:8080/v3/api-docs/swagger-config"
            assert timeout == 30
            return MockResponse(swagger_config_payload)

        monkeypatch.setattr("swagger_mcp.parser.requests.get", mock_get)

        try:
            load_swagger("http://127.0.0.1:8080/v3/api-docs/swagger-config")
            result = load_swagger_service("不存在的服务")
            assert result["success"] is False
            assert "Swagger service not found" in result["error"]
        finally:
            parser.current_document = original_document
            parser.current_swagger_config = original_config

    @pytest.mark.unit
    def test_load_swagger_keeps_normal_url_behavior(self, monkeypatch, auth_service_payload):
        from swagger_mcp.server import load_swagger
        from swagger_mcp.parser import parser

        original_document = parser.current_document
        original_config = parser.current_swagger_config

        def mock_get(url, timeout):
            assert url == "http://127.0.0.1:8080/auth/v3/api-docs"
            assert timeout == 30
            return MockResponse(auth_service_payload)

        monkeypatch.setattr("swagger_mcp.parser.requests.get", mock_get)

        try:
            result = load_swagger("http://127.0.0.1:8080/auth/v3/api-docs")
            assert result["success"] is True
            assert result["info"]["title"] == "认证服务 API"
            assert parser.current_document is not None
            assert parser.current_document.info.title == "认证服务 API"
        finally:
            parser.current_document = original_document
            parser.current_swagger_config = original_config
