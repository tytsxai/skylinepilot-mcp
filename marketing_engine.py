#!/usr/bin/env python3
"""
营销文案引擎
用于生成营销触达文案、CTA 建议和基础文案质量评分
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List


@dataclass
class CampaignContext:
    """营销活动上下文"""
    product_name: str
    audience: str
    goal: str
    tone: str = "professional"
    channel: str = "telegram_dm"
    offer: str = ""
    cta: str = "回复“1”领取详情"


class MarketingEngine:
    """营销文案生成器（规则驱动，稳定可控）"""

    def __init__(self):
        self.supported_tones = {"professional", "friendly", "urgent", "consultative"}
        self.playbooks: Dict[str, Dict] = {
            "cold_start": {
                "name": "冷启动触达",
                "steps": ["建立相关性", "给出价值点", "轻量 CTA"],
                "example_cta": ["回复“1”领取清单", "想要模板可直接回复“模板”"],
            },
            "reactivation": {
                "name": "沉默用户召回",
                "steps": ["温和唤醒", "补充利益点", "限时提醒"],
                "example_cta": ["回复“试用”获取体验", "回复“活动”领取方案"],
            },
            "event_push": {
                "name": "活动通知促转化",
                "steps": ["活动亮点", "时间节点", "行动指令"],
                "example_cta": ["现在回复“报名”锁定名额", "回复“我要参加”获取链接"],
            },
        }

    def list_playbooks(self) -> Dict[str, Dict]:
        """获取可用营销 playbook"""
        return self.playbooks

    def generate_copy(self, ctx: CampaignContext, variants: int = 3) -> List[Dict]:
        """生成多版本营销文案"""
        if ctx.tone not in self.supported_tones:
            ctx.tone = "professional"

        variants = max(1, min(variants, 5))
        copies: List[Dict] = []
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        for i in range(1, variants + 1):
            hook = self._build_hook(ctx, i)
            value = self._build_value(ctx, i)
            cta = self._build_cta(ctx, i)

            text = f"{hook}\n{value}\n{cta}"
            copies.append(
                {
                    "variant": i,
                    "title": f"{ctx.goal}文案 V{i}",
                    "copy": text,
                    "meta": {
                        "tone": ctx.tone,
                        "channel": ctx.channel,
                        "generated_at": timestamp,
                    },
                }
            )

        return copies

    def score_copy(self, text: str) -> Dict:
        """基础文案评分（用于快速迭代，不替代人工审核）"""
        text = (text or "").strip()
        if not text:
            return {"score": 0, "level": "poor", "issues": ["文案为空"], "tips": ["请先输入文案内容"]}

        issues: List[str] = []
        tips: List[str] = []
        score = 100

        # 长度检查
        length = len(text)
        if length < 30:
            score -= 20
            issues.append("内容过短，价值点不够完整")
            tips.append("建议至少包含“场景 + 价值 + CTA”三段")
        elif length > 280:
            score -= 10
            issues.append("内容偏长，首屏信息密度可能过高")
            tips.append("建议首条触达控制在 80~180 字")

        # CTA 检查
        cta_patterns = [r"回复", r"点击", r"领取", r"报名", r"试用", r"联系"]
        if not any(re.search(pattern, text) for pattern in cta_patterns):
            score -= 25
            issues.append("缺少明确行动引导（CTA）")
            tips.append("增加如“回复‘1’领取方案”的动作引导")

        # 价值点检查
        value_patterns = [r"提升", r"节省", r"效率", r"增长", r"降低", r"优化"]
        if not any(re.search(pattern, text) for pattern in value_patterns):
            score -= 15
            issues.append("价值表达不够明确")
            tips.append("明确写出可量化收益或具体价值")

        # 语气检查
        if text.count("！") > 4:
            score -= 8
            issues.append("感叹号过多，可能造成压迫感")
            tips.append("减少强促语气，提升沟通自然度")

        score = max(0, score)
        if score >= 85:
            level = "excellent"
        elif score >= 70:
            level = "good"
        elif score >= 55:
            level = "fair"
        else:
            level = "poor"

        return {"score": score, "level": level, "issues": issues, "tips": tips}

    def _build_hook(self, ctx: CampaignContext, variant: int) -> str:
        if ctx.tone == "friendly":
            hooks = [
                f"你好 👋 我们正在帮{ctx.audience}把 Telegram 运营流程做得更轻松。",
                f"嗨，想和你分享一个适合{ctx.audience}的增长方案。",
                f"最近我们在做一套更适合{ctx.audience}的自动化运营方式。",
            ]
        elif ctx.tone == "urgent":
            hooks = [
                f"这周我们给{ctx.audience}开放了限量优化名额。",
                f"有个针对{ctx.audience}的活动窗口，截止时间临近。",
                f"如果你最近在推进{ctx.goal}，现在是最合适的执行时点。",
            ]
        elif ctx.tone == "consultative":
            hooks = [
                f"想请教下，你们目前在{ctx.goal}这块的执行方式是怎样的？",
                f"如果你方便，我可以给你一版针对{ctx.audience}的执行建议。",
                f"我们观察到{ctx.audience}在{ctx.goal}时常遇到同类瓶颈。",
            ]
        else:
            hooks = [
                f"我们正在帮助{ctx.audience}系统化提升 Telegram 运营执行效率。",
                f"针对{ctx.audience}，我们整理了一套可落地的 Telegram 增长流程。",
                f"这是一套面向{ctx.audience}的 Telegram 自动化运营方案。",
            ]
        return hooks[(variant - 1) % len(hooks)]

    def _build_value(self, ctx: CampaignContext, variant: int) -> str:
        offer_text = f"当前可提供：{ctx.offer}。" if ctx.offer else ""
        value_blocks = [
            f"核心价值是把重复触达和定时跟进任务化，减少手工操作，提升稳定性。{offer_text}",
            f"你可以直接用多账号管理 + 批量发送 + AI 文案优化，快速搭建增长执行闭环。{offer_text}",
            f"重点不是“多发消息”，而是让每次触达更有节奏、更可复盘。{offer_text}",
        ]
        return value_blocks[(variant - 1) % len(value_blocks)]

    def _build_cta(self, ctx: CampaignContext, variant: int) -> str:
        cta_candidates = [
            ctx.cta,
            "如果你愿意，我可以先发你一份 2 分钟执行清单。",
            "你回复“模板”，我直接给你 3 套可复制话术。",
        ]
        return cta_candidates[(variant - 1) % len(cta_candidates)]


marketing_engine = MarketingEngine()

