"""
营销路由模块
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from log_manager import log_manager
from template_manager import template_manager
from src.skylinepilot.core.marketing.service import marketing_service
from src.skylinepilot.interfaces.web_api.response import ok_response

router = APIRouter()


class MarketingGenerateRequest(BaseModel):
    product_name: str
    audience: str
    goal: str
    tone: str = "professional"
    channel: str = "telegram_dm"
    offer: str = ""
    cta: str = "回复“1”领取详情"
    variants: int = 3


class MarketingScoreRequest(BaseModel):
    text: str


@router.get("/api/marketing/playbooks")
async def list_marketing_playbooks():
    """获取营销玩法库"""
    playbooks = marketing_service.list_playbooks()
    return ok_response({
        "playbooks": playbooks,
        "total": len(playbooks)
    })


@router.post("/api/marketing/generate")
async def generate_marketing_copy(request: MarketingGenerateRequest):
    """生成营销文案多版本"""
    copies = marketing_service.generate({
        "product_name": request.product_name,
        "audience": request.audience,
        "goal": request.goal,
        "tone": request.tone,
        "channel": request.channel,
        "offer": request.offer,
        "cta": request.cta,
        "variants": request.variants
    })
    log_manager.add_log(
        "营销文案",
        request.product_name,
        f"生成营销文案 {len(copies)} 个版本（目标：{request.goal}）",
        "success"
    )
    return ok_response({
        "copies": copies,
        "total": len(copies)
    })


@router.post("/api/marketing/score")
async def score_marketing_copy(request: MarketingScoreRequest):
    """评分营销文案质量"""
    result = marketing_service.score(request.text)
    return ok_response(result)


@router.post("/api/marketing/save-as-template")
async def save_marketing_as_template(request: dict):
    """将营销文案保存为消息模板"""
    template_id = request.get("template_id")
    name = request.get("name")
    content = request.get("content")
    category = request.get("category", "marketing")
    variables = request.get("variables", [])

    if not template_id or not name or not content:
        raise HTTPException(status_code=400, detail="缺少 template_id/name/content")

    success = template_manager.add_template(
        template_id=template_id,
        name=name,
        content=content,
        category=category,
        variables=variables
    )
    if not success:
        raise HTTPException(status_code=400, detail="模板ID已存在")

    log_manager.add_log("营销文案", template_id, f"保存营销模板: {name}", "success")
    return ok_response({"message": "模板保存成功", "template_id": template_id})


@router.get("/api/workspace/marketing/playbooks")
async def workspace_marketing_playbooks():
    """品牌化别名：营销玩法库"""
    playbooks = marketing_service.list_playbooks()
    return ok_response({"playbooks": playbooks, "total": len(playbooks)})

