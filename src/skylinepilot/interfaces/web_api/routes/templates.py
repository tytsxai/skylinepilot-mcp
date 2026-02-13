"""
模板路由模块
"""
from typing import Optional

from fastapi import APIRouter, HTTPException

from log_manager import log_manager
from src.skylinepilot.core.templates.service import templates_service
from src.skylinepilot.interfaces.web_api.response import ok_response

router = APIRouter()


@router.get("/api/templates")
async def list_templates(category: Optional[str] = None):
    """获取消息模板列表"""
    templates = templates_service.list_templates(category=category)
    return {"success": True, "templates": templates, "total": len(templates)}


@router.post("/api/templates")
async def add_template(request: dict):
    """添加消息模板"""
    try:
        success, template_id, name = templates_service.add_template(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if success:
        log_manager.add_log("模板管理", template_id, f"添加模板: {name}", "success")
        return {"success": True, "message": "模板添加成功"}
    raise HTTPException(status_code=400, detail="模板ID已存在")


@router.delete("/api/templates/{template_id}")
async def delete_template(template_id: str):
    """删除模板"""
    success = templates_service.delete_template(template_id)
    if success:
        log_manager.add_log("模板管理", template_id, "删除模板", "warning")
        return {"success": True, "message": "模板已删除"}
    raise HTTPException(status_code=404, detail="模板不存在")


@router.get("/api/templates/{template_id}/preview")
async def preview_template(template_id: str, vars: Optional[str] = None):
    """预览模板渲染结果"""
    try:
        rendered = templates_service.preview_template(template_id, vars)
        return {"success": True, "template_id": template_id, "rendered": rendered}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/api/workspace/templates")
async def workspace_list_templates(category: Optional[str] = None):
    """品牌化别名：模板列表"""
    templates = templates_service.list_templates(category=category)
    return ok_response({"templates": templates, "total": len(templates)})

