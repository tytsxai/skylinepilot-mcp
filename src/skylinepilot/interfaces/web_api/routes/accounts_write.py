"""
账号写操作路由
"""
from fastapi import APIRouter, HTTPException

from account_manager import account_manager
from log_manager import log_manager
from proxy_manager import proxy_manager
from stats_tracker import stats_tracker
from src.skylinepilot.interfaces.web_api.response import ok_response

router = APIRouter()


@router.post("/api/accounts/generate-qr")
async def generate_qr_code(request: dict):
    """生成二维码"""
    account_id = request.get("account_id")
    proxy_id = request.get("proxy_id")

    if not account_id:
        raise HTTPException(status_code=400, detail="缺少 account_id")

    stats_tracker.record_use(account_id)
    proxy = proxy_manager.get_proxy(proxy_id) if proxy_id else proxy_manager.get_proxy_for_account(account_id)
    return await account_manager.generate_qr_code(account_id, proxy)


@router.post("/api/accounts/{account_id}/refresh-qr")
async def refresh_qr_code(account_id: str):
    """刷新二维码"""
    proxy = proxy_manager.get_proxy_for_account(account_id)
    return await account_manager.refresh_qr_code(account_id, proxy)


@router.post("/api/accounts/{account_id}/2fa-password")
async def submit_2fa_password(account_id: str, request: dict):
    """提交两步验证密码"""
    password = request.get("password")
    if not password:
        raise HTTPException(status_code=400, detail="缺少密码")

    stats_tracker.record_use(account_id)
    return await account_manager.submit_2fa_password(account_id, password)


@router.delete("/api/accounts/{account_id}")
async def delete_account(account_id: str):
    """删除账号"""
    if account_id == "default":
        raise HTTPException(status_code=400, detail="无法删除默认账号")

    success = await account_manager.remove_account(account_id)
    if not success:
        raise HTTPException(status_code=404, detail="账号不存在")

    log_manager.add_log("账号管理", account_id, "删除账号", "warning")
    return {"success": True, "message": "账号已删除"}


@router.post("/api/accounts/add-session")
async def add_account_with_session(request: dict):
    """使用Session添加账号"""
    account_id = request.get("account_id")
    session_string = request.get("session_string")
    phone = request.get("phone")
    username = request.get("username")

    if not account_id or not session_string:
        raise HTTPException(status_code=400, detail="缺少必要参数")

    success = await account_manager.add_account_with_session(account_id, session_string, phone, username)
    if not success:
        raise HTTPException(status_code=400, detail="添加失败")

    stats_tracker.record_use(account_id)
    log_manager.add_log("账号管理", account_id, "添加账号", "success")
    return {"success": True, "message": "账号添加成功"}


@router.post("/api/accounts/batch-import")
async def batch_import(request: dict):
    """批量导入账号"""
    accounts = request.get("accounts", [])
    return await account_manager.batch_import(accounts)


@router.post("/api/accounts/validate-usernames")
async def validate_usernames(request: dict):
    """验证用户名是否有效"""
    account_id = request.get("account_id")
    usernames = request.get("usernames", [])
    if not account_id or not usernames:
        raise HTTPException(status_code=400, detail="缺少参数")

    try:
        results = await account_manager.validate_usernames(account_id, usernames)
        return {"success": True, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/accounts/send-code")
async def send_phone_code(request: dict):
    """发送验证码到手机号"""
    account_id = request.get("account_id")
    phone = request.get("phone")
    proxy_id = request.get("proxy_id")

    if not account_id or not phone:
        raise HTTPException(status_code=400, detail="缺少必要参数")

    proxy = proxy_manager.get_proxy(proxy_id) if proxy_id else proxy_manager.get_proxy_for_account(account_id)
    result = await account_manager.send_phone_code(account_id, phone, proxy)
    if result.get("success"):
        log_manager.add_log("账号管理", account_id, f"发送验证码到 {phone}", "info")
    return result


@router.post("/api/accounts/verify-code")
async def verify_phone_code(request: dict):
    """验证手机验证码"""
    account_id = request.get("account_id")
    code = request.get("code")
    if not account_id or not code:
        raise HTTPException(status_code=400, detail="缺少必要参数")

    result = await account_manager.verify_phone_code(account_id, code)
    if result.get("success"):
        stats_tracker.record_use(account_id)
        log_manager.add_log("账号管理", account_id, "手机号登录成功", "success")
    return result


@router.post("/api/accounts/{account_id}/phone-2fa")
async def submit_phone_2fa(account_id: str, request: dict):
    """提交手机号登录的 2FA 密码"""
    password = request.get("password")
    if not password:
        raise HTTPException(status_code=400, detail="缺少密码")

    result = await account_manager.submit_2fa_for_phone(account_id, password)
    if result.get("success"):
        stats_tracker.record_use(account_id)
        log_manager.add_log("账号管理", account_id, "手机号登录成功(2FA)", "success")
    return result


@router.delete("/api/accounts/{account_id}/phone-login")
async def cancel_phone_login(account_id: str):
    """取消手机号登录"""
    success = await account_manager.cancel_phone_login(account_id)
    if not success:
        raise HTTPException(status_code=404, detail="会话不存在")
    return {"success": True, "message": "已取消"}


@router.post("/api/workspace/accounts/generate-qr")
async def workspace_generate_qr(request: dict):
    """品牌化别名：生成二维码"""
    account_id = request.get("account_id")
    proxy_id = request.get("proxy_id")
    if not account_id:
        raise HTTPException(status_code=400, detail="缺少 account_id")

    stats_tracker.record_use(account_id)
    proxy = proxy_manager.get_proxy(proxy_id) if proxy_id else proxy_manager.get_proxy_for_account(account_id)
    result = await account_manager.generate_qr_code(account_id, proxy)
    return ok_response(result)


@router.post("/api/workspace/accounts/add-session")
async def workspace_add_session(request: dict):
    """品牌化别名：Session 添加账号"""
    account_id = request.get("account_id")
    session_string = request.get("session_string")
    phone = request.get("phone")
    username = request.get("username")
    if not account_id or not session_string:
        raise HTTPException(status_code=400, detail="缺少必要参数")

    success = await account_manager.add_account_with_session(account_id, session_string, phone, username)
    if not success:
        raise HTTPException(status_code=400, detail="添加失败")

    stats_tracker.record_use(account_id)
    log_manager.add_log("账号管理", account_id, "添加账号(品牌化API)", "success")
    return ok_response({"message": "账号添加成功", "account_id": account_id})

