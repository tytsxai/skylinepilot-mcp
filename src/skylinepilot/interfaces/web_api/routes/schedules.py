"""
定时任务路由模块
"""
from typing import Optional

from fastapi import APIRouter, HTTPException

from log_manager import log_manager
from scheduler import task_scheduler
from src.skylinepilot.interfaces.web_api.response import ok_response

router = APIRouter()


@router.get("/api/schedules")
async def list_schedules():
    """获取定时任务列表"""
    schedules = task_scheduler.list_schedules()
    return {"success": True, "schedules": schedules, "total": len(schedules)}


@router.post("/api/schedules")
async def add_schedule(request: dict):
    """添加定时任务"""
    schedule_id = request.get("schedule_id")
    name = request.get("name")
    action = request.get("action")
    message = request.get("message")
    enabled = request.get("enabled", True)

    execute_time = request.get("execute_time")
    repeat = request.get("repeat", "once")
    account_id = request.get("account_id")
    friend_ids = request.get("friend_ids", [])
    stranger_usernames = request.get("stranger_usernames", [])
    interval = request.get("interval", 2000)
    auto_dedup = request.get("auto_dedup", True)
    validate_usernames = request.get("validate_usernames", True)

    cron = request.get("cron")
    target = request.get("target")
    template_id = request.get("template_id")
    account_ids = request.get("account_ids")

    if not schedule_id or not name:
        raise HTTPException(status_code=400, detail="缺少必要参数")

    if execute_time and not cron:
        hour = execute_time.get("hour", 0)
        minute = execute_time.get("minute", 0)
        day = execute_time.get("day", "*")
        month = execute_time.get("month", "*")
        if repeat == "once":
            cron = f"{minute} {hour} {day} {month} *"
        elif repeat == "daily":
            cron = f"{minute} {hour} * * *"
        elif repeat == "weekly":
            cron = f"{minute} {hour} * * 1"
        elif repeat == "workday":
            cron = f"{minute} {hour} * * 1-5"
        else:
            cron = f"{minute} {hour} * * *"

    if not target:
        target = "custom" if (friend_ids or stranger_usernames) else "all"

    success = task_scheduler.add_schedule(
        schedule_id=schedule_id,
        name=name,
        cron=cron or "0 9 * * *",
        action=action or "send_message",
        target=target,
        template_id=template_id,
        message=message,
        account_ids=account_ids or ([account_id] if account_id else []),
        enabled=enabled,
        execute_time=execute_time,
        repeat=repeat,
        friend_ids=friend_ids,
        stranger_usernames=stranger_usernames,
        interval=interval,
        auto_dedup=auto_dedup,
        validate_usernames=validate_usernames,
    )
    if not success:
        raise HTTPException(status_code=400, detail="任务添加失败")

    log_manager.add_log("定时任务", schedule_id, f"添加定时任务: {name}", "success")
    return {"success": True, "message": "定时任务添加成功"}


@router.delete("/api/schedules/{schedule_id}")
async def delete_schedule(schedule_id: str):
    """删除定时任务"""
    success = task_scheduler.delete_schedule(schedule_id)
    if not success:
        raise HTTPException(status_code=404, detail="定时任务不存在")

    log_manager.add_log("定时任务", schedule_id, "删除定时任务", "warning")
    return {"success": True, "message": "定时任务已删除"}


@router.post("/api/schedules/{schedule_id}/toggle")
async def toggle_schedule(schedule_id: str):
    """切换定时任务状态"""
    success = task_scheduler.toggle_schedule(schedule_id)
    if not success:
        raise HTTPException(status_code=404, detail="定时任务不存在")

    schedule = task_scheduler.schedules.get(schedule_id, {})
    status = "启用" if schedule.get("enabled", False) else "禁用"
    log_manager.add_log("定时任务", schedule_id, f"{status}定时任务", "info")
    return {"success": True, "message": "状态已更新", "enabled": schedule.get("enabled", False)}


@router.get("/api/schedules/{schedule_id}/next-run")
async def get_next_run(schedule_id: str):
    """获取下次执行时间"""
    next_run = task_scheduler.get_next_run(schedule_id)
    if not next_run:
        raise HTTPException(status_code=404, detail="定时任务不存在")
    return {"success": True, "schedule_id": schedule_id, "next_run": next_run}


@router.get("/api/workspace/schedules")
async def workspace_list_schedules():
    """品牌化别名：任务列表"""
    schedules = task_scheduler.list_schedules()
    return ok_response({"schedules": schedules, "total": len(schedules)})

