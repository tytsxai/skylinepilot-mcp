from src.skylinepilot.interfaces.mcp.tools.contacts import format_contacts
from src.skylinepilot.interfaces.mcp.tools.profile import format_me


class DummyUser:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def test_format_contacts_basic():
    users = [
        DummyUser(id=1, first_name="A", last_name="B", username="ab", phone="10086"),
        DummyUser(id=2, first_name="C", last_name="", username=None, phone=None),
    ]
    text = format_contacts(users)
    assert "👤 A B @ab (ID: 1) | 10086" in text
    assert "👤 C (ID: 2)" in text


def test_format_me_basic():
    me = DummyUser(
        id=7,
        first_name="Sky",
        last_name="Pilot",
        username="skyline",
        phone="123",
        bot=False,
        verified=True,
        premium=False,
    )
    text = format_me(me)
    assert "ID: 7" in text
    assert "用户名: @skyline" in text
    assert "已验证: 是" in text

