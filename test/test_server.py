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
