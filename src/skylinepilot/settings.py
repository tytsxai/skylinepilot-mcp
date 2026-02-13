"""
SkylinePilot 全局配置
"""
import os
from dataclasses import dataclass


@dataclass
class Settings:
    app_name: str = os.getenv("APP_NAME", "SkylinePilot MCP")
    app_env: str = os.getenv("APP_ENV", "production")
    dashboard_port: int = int(os.getenv("DASHBOARD_PORT", "8080"))
    mcp_server_name: str = os.getenv("MCP_SERVER_NAME", "skylinepilot-core")
    session_file: str = os.getenv("SESSION_FILE", ".telegram_session")


settings = Settings()

