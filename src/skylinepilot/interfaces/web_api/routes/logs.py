"""
日志路由模块
"""
from typing import Optional

from fastapi import APIRouter

from log_manager import log_manager

router = APIRouter()


@router.get("/api/logs")
async def get_logs(limit: int = 100, account: Optional[str] = None, action: Optional[str] = None):
    """获取操作日志"""
    logs = log_manager.get_logs(limit=limit, account=account, action=action)
    return {"success": True, "logs": logs, "total": len(logs)}


@router.get("/api/logs/stats")
async def get_log_stats():
    """获取日志统计"""
    stats = log_manager.get_stats()
    return {"success": True, "stats": stats}


@router.post("/api/logs/clear")
async def clear_logs():
    """清空日志"""
    log_manager.clear_logs()
    return {"success": True, "message": "日志已清空"}

