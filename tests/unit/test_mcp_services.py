import asyncio

from src.skylinepilot.interfaces.mcp.tools.contact_service import (
    run_get_contacts,
    run_search_contacts,
    run_add_contact,
    run_delete_contact,
    run_block_user,
    run_unblock_user,
)
from src.skylinepilot.interfaces.mcp.tools.profile_service import (
    run_get_me,
    run_get_user_status,
    run_update_profile,
    run_mute_chat,
    run_unmute_chat,
)


class FakeUser:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class FakeResult:
    def __init__(self, users=None, imported=None):
        self.users = users or []
        self.imported = imported or []


class FakeClient:
    def __init__(self):
        self.calls = []

    async def __call__(self, req):
        name = req.__class__.__name__
        self.calls.append(name)
        if name in ("GetContactsRequest", "SearchRequest"):
            return FakeResult(users=[FakeUser(id=1, first_name="A", last_name="B", username="ab", phone="10086")])
        if name == "ImportContactsRequest":
            return FakeResult(imported=[1])
        return FakeResult()

    async def get_me(self):
        return FakeUser(id=7, first_name="Sky", last_name="Pilot", username="sky", phone="1", bot=False, verified=True, premium=False)

    async def get_entity(self, user_id):
        class UserStatusOnline:
            pass
        s = UserStatusOnline()
        return FakeUser(id=99, status=s)


def test_contact_services():
    c = FakeClient()

    async def _run():
        text1 = await run_get_contacts(c)
        text2 = await run_search_contacts(c, query="ab")
        text3 = await run_add_contact(c, phone="+1", first_name="A", last_name="B")
        text4 = await run_delete_contact(c, user_id="u1")
        text5 = await run_block_user(c, user_id="u2")
        text6 = await run_unblock_user(c, user_id="u3")
        return text1, text2, text3, text4, text5, text6

    t1, t2, t3, t4, t5, t6 = asyncio.run(_run())
    assert "👤" in t1 and "👤" in t2
    assert "已添加联系人" in t3
    assert "已删除联系人" in t4
    assert "已拉黑" in t5
    assert "已解除拉黑" in t6


def test_profile_services():
    c = FakeClient()

    async def _run():
        a = await run_get_me(c)
        b = await run_get_user_status(c, user_id="u1")
        c1 = await run_update_profile(c, first_name="S", last_name="P", about="x")
        d = await run_mute_chat(c, chat_id="chat1")
        e = await run_unmute_chat(c, chat_id="chat1")
        return a, b, c1, d, e

    a, b, c1, d, e = asyncio.run(_run())
    assert "你的信息" in a
    assert "在线" in b or "状态" in b
    assert "个人资料已更新" in c1
    assert "已静音" in d
    assert "已取消静音" in e
