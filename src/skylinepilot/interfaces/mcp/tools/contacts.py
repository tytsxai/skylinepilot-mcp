"""
联系人工具域：文本格式化能力
"""
from typing import Any, Iterable, List


def format_contacts(users: Iterable[Any]) -> str:
    """统一联系人文本输出"""
    lines: List[str] = []
    for user in users:
        name = f"{getattr(user, 'first_name', '')} {getattr(user, 'last_name', '')}".strip()
        username = f" @{user.username}" if getattr(user, "username", None) else ""
        phone = getattr(user, "phone", None)
        phone_str = f" | {phone}" if phone else ""
        lines.append(f"👤 {name}{username} (ID: {user.id}){phone_str}")
    return "\n".join(lines)

