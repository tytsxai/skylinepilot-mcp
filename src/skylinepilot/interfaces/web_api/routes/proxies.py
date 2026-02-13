"""
代理路由模块
"""
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from log_manager import log_manager
from proxy_manager import proxy_manager
from src.skylinepilot.interfaces.web_api.response import ok_response

router = APIRouter()


class AddProxyRequest(BaseModel):
    proxy_id: str
    protocol: str
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None


class SetGlobalProxyRequest(BaseModel):
    protocol: str
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None


class AssignProxyRequest(BaseModel):
    account_id: str
    proxy_id: str


@router.get("/api/proxies")
async def list_proxies():
    """获取所有代理"""
    proxies = proxy_manager.list_proxies()
    return {"success": True, **proxies}


@router.post("/api/proxies/add")
async def add_proxy(request: AddProxyRequest):
    """添加代理"""
    success = proxy_manager.add_proxy(
        request.proxy_id,
        request.protocol,
        request.host,
        request.port,
        request.username,
        request.password,
    )
    if not success:
        raise HTTPException(status_code=400, detail="代理协议不支持")

    log_manager.add_log("代理管理", request.proxy_id, f"添加代理 {request.protocol}://{request.host}:{request.port}", "success")
    return {"success": True, "message": "代理添加成功"}


@router.delete("/api/proxies/{proxy_id}")
async def delete_proxy(proxy_id: str):
    """删除代理"""
    success = proxy_manager.delete_proxy(proxy_id)
    if not success:
        raise HTTPException(status_code=404, detail="代理不存在")

    log_manager.add_log("代理管理", proxy_id, "删除代理", "warning")
    return {"success": True, "message": "代理已删除"}


@router.post("/api/proxies/set-global")
async def set_global_proxy(request: SetGlobalProxyRequest):
    """设置全局代理"""
    success = proxy_manager.set_global_proxy(
        request.protocol,
        request.host,
        request.port,
        request.username,
        request.password,
    )
    if not success:
        raise HTTPException(status_code=400, detail="代理协议不支持")

    log_manager.add_log("代理管理", "global", f"设置全局代理 {request.protocol}://{request.host}:{request.port}", "success")
    return {"success": True, "message": "全局代理设置成功"}


@router.delete("/api/proxies/global")
async def remove_global_proxy():
    """移除全局代理"""
    proxy_manager.remove_global_proxy()
    log_manager.add_log("代理管理", "global", "移除全局代理", "warning")
    return {"success": True, "message": "全局代理已移除"}


@router.post("/api/proxies/assign")
async def assign_proxy(request: AssignProxyRequest):
    """分配代理给账号"""
    success = proxy_manager.assign_proxy_to_account(request.account_id, request.proxy_id)
    if not success:
        raise HTTPException(status_code=404, detail="代理不存在")

    log_manager.add_log("代理管理", request.account_id, f"分配代理 {request.proxy_id}", "success")
    return {"success": True, "message": "代理分配成功"}


@router.delete("/api/proxies/{proxy_id}/accounts/{account_id}")
async def unassign_proxy(proxy_id: str, account_id: str):
    """取消代理分配"""
    success = proxy_manager.unassign_proxy_from_account(account_id, proxy_id)
    if not success:
        raise HTTPException(status_code=404, detail="未找到该分配关系")
    return {"success": True, "message": "代理分配已取消"}


@router.post("/api/proxies/test")
async def test_proxy(request: dict):
    """测试代理连通性"""
    proxy_id = request.get("proxy_id")
    test_all = request.get("test_all", False)

    if test_all:
        result = await proxy_manager.test_all_proxies()
        return {"success": True, "results": result}

    if not proxy_id:
        raise HTTPException(status_code=400, detail="缺少proxy_id")
    if proxy_id not in proxy_manager.proxies:
        raise HTTPException(status_code=404, detail="代理不存在")

    result = await proxy_manager.test_proxy(proxy_manager.proxies[proxy_id])
    return {"success": True, "result": result}


@router.get("/api/workspace/proxies")
async def workspace_list_proxies():
    """品牌化别名：代理列表"""
    proxies = proxy_manager.list_proxies()
    return ok_response(proxies)

