"""
兼容入口：导出当前 dashboard FastAPI app
后续会将 dashboard.py 按模块迁移到 src/skylinepilot/interfaces/web_api/*
"""
from dashboard import app

__all__ = ["app"]

