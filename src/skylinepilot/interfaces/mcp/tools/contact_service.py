"""
联系人工具域：面向 MCP 工具的服务编排
"""
from .contact_ops import (
    fetch_contacts,
    search_contacts,
    import_contact,
    delete_contact,
    block_contact_user,
    unblock_contact_user,
)
from .contacts import format_contacts


async def run_get_contacts(client) -> str:
    result = await fetch_contacts(client)
    if not result.users:
        return "没有联系人"
    return format_contacts(result.users)


async def run_search_contacts(client, query: str, limit: int = 50) -> str:
    result = await search_contacts(client, query=query, limit=limit)
    if not result.users:
        return f"未找到匹配 '{query}' 的联系人"
    return format_contacts(result.users)


async def run_add_contact(client, phone: str, first_name: str, last_name: str = "") -> str:
    result = await import_contact(client, phone=phone, first_name=first_name, last_name=last_name)
    if result.imported:
        return f"✅ 已添加联系人: {first_name} {last_name}"
    return "联系人未添加，可能已存在"


async def run_delete_contact(client, user_id) -> str:
    await delete_contact(client, user_id=user_id)
    return f"✅ 已删除联系人 {user_id}"


async def run_block_user(client, user_id) -> str:
    await block_contact_user(client, user_id=user_id)
    return f"✅ 已拉黑 {user_id}"


async def run_unblock_user(client, user_id) -> str:
    await unblock_contact_user(client, user_id=user_id)
    return f"✅ 已解除拉黑 {user_id}"

