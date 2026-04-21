"""
OpenAPI/Swagger document parser
Supports OpenAPI 3.0 and Swagger 2.0 specifications
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any

import requests
import yaml
from openapi_spec_validator.readers import read_from_filename

from swagger_mcp.models import (
    SwaggerDocument, SwaggerInfo, ApiEndpoint, Schema,
    Parameter, Response, RequestBody, SchemaProperty
)


class SwaggerParser:
    """OpenAPI/Swagger文档解析器
    
    支持解析以下格式：
    - OpenAPI 3.0 (JSON/YAML)
    - Swagger 2.0 (JSON/YAML)
    """
    
    def __init__(self):
        self.current_document: Optional[SwaggerDocument] = None
    
    def load_from_url(self, url: str) -> SwaggerDocument:
        """从URL加载OpenAPI/Swagger文档"""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            content_type = response.headers.get('content-type', '')
            if 'application/json' in content_type:
                spec_dict = response.json()
            elif 'application/yaml' in content_type or 'text/yaml' in content_type:
                spec_dict = yaml.safe_load(response.text)
            else:
                # 尝试JSON，如果失败则尝试YAML
                try:
                    spec_dict = response.json()
                except json.JSONDecodeError:
                    spec_dict = yaml.safe_load(response.text)
            
            self.current_document = self._parse_spec(spec_dict)
            return self.current_document
            
        except requests.RequestException as e:
            raise ValueError(f"Failed to load Swagger document from URL: {e}")
        except (json.JSONDecodeError, yaml.YAMLError) as e:
            raise ValueError(f"Failed to parse Swagger document: {e}")
    
    def load_from_file(self, file_path: str) -> SwaggerDocument:
        """从本地文件加载OpenAPI/Swagger文档"""
        try:
            path = Path(file_path)
            if not path.exists():
                raise FileNotFoundError(f"Swagger file not found: {file_path}")
            
            # 使用openapi-spec-validator读取和验证
            spec_dict, spec_url = read_from_filename(str(path))
            
            self.current_document = self._parse_spec(dict(spec_dict))  # type: ignore
            return self.current_document
            
        except Exception as e:
            raise ValueError(f"Failed to load Swagger document from file: {e}")
    
    def validate_spec(self, spec_dict: Dict[str, Any]) -> bool:
        """验证OpenAPI规范"""
        try:
            from openapi_spec_validator import validate_spec
            validate_spec(spec_dict)  # type: ignore
            return True
        except Exception:
            return False
    
    def _parse_spec(self, spec_dict: Dict[str, Any]) -> SwaggerDocument:
        """解析OpenAPI规范字典"""
        # 解析基本信息
        info_data = spec_dict.get('info', {})
        info = SwaggerInfo(
            title=info_data.get('title', 'Unknown API'),
            version=info_data.get('version', '1.0.0'),
            description=info_data.get('description'),
            contact=info_data.get('contact'),
            license=info_data.get('license')
        )
        
        # 解析服务器信息
        servers = spec_dict.get('servers', [])
        if not servers and 'host' in spec_dict:
            # Swagger 2.0 格式
            scheme = spec_dict.get('schemes', ['http'])[0]
            base_path = spec_dict.get('basePath', '')
            servers = [{'url': f"{scheme}://{spec_dict['host']}{base_path}"}]
        
        # 解析API端点
        apis = self._parse_paths(spec_dict.get('paths', {}))
        
        # 解析数据模型
        schemas = self._parse_schemas(spec_dict)
        
        # 解析安全定义
        security_definitions = spec_dict.get('securityDefinitions', {})
        if not security_definitions:
            security_definitions = spec_dict.get('components', {}).get('securitySchemes', {})
        
        return SwaggerDocument(
            info=info,
            apis=apis,
            schemas=schemas,
            servers=servers,
            security_definitions=security_definitions
        )
    
    def _parse_paths(self, paths: Dict[str, Any]) -> List[ApiEndpoint]:
        """解析API路径"""
        apis = []
        
        for path, path_item in paths.items():
            for method, operation in path_item.items():
                if method.lower() not in ['get', 'post', 'put', 'delete', 'patch', 'head', 'options']:
                    continue
                
                # 解析参数
                parameters = self._parse_parameters(
                    operation.get('parameters', []) + path_item.get('parameters', [])
                )
                request_body = self._parse_request_body(operation.get('requestBody'))
                
                # 解析响应
                responses = self._parse_responses(operation.get('responses', {}))
                
                api = ApiEndpoint(
                    path=path,
                    method=method.upper(),
                    operation_id=operation.get('operationId'),
                    summary=operation.get('summary'),
                    description=operation.get('description'),
                    tags=operation.get('tags', []),
                    parameters=parameters,
                    responses=responses,
                    request_body=request_body,
                    security=operation.get('security', []),
                    deprecated=operation.get('deprecated', False)
                )
                apis.append(api)
        
        return apis
    
    def _parse_parameters(self, params: List[Dict[str, Any]]) -> List[Parameter]:
        """解析参数"""
        parameters = []
        
        for param in params:
            param_type = param.get('type', 'string')
            schema = param.get('schema')
            if 'schema' in param:
                # OpenAPI 3.0 格式
                param_type = self._get_schema_type(schema)
            
            parameter = Parameter(
                name=param['name'],
                location=param.get('in', 'query'),
                type=param_type,
                required=param.get('required', False),
                description=param.get('description'),
                default=param.get('default'),
                example=param.get('example'),
                schema=schema,
                content_type=self._get_first_content_type(param.get('content'))
            )
            parameters.append(parameter)
        
        return parameters

    def _parse_request_body(self, request_body: Optional[Dict[str, Any]]) -> Optional[RequestBody]:
        """解析 OpenAPI 3 requestBody"""
        if not request_body:
            return None

        content = request_body.get('content')
        content_type = self._get_first_content_type(content)
        schema = self._get_first_schema_from_content(content)

        return RequestBody(
            description=request_body.get('description'),
            required=request_body.get('required', False),
            content_type=content_type,
            schema=schema,
            content=content
        )
    
    def _parse_responses(self, responses: Dict[str, Any]) -> List[Response]:
        """解析响应"""
        response_list = []
        
        for status_code, response_data in responses.items():
            content_type = None
            schema = None
            content = response_data.get('content')
            
            # OpenAPI 3.0 格式
            if content:
                content_type = self._get_first_content_type(content)
                schema = self._get_first_schema_from_content(content)
            # Swagger 2.0 格式
            elif 'schema' in response_data:
                schema = response_data['schema']
                content_type = 'application/json'
            
            response = Response(
                status_code=status_code,
                description=response_data.get('description', ''),
                content_type=content_type,
                schema=schema,
                content=content
            )
            response_list.append(response)
        
        return response_list
    
    def _parse_schemas(self, spec_dict: Dict[str, Any]) -> List[Schema]:
        """解析数据模型"""
        schemas = []
        
        # OpenAPI 3.0 格式
        components = spec_dict.get('components', {})
        schemas_dict = components.get('schemas', {})
        
        # Swagger 2.0 格式
        if not schemas_dict:
            schemas_dict = spec_dict.get('definitions', {})
        
        for name, schema_def in schemas_dict.items():
            schema = self._parse_single_schema(name, schema_def)
            schemas.append(schema)
        
        return schemas
    
    def _parse_single_schema(self, name: str, schema_def: Dict[str, Any]) -> Schema:
        """解析单个数据模型"""
        properties = []
        
        for prop_name, prop_def in schema_def.get('properties', {}).items():
            property_obj = SchemaProperty(
                name=prop_name,
                type=self._get_schema_type(prop_def),
                description=prop_def.get('description'),
                required=prop_name in schema_def.get('required', []),
                format=prop_def.get('format'),
                example=prop_def.get('example'),
                enum=prop_def.get('enum'),
                items=prop_def.get('items'),
                properties=prop_def.get('properties'),
                ref=prop_def.get('$ref'),
                all_of=prop_def.get('allOf'),
                one_of=prop_def.get('oneOf'),
                any_of=prop_def.get('anyOf')
            )
            properties.append(property_obj)
        
        return Schema(
            name=name,
            type=self._get_schema_type(schema_def),
            description=schema_def.get('description'),
            properties=properties,
            required=schema_def.get('required', []),
            example=schema_def.get('example'),
            items=schema_def.get('items'),
            ref=schema_def.get('$ref'),
            all_of=schema_def.get('allOf'),
            one_of=schema_def.get('oneOf'),
            any_of=schema_def.get('anyOf')
        )

    def _get_first_content_type(self, content: Optional[Dict[str, Any]]) -> Optional[str]:
        """获取 content 中的第一个 content type"""
        if not content:
            return None

        for content_type in content.keys():
            return content_type
        return None

    def _get_first_schema_from_content(self, content: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """获取 content 中第一个 schema"""
        if not content:
            return None

        for media_type in content.values():
            if isinstance(media_type, dict):
                schema = media_type.get('schema')
                if schema is not None:
                    return schema
        return None

    def _get_schema_type(self, schema: Optional[Dict[str, Any]]) -> str:
        """推断 schema 类型，兼容 OpenAPI 3 组合结构"""
        if not schema:
            return 'string'
        if 'type' in schema:
            return str(schema['type'])
        if '$ref' in schema:
            return 'ref'
        if 'allOf' in schema:
            return 'allOf'
        if 'oneOf' in schema:
            return 'oneOf'
        if 'anyOf' in schema:
            return 'anyOf'
        if 'properties' in schema:
            return 'object'
        if 'items' in schema:
            return 'array'
        return 'string'
    
    def get_apis_by_tag(self, tag: str) -> List[ApiEndpoint]:
        """根据标签获取API"""
        if not self.current_document:
            return []
        
        return [api for api in self.current_document.apis if tag in api.tags]
    
    def search_apis(self, query: str) -> List[ApiEndpoint]:
        """搜索API"""
        if not self.current_document:
            return []
        
        query_lower = query.lower()
        results = []
        
        for api in self.current_document.apis:
            if (query_lower in api.path.lower() or
                query_lower in api.method.lower() or
                (api.summary and query_lower in api.summary.lower()) or
                (api.description and query_lower in api.description.lower()) or
                any(query_lower in tag.lower() for tag in api.tags)):
                results.append(api)
        
        return results
    
    def get_schema_by_name(self, name: str) -> Optional[Schema]:
        """根据名称获取Schema"""
        if not self.current_document:
            return None
        
        for schema in self.current_document.schemas:
            if schema.name == name:
                return schema
        
        return None


# 创建全局解析器实例
parser = SwaggerParser()
