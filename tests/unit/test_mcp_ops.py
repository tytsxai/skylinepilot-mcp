import asyncio

from src.skylinepilot.interfaces.mcp.tools.contact_ops import (
    import_contact,
    delete_contact,
    block_contact_user,
    unblock_contact_user,
)
from src.skylinepilot.interfaces.mcp.tools.profile_ops import (
    update_my_profile,
    set_chat_mute_state,
)


class FakeClient:
    def __init__(self):
        self.calls = []

    async def __call__(self, req):
        self.calls.append(req.__class__.__name__)
        return type("Result", (), {"imported": [1]})()

    async def get_entity(self, value):
        self.calls.append(f"get_entity:{value}")
        return f"entity:{value}"


def test_contact_ops_requests():
    c = FakeClient()

    async def _run():
        await import_contact(c, phone="+8613800138000", first_name="A", last_name="B")
        await delete_contact(c, user_id="u1")
        await block_contact_user(c, user_id="u2")
        await unblock_contact_user(c, user_id="u3")

    asyncio.run(_run())
    assert "ImportContactsRequest" in c.calls
    assert "DeleteContactsRequest" in c.calls
    assert "BlockRequest" in c.calls
    assert "UnblockRequest" in c.calls


def test_profile_ops_requests():
    c = FakeClient()

    async def _run():
        await update_my_profile(c, first_name="Sky", last_name="Pilot", about="Hello")
        await set_chat_mute_state(c, chat_id="chat1", mute=True)
        await set_chat_mute_state(c, chat_id="chat1", mute=False)

    asyncio.run(_run())
    assert "UpdateProfileRequest" in c.calls
    assert c.calls.count("UpdateNotifySettingsRequest") == 2

