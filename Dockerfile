FROM python:3.12-slim
WORKDIR /app

COPY ./ /app/
RUN pip install --no-cache-dir -r requirements.txt
# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["sh", "-c", "FASTMCP_TRANSPORT=streamable-http FASTMCP_HOST=0.0.0.0 FASTMCP_PORT=8000 exec python swagger_mcp/server.py --swagger-uri http://192.168.46.36:8080/v3/api-docs/swagger-config"]
