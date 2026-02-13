"""
资料工具域：数据访问与状态计算
"""
from telethon import functions
from telethon.tl.types import InputPeerNotifySettings


async def fetch_me(client):
    """获取当前账号信息"""
    return await client.get_me()


async def fetch_user_entity(client, user_id):
    """获取用户实体"""
    return await client.get_entity(user_id)


async def update_my_profile(client, first_name=None, last_name=None, about=None):
    """更新当前账号资料"""
    return await client(functions.account.UpdateProfileRequest(
        first_name=first_name,
        last_name=last_name,
        about=about
    ))


async def set_chat_mute_state(client, chat_id, mute: bool):
    """设置聊天静音状态"""
    peer = await client.get_entity(chat_id)
    mute_until = 2**31 - 1 if mute else 0
    return await client(functions.account.UpdateNotifySettingsRequest(
        peer=peer,
        settings=InputPeerNotifySettings(mute_until=mute_until)
    ))
