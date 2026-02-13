"""
批量操作路由模块
"""
from fastapi import APIRouter, HTTPException

from batch_operations import batch_operations

router = APIRouter()


@router.post("/api/batch/send-message")
async def batch_send_message_api(request: dict):
    """批量发送消息"""
    chat_id = request.get("chat_id")
    message = request.get("message")
    account_ids = request.get("account_ids")
    delay = request.get("delay", 2.0)
    if not chat_id or not message:
        raise HTTPException(status_code=400, detail="缺少必要参数")

    return await batch_operations.batch_send_message(
        chat_id=chat_id,
        message=message,
        account_ids=account_ids,
        delay=delay,
    )


@router.post("/api/batch/send-template")
async def batch_send_template_api(request: dict):
    """批量发送模板消息"""
    chat_id = request.get("chat_id")
    template_id = request.get("template_id")
    account_ids = request.get("account_ids")
    template_vars = request.get("template_vars", {})
    delay = request.get("delay", 2.0)
    if not chat_id or not template_id:
        raise HTTPException(status_code=400, detail="缺少必要参数")

    return await batch_operations.batch_send_template(
        chat_id=chat_id,
        template_id=template_id,
        account_ids=account_ids,
        template_vars=template_vars,
        delay=delay,
    )


@router.post("/api/batch/check-health")
async def batch_check_health_api(request: dict):
    """批量检查账号健康状态"""
    account_ids = request.get("account_ids")
    return await batch_operations.batch_check_health(account_ids)


@router.post("/api/batch/export-sessions")
async def batch_export_sessions_api(request: dict):
    """批量导出Session"""
    account_ids = request.get("account_ids")
    return await batch_operations.batch_export_sessions(account_ids)


@router.post("/api/batch/delete-accounts")
async def batch_delete_accounts_api(request: dict):
    """批量删除账号"""
    account_ids = request.get("account_ids")
    if not account_ids:
        raise HTTPException(status_code=400, detail="缺少账号ID列表")
    return await batch_operations.batch_delete_accounts(account_ids)


@router.post("/api/batch/get-dialogs")
async def batch_get_dialogs_api(request: dict):
    """批量获取对话列表"""
    account_ids = request.get("account_ids")
    limit = request.get("limit", 20)
    return await batch_operations.batch_get_dialogs(account_ids=account_ids, limit=limit)

