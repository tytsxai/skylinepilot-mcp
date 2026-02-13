#!/usr/bin/env python3
"""
营销文案引擎快速测试
"""
from marketing_engine import CampaignContext, marketing_engine


def test_generate_copy_variants():
    ctx = CampaignContext(
        product_name="SkylinePilot MCP",
        audience="Telegram 运营团队",
        goal="活动转化",
        tone="professional",
        offer="3 套活动触达模板",
        cta="回复“模板”立即领取"
    )
    copies = marketing_engine.generate_copy(ctx, variants=3)
    assert len(copies) == 3
    assert "回复" in copies[0]["copy"] or "领取" in copies[0]["copy"]


def test_score_copy():
    text = "你好，我们可以帮助你提升 Telegram 运营效率。回复“1”领取完整方案。"
    result = marketing_engine.score_copy(text)
    assert result["score"] >= 60
    assert result["level"] in {"excellent", "good", "fair", "poor"}

