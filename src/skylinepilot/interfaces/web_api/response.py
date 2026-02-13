"""
Web API 响应封装
"""
from typing import Any, Dict, Optional


def ok_response(data: Any) -> Dict[str, Any]:
    """统一成功响应结构"""
    return {"ok": True, "data": data, "error": None}


def error_response(message: str, code: str = "BAD_REQUEST", details: Optional[Any] = None) -> Dict[str, Any]:
    """统一失败响应结构（供渐进迁移使用）"""
    return {
        "ok": False,
        "data": None,
        "error": {
            "code": code,
            "message": message,
            "details": details,
        },
    }
