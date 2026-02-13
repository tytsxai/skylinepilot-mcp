"""
联系人工具域：数据访问与业务流程
"""
from telethon import functions
from telethon.tl.types import InputPhoneContact


async def fetch_contacts(client):
    """获取联系人列表"""
    return await client(functions.contacts.GetContactsRequest(hash=0))


async def search_contacts(client, query: str, limit: int = 50):
    """搜索联系人"""
    return await client(functions.contacts.SearchRequest(q=query, limit=limit))


async def import_contact(client, phone: str, first_name: str, last_name: str = ""):
    """导入联系人"""
    return await client(functions.contacts.ImportContactsRequest(
        contacts=[InputPhoneContact(
            client_id=0,
            phone=phone,
            first_name=first_name,
            last_name=last_name
        )]
    ))


async def delete_contact(client, user_id):
    """删除联系人"""
    user = await client.get_entity(user_id)
    return await client(functions.contacts.DeleteContactsRequest(id=[user]))


async def block_contact_user(client, user_id):
    """拉黑联系人"""
    user = await client.get_entity(user_id)
    return await client(functions.contacts.BlockRequest(id=user))


async def unblock_contact_user(client, user_id):
    """解除拉黑联系人"""
    user = await client.get_entity(user_id)
    return await client(functions.contacts.UnblockRequest(id=user))
