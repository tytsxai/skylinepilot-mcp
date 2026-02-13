"""
统计路由模块
"""
from typing import Optional

from fastapi import APIRouter

from stats_tracker import stats_tracker

router = APIRouter()


@router.get("/api/stats/summary")
async def get_stats_summary():
    """获取统计摘要"""
    summary = stats_tracker.get_summary()
    return {"success": True, "summary": summary}


@router.get("/api/stats/account/{account_id}")
async def get_account_stats(account_id: str):
    """获取账号统计"""
    stats = stats_tracker.get_account_stats(account_id)
    return {"success": True, "account_id": account_id, "stats": stats}


@router.get("/api/stats/daily")
async def get_daily_stats(date: Optional[str] = None):
    """获取每日统计"""
    stats = stats_tracker.get_daily_stats(date)
    return {"success": True, "date": date or "today", "stats": stats}


@router.get("/api/stats/weekly")
async def get_weekly_stats(week: Optional[str] = None):
    """获取每周统计"""
    stats = stats_tracker.get_weekly_stats(week)
    return {"success": True, "week": week or "current", "stats": stats}


@router.get("/api/stats/top")
async def get_top_accounts(by: str = "uses", limit: int = 10, period: str = "all"):
    """获取最活跃账号"""
    result = stats_tracker.get_top_accounts(by, limit, period)
    return {"success": True, "top_accounts": result}


@router.get("/api/stats/trend/{account_id}")
async def get_activity_trend(account_id: str, days: int = 7):
    """获取活跃度趋势"""
    trend = stats_tracker.get_activity_trend(account_id, days)
    return {"success": True, "account_id": account_id, "trend": trend}

