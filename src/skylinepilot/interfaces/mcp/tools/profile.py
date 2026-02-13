"""
资料工具域：文本格式化能力
"""
from typing import Any, List


def format_me(me: Any) -> str:
    """格式化当前账号信息"""
    name = f"{me.first_name or ''} {me.last_name or ''}".strip()
    lines: List[str] = [
        "📱 你的信息:",
        f"ID: {me.id}",
        f"名称: {name}",
    ]

    if me.username:
        lines.append(f"用户名: @{me.username}")
    if me.phone:
        lines.append(f"手机: {me.phone}")
    lines.append(f"是机器人: {'是' if me.bot else '否'}")
    lines.append(f"已验证: {'是' if getattr(me, 'verified', False) else '否'}")
    lines.append(f"高级版: {'是' if getattr(me, 'premium', False) else '否'}")
    return "\n".join(lines)


def format_user_status(user: Any) -> str:
    """格式化用户在线状态"""
    if hasattr(user, "status") and user.status:
        status = user.status
        if hasattr(status, "was_online"):
            last_seen = status.was_online.strftime("%Y-%m-%d %H:%M:%S")
            return f"👤 用户上次在线: {last_seen}"
        status_name = status.__class__.__name__
        if status_name == "UserStatusOnline":
            return "🟢 用户当前在线"
        if status_name == "UserStatusOffline":
            return "🔴 用户离线"
        if status_name == "UserStatusRecently":
            return "🟡 用户最近在线"
        return f"状态: {status}"
    return "无法获取用户状态"

