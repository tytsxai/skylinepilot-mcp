"""
健康监控路由模块
"""
from typing import Optional

from fastapi import APIRouter

from health_monitor import health_monitor
from src.skylinepilot.interfaces.web_api.response import ok_response

router = APIRouter()


@router.get("/api/health/report")
async def get_health_report(account_id: Optional[str] = None):
    """获取健康报告"""
    report = health_monitor.get_health_report(account_id)
    return {"success": True, "report": report}


@router.post("/api/health/check/{account_id}")
async def check_account_health(account_id: str):
    """检查账号健康状态"""
    result = await health_monitor.check_account_health(account_id)
    return {"success": True, "result": result}


@router.get("/api/health/risk-accounts")
async def get_risk_accounts():
    """获取高风险账号"""
    accounts = health_monitor.get_risk_accounts()
    return {"success": True, "risk_accounts": accounts, "total": len(accounts)}


@router.get("/api/workspace/health/report")
async def workspace_health_report(account_id: Optional[str] = None):
    """品牌化别名：健康报告"""
    report = health_monitor.get_health_report(account_id)
    return ok_response({"report": report})

