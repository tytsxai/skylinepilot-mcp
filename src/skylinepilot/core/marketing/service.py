"""
营销服务层（兼容层）
将营销能力从接口层隔离，便于后续接入更复杂的模型与策略引擎
"""
from dataclasses import asdict
from typing import Dict, List

from marketing_engine import CampaignContext, marketing_engine


class MarketingService:
    """营销文案服务"""

    def list_playbooks(self) -> Dict:
        return marketing_engine.list_playbooks()

    def generate(self, payload: Dict) -> List[Dict]:
        ctx = CampaignContext(
            product_name=payload.get("product_name", ""),
            audience=payload.get("audience", ""),
            goal=payload.get("goal", ""),
            tone=payload.get("tone", "professional"),
            channel=payload.get("channel", "telegram_dm"),
            offer=payload.get("offer", ""),
            cta=payload.get("cta", "回复“1”领取详情"),
        )
        return marketing_engine.generate_copy(ctx, variants=payload.get("variants", 3))

    def score(self, text: str) -> Dict:
        return marketing_engine.score_copy(text)

    def preview_context(self, payload: Dict) -> Dict:
        ctx = CampaignContext(
            product_name=payload.get("product_name", ""),
            audience=payload.get("audience", ""),
            goal=payload.get("goal", ""),
            tone=payload.get("tone", "professional"),
            channel=payload.get("channel", "telegram_dm"),
            offer=payload.get("offer", ""),
            cta=payload.get("cta", "回复“1”领取详情"),
        )
        return asdict(ctx)


marketing_service = MarketingService()

