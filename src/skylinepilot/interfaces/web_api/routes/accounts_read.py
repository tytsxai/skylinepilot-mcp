"""
账号查询路由（只读）
"""
from fastapi import APIRouter, HTTPException

from src.skylinepilot.core.accounts.service import accounts_service
from src.skylinepilot.interfaces.web_api.response import ok_response

router = APIRouter()


@router.get("/api/accounts")
async def list_accounts():
    """获取所有账号列表"""
    try:
        accounts = accounts_service.list_accounts()
        return {"success": True, "accounts": accounts, "total": len(accounts)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/accounts/{account_id}/qr-status")
async def get_qr_status(account_id: str):
    """获取二维码登录状态"""
    return accounts_service.get_qr_status(account_id)


@router.get("/api/accounts/{account_id}/export-session")
async def export_session(account_id: str):
    """导出Session"""
    session = accounts_service.export_session(account_id)
    if session:
        return {
            "success": True,
            "account_id": account_id,
            "session_string": session
        }
    raise HTTPException(status_code=404, detail="账号不存在")


@router.get("/api/accounts/{account_id}/friends")
async def get_account_friends(account_id: str):
    """获取账号的好友列表"""
    try:
        friends = await accounts_service.list_friends(account_id)
        return {"success": True, "friends": friends, "total": len(friends)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/accounts/{account_id}/phone-status")
async def get_phone_login_status(account_id: str):
    """获取手机号登录状态"""
    return accounts_service.get_phone_login_status(account_id)


@router.get("/api/workspace/accounts")
async def workspace_list_accounts():
    """品牌化别名：获取账号列表"""
    accounts = accounts_service.list_accounts()
    return ok_response({"accounts": accounts, "total": len(accounts)})

