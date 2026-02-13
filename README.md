<div align="center">

<img src="https://img.icons8.com/color/96/000000/telegram-app.png" alt="SkylinePilot MCP" width="84" height="84">

# SkylinePilot MCP

**让 Telegram 运营从“手工群发”进化为“系统化增长引擎”**

[![CI](https://github.com/tytsxai/skylinepilot-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/tytsxai/skylinepilot-mcp/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![GitHub Repo](https://img.shields.io/badge/GitHub-tytsxai%2Fskylinepilot--mcp-blue)](https://github.com/tytsxai/skylinepilot-mcp)

> 核心功能不变，体验与商业表达全面升级：
> 多账号管理 / 123+ MCP 工具 / 批量触达 / 定时任务 / AI 文案润色 / Web 控制台

<p>
  <a href="#-快速开始">快速开始</a> ·
  <a href="#-营销与运营场景">营销场景</a> ·
  <a href="#-核心能力">核心能力</a> ·
  <a href="#-文案系统与转化策略">文案策略</a> ·
  <a href="#-路线图">路线图</a>
</p>

</div>

---

## 为什么是 SkylinePilot MCP

你不是在找一个“会发消息的脚本”。
你需要的是一个可持续的 Telegram 增长系统：

- **可规模化**：多账号矩阵统一调度
- **可控风险**：代理、节奏、健康监控、日志审计
- **可提升转化**：模板 + AI 润色 + A/B 文案迭代
- **可运营**：任务化、批量化、可视化

一句话：
**让团队把时间花在“策略”上，而不是重复点击发送。**

---

## 核心能力

### 1) MCP 自动化能力（123+ Tools）
- 聊天、消息、联系人、群组、频道、媒体、搜索、会话等核心操作覆盖
- AI 可直接调用工具执行真实业务动作

### 2) 多账号运营中台
- 账号导入、会话管理、在线状态追踪
- 账号维度统计：使用频次、风险状态、运行健康度

### 3) 登录与接入体验
- 二维码登录 + 手机号验证码登录
- 支持 2FA 流程

### 4) 营销执行能力
- 批量发送（用户名/联系人）
- 定时任务（一次/每天/每周/工作日）
- 消息模板变量替换（姓名、时间、活动参数）

### 5) 文案增强能力
- `polish_message`：优化语气、结构、礼貌度
- `expand_message`：扩写价值表达、增强行动引导
- 可与定时任务联动，先润色再发送

### 6) 风险与稳定性
- 代理管理（全局 + 按账号）
- 健康监控 + 异常提醒
- 操作日志可追溯

---

## 营销与运营场景

### 场景 A：新品冷启动
**目标**：7 天内触达首批种子用户并获取首轮反馈

执行建议：
1. 用标签拆分目标人群（开发者 / 渠道 / KOL / 老用户）
2. 每个人群使用独立模板
3. 每天固定时段发送，控制节奏与间隔
4. 对回复用户做二次触达（感谢 + CTA）

### 场景 B：私域复购召回
**目标**：激活沉默用户，提升活动参与率

执行建议：
1. 先发“低打扰唤醒文案”
2. 24 小时后发“利益点强化文案”
3. 72 小时后发“限时提醒文案”
4. 按点击/回复做后续分层

### 场景 C：社群运营自动化
**目标**：降低运营重复劳动

执行建议：
- 每日问候、每周公告、活动提醒全部任务化
- 模板参数化（活动名、时间、报名链接）
- 所有发送行为记录日志，便于复盘

---

## 文案系统与转化策略

## 文案三层模型（建议直接套用）

1. **开场钩子（Hook）**：3 秒内建立相关性
2. **价值表达（Value）**：用 1-2 个明确收益点打动用户
3. **行动引导（CTA）**：一句话告诉用户下一步做什么

示例：

- 原文：`你好，看看我们的产品`
- 优化后：
  `你好 👋 我们刚上线了一个可把 Telegram 运营效率提升 3-5 倍的工具，`
  `支持多账号批量触达和 AI 文案优化。`
  `如果你愿意，我可以发你 2 分钟上手清单。`

## 推荐 CTA 模板
- `回复“1”，我发你完整玩法。`
- `如果方便，我给你一个 2 分钟演示视频。`
- `想要测试账号的话，回复“试用”。`

## 新增：营销文案 API（已落地）

- `GET /api/marketing/playbooks`：获取营销玩法库
- `POST /api/marketing/generate`：生成多版本营销文案
- `POST /api/marketing/score`：对营销文案进行质量评分
- `POST /api/marketing/save-as-template`：保存为模板并用于后续批量发送

## 避坑原则
- 不要一上来就硬推销
- 不要一条消息塞 5 个卖点
- 不要没有明确下一步动作

---

## 快速开始

### 本地启动

```bash
git clone https://github.com/tytsxai/skylinepilot-mcp.git
cd skylinepilot-mcp
pip install -r requirements.txt
python dashboard.py
```

浏览器打开：

- `http://localhost:8080/console/dashboard.html`

### 新人维护必跑检查（防复发）

> 这一步建议在每次修改后都执行，避免“修 A 坏 B”的回归。

```bash
# 安装开发依赖（包含 pytest）
pip install -r requirements-dev.txt

# 运行分层测试
python -m pytest -q

# 语法编译检查（快速发现低级错误）
python -m py_compile main.py dashboard.py marketing_engine.py
```

若遇到 `ModuleNotFoundError: src / marketing_engine`，优先检查：
- `tests/conftest.py` 是否仍存在且路径注入逻辑未被破坏
- `pytest.ini` 是否仍收敛到 `tests/` 目录

### MCP 接入（Claude / 其他支持 MCP 的客户端）

```json
{
  "mcpServers": {
    "telegram": {
      "command": "python",
      "args": ["/path/to/skylinepilot-mcp/main.py"]
    }
  }
}
```

---

## 兼容性声明（本次改造）

本轮改造聚焦 **品牌、文档、风格、架构规范**，并遵守：

- 核心功能不变
- 关键入口不变（`main.py` / `dashboard.py`）
- 现有账号与会话数据可继续使用

---

## 项目结构（当前）

```text
.
├── main.py                  # MCP 主服务（123+ tools）
├── dashboard.py             # FastAPI 管理后台
├── account_manager.py       # 账号管理
├── proxy_manager.py         # 代理管理
├── scheduler.py             # 定时任务
├── batch_operations.py      # 批量操作
├── console_ui/dashboard.html # 控制台前端
├── runtime_data/             # 账号与会话配置
└── growth_docs/              # 文档系统
```

---

## 路线图

- **Phase 0：基线冻结**（先保证行为不回归）
- **Phase 1：目录重组与兼容壳层**
- **Phase 2：服务拆分与 API 统一**
- **Phase 3：前端组件化与视觉统一**
- **Phase 4：测试分层与自动化发布**

详见：`growth_docs/PROJECT_REBUILD_BLUEPRINT.md`

---

## 文档索引

- 全面改造蓝图：`growth_docs/PROJECT_REBUILD_BLUEPRINT.md`
- 品牌风格指南：`growth_docs/BRAND_STYLE_GUIDE.md`
- 营销增长手册：`growth_docs/MARKETING_GROWTH_PLAYBOOK.md`
- 架构镜像：`AGENTS.md`

---

## 贡献

欢迎提交 PR：

1. 先提 Issue 说明改动目标
2. 按模块提交（不要一个 PR 做完所有事）
3. 带上最小验证步骤

---

## License

MIT
