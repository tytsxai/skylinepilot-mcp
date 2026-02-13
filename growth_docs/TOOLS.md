# SkylinePilot MCP 工具清单（文档版）

> 本文是「工具导航索引」，用于快速定位能力。  
> 精确行为以 `main.py` 中 `@mcp.tool` 实现为准。

---

## 1) 当前规模快照

- MCP 工具总数：**123**
- 统计基线：`main.py` 的 `@mcp.tool` 装饰器数量
- 基线日期：**2026-02-13**

---

## 2) 能力域导航（按场景）

| 能力域 | 代表工具 | 典型用途 |
|---|---|---|
| 会话/聊天 | `get_chats`, `get_chat`, `join_chat`, `leave_chat` | 浏览会话、入群退群 |
| 消息操作 | `send_message`, `get_messages`, `reply_message`, `edit_message`, `delete_message`, `search_messages` | 发消息、查历史、编辑撤回 |
| 联系人 | `get_contacts`, `search_contacts`, `add_contact`, `delete_contact`, `block_user`, `unblock_user` | 联系人维护与黑名单管理 |
| 群组治理 | `get_participants`, `get_admins`, `invite_to_chat`, `promote_admin`, `ban_user`, `unban_user` | 群成员管理与权限治理 |
| 个人资料 | `get_me`, `update_profile`, `get_user_status` | 账号资料查询与更新 |
| 通知控制 | `mute_chat`, `unmute_chat` | 会话静音与恢复 |
| 媒体发送 | `send_photo`, `send_video`, `send_document`, `send_voice` | 多媒体内容发送 |
| 运营辅助 | `create_poll` 等 | 投票互动和运营动作 |

> 说明：以上是「高频工具索引」，不是完整函数列表。

---

## 3) 如何获取“完整工具名单”

建议在仓库根目录执行以下命令，自动提取最新工具列表：

```bash
python3 - <<'PY'
import ast
from pathlib import Path

src = Path("main.py").read_text(encoding="utf-8")
mod = ast.parse(src)
tools = []

for node in mod.body:
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        for d in node.decorator_list:
            if isinstance(d, ast.Call) and isinstance(d.func, ast.Attribute) and d.func.attr == "tool":
                tools.append(node.name)
                break
            if isinstance(d, ast.Attribute) and d.attr == "tool":
                tools.append(node.name)
                break

print(f"tool_count={len(tools)}")
for name in tools:
    print(name)
PY
```

---

## 4) 维护约定

1. 每次新增/删除 MCP 工具时，至少更新：
   - 本文件的“当前规模快照”
   - `AGENTS.md` 的“本次文档变更记录”
2. 当工具语义发生破坏性变化时，同步更新：
   - `README.md` 的能力说明
   - `SUPPORT.md` 的用户支持说明

