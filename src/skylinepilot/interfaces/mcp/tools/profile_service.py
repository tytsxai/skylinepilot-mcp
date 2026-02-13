"""
资料工具域：面向 MCP 工具的服务编排
"""
from .profile import format_me, format_user_status
from .profile_ops import fetch_me, fetch_user_entity, update_my_profile, set_chat_mute_state


async def run_get_me(client) -> str:
    me = await fetch_me(client)
    return format_me(me)


async def run_get_user_status(client, user_id) -> str:
    user = await fetch_user_entity(client, user_id)
    return format_user_status(user)


async def run_update_profile(client, first_name=None, last_name=None, about=None) -> str:
    await update_my_profile(client, first_name=first_name, last_name=last_name, about=about)
    return "✅ 个人资料已更新"


async def run_mute_chat(client, chat_id) -> str:
    await set_chat_mute_state(client, chat_id=chat_id, mute=True)
    return f"✅ {chat_id} 已静音"


async def run_unmute_chat(client, chat_id) -> str:
    await set_chat_mute_state(client, chat_id=chat_id, mute=False)
    return f"✅ {chat_id} 已取消静音"

