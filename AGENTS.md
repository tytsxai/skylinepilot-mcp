# AGENTS.md

> 本文件是仓库架构与职责边界的“最小真相源”。  
> 当目录、模块职责、接口边界发生变化时，必须同步更新。

---

## 1) 当前目录骨架（As-Is）

```text
skylinepilot-mcp/
├── main.py                      # MCP 主服务（123 tools，当前为超大单文件）
├── dashboard.py                 # FastAPI 管理后台（路由+业务混合）
├── marketing_engine.py          # 营销文案引擎（生成/评分/玩法库）
├── account_manager.py           # 账号管理核心逻辑（配置/登录状态）
├── proxy_manager.py             # 代理管理
├── scheduler.py                 # 定时任务调度
├── batch_operations.py          # 批量任务
├── template_manager.py          # 模板管理
├── health_monitor.py            # 健康监控
├── stats_tracker.py             # 使用统计
├── log_manager.py               # 操作日志
├── web_login.py                 # Flask 登录服务（与 FastAPI 并存）
├── qr_login.py / qr_web_login.py / login.py / pyro_qr_login.py
│                                # 多种登录入口（能力重叠）
├── session_manager.py           # Session 管理
├── console_ui/
│   └── dashboard.html           # 前端单文件（HTML/CSS/JS 混合）
├── runtime_data/
│   └── config.json              # 账号配置与 session 数据
├── growth_docs/                        # 项目文档集合
├── src/skylinepilot/            # 新架构骨架（兼容迁移中）
│   ├── core/
│   │   ├── accounts/__init__.py # 账号核心模块入口
│   │   ├── accounts/service.py  # 账号服务层（只读查询能力封装）
│   │   ├── templates/__init__.py# 模板核心模块入口
│   │   └── templates/service.py # 模板服务层（规则与入参规范化）
│   └── interfaces/
│       ├── web_api/
│       │   ├── response.py      # 统一响应结构（ok/data/error）
│       │   └── routes/
│       │       ├── marketing.py # 营销路由模块（已从 dashboard.py 拆出）
│       │       ├── accounts_read.py # 账号只读路由模块
│       │       ├── accounts_write.py # 账号写操作路由模块
│       │       ├── proxies.py   # 代理路由模块
│       │       ├── health.py    # 健康监控路由模块
│       │       ├── stats.py     # 统计路由模块
│       │       ├── logs.py      # 日志路由模块
│       │       ├── schedules.py # 定时任务路由模块
│       │       ├── batch.py     # 批量操作路由模块
│       │       └── templates.py # 模板路由模块
│       └── mcp/tools/
│           ├── contact_ops.py   # 联系人工具域数据访问
│           ├── contact_service.py # 联系人工具域服务编排
│           ├── contacts.py      # 联系人工具域格式化能力
│           ├── profile.py       # 资料工具域格式化能力
│           ├── profile_ops.py   # 资料工具域数据访问
│           └── profile_service.py # 资料工具域服务编排
├── tests/
│   ├── unit/                    # 单元测试分层（迁移开始）
│   └── integration/             # 集成测试分层（迁移开始）
├── .github/workflows/ci.yml     # CI 流水线（pytest + py_compile）
├── pytest.ini                   # pytest 收敛到 tests/ 分层目录
└── test_*.py                    # 测试脚本（尚未标准化分层）
```

---

## 2) 模块职责与边界（当前）

### `main.py`
- **职责**：MCP 工具注册与执行。
- **问题**：业务聚合过重、分层不清，改动半径大。

### `dashboard.py`
- **职责**：HTTP API + WebSocket + 生命周期管理。
- **现状**：`dashboard.py` 已完成“组合壳层化”，主文件仅保留 `"/"` 与 `"/ws"` 两个 `@app` 路由。
- **现状补充**：账号读写、营销、模板、代理、健康、统计、日志、调度、批量路由均已迁移到 `src/skylinepilot/interfaces/web_api/routes/*`。
- **问题**：WebSocket 推送与运行时状态采集仍与主文件耦合，后续可继续拆分。

### 管理器类（`*_manager.py`）
- **职责**：围绕账户/代理/模板/日志/统计等提供服务。
- **问题**：持久化、业务规则、IO 混在同一层。

### `marketing_engine.py`
- **职责**：营销文案生成、文案评分、玩法库输出。
- **定位**：先提供规则驱动稳定能力，后续可无缝接入 LLM 策略。

### `src/skylinepilot/core/marketing/service.py`
- **职责**：营销能力服务层，屏蔽接口层对底层实现的直接依赖。
- **现状**：`dashboard.py` 的营销 API 已通过该服务层调用。

### `src/skylinepilot/interfaces/web_api/response.py`
- **职责**：统一 API 响应格式（`ok/data/error`）。
- **现状**：已在首页响应、营销路由中使用，其他路由待渐进迁移。

### `src/skylinepilot/core/accounts/service.py`
- **职责**：账号查询能力服务层，隔离 `dashboard` 对 `account_manager` 的直接依赖。

### `src/skylinepilot/core/templates/service.py`
- **职责**：模板规则封装（自动生成模板ID/变量提取/预览解析）。

### `src/skylinepilot/interfaces/mcp/tools/*`
- **职责**：MCP 工具按域拆分第一步，先抽取联系人/资料文本格式化逻辑。
- **现状**：`main.py` 中 `get_contacts/search_contacts/get_me/get_user_status` 已改为调用域模块。
- **现状补充**：已新增 `contact_ops.py` / `profile_ops.py` / `contact_service.py` / `profile_service.py`。
- **现状补充**：`add/delete/block/unblock contact`、`update_profile`、`mute/unmute` 已经通过 service+ops 分层调用。

### `web_login.py` 与 FastAPI 并存
- **职责**：网页登录与二维码流程。
- **问题**：双框架并存提高维护成本。

### `console_ui/dashboard.html`
- **职责**：管理后台前端页面。
- **问题**：单文件过大，不利于样式统一和组件复用。

---

## 3) 建议中的目标边界（To-Be）

```text
src/skylinepilot/
├── core/            # 业务能力：workspace_accounts/messaging/scheduler/templates/health
├── infra/           # 基础设施：telegram client/storage/proxy/logging
├── interfaces/      # 对外接口：mcp_tools/web_api
├── web/             # 前端静态资源与启动
└── settings.py      # 全局配置
```

边界原则：
1. `interfaces` 不直接写配置文件，不直接操作底层 SDK。
2. `core` 不关心 HTTP/MCP 协议细节。
3. `infra` 只提供能力，不承载业务策略。

---

## 4) 上下游依赖（建议）

```text
MCP/Web Request
    -> interfaces (参数校验/响应封装)
    -> core (业务编排与规则)
    -> infra (Telethon/存储/网络)
```

禁止反向依赖：
- `infra` 依赖 `core`
- `core` 依赖 `interfaces`

---

## 5) 本次文档变更记录

- 新增：`growth_docs/PROJECT_REBUILD_BLUEPRINT.md`
  - 输出“核心功能不变”的全面改造蓝图
  - 包含命名升级、风格统一、架构重组、分阶段迁移、验收标准
- 新增：`growth_docs/BRAND_STYLE_GUIDE.md`
  - 统一品牌命名、视觉 Token、接口风格、文案规范
- 新增：`growth_docs/MARKETING_GROWTH_PLAYBOOK.md`
  - 营销定位、增长漏斗、渠道内容、销售话术、KPI 与复盘模板
- 新增：`growth_docs/EXECUTION_PROGRESS.md`
  - 记录本轮已执行改造与下一轮计划
- 更新：`README.md`
  - 重写为产品化表达，突出营销与运营场景，兼顾技术接入
- 更新：`ROADMAP.md`
  - 路线图加入品牌升级与营销增长并行轨道
- 更新：`pyproject.toml`
  - 包名升级为 `skylinepilot-mcp`，新增 CLI 别名 `skylinepilot`
- 更新：`main.py`
  - MCP Server 名称改为可配置：`MCP_SERVER_NAME`（默认 `skylinepilot-core`）
- 更新：`dashboard.py` / `console_ui/dashboard.html`
  - 控制台品牌文案升级为 SkylinePilot MCP
- 新增：`marketing_engine.py`
  - 新增营销文案生成与评分引擎
- 更新：`dashboard.py`
  - 新增营销 API：playbooks / generate / score / save-as-template
- 新增：`src/skylinepilot/*`
  - 建立核心目录骨架与兼容入口（MCP/Web）
- 新增：`test_marketing_engine.py`
  - 营销能力基础测试用例
- 更新：仓库与目录命名
  - 目录重命名：`accounts` -> `runtime_data`
  - 目录重命名：`static` -> `console_ui`
  - 目录重命名：`docs` -> `growth_docs`
  - 项目目录重命名：`telegram-mcp` -> `skylinepilot-mcp`
- 更新：`dashboard.py`
  - 新增品牌化 API 别名：`/api/workspace/*`（与旧 `/api/*` 路径并存）
- 新增：`src/skylinepilot/interfaces/web_api/response.py`
  - 提供统一响应封装：`ok_response` / `error_response`
- 新增：`src/skylinepilot/interfaces/web_api/routes/marketing.py`
  - 营销路由从 `dashboard.py` 拆分到独立模块
- 新增：`src/skylinepilot/interfaces/web_api/routes/accounts_read.py`
  - 账号只读路由从 `dashboard.py` 拆分到独立模块
- 新增：`src/skylinepilot/interfaces/web_api/routes/accounts_write.py`
  - 账号写操作路由从 `dashboard.py` 拆分到独立模块
- 新增：`src/skylinepilot/interfaces/web_api/routes/proxies.py`
  - 代理路由与品牌化别名从 `dashboard.py` 拆分到独立模块
- 新增：`src/skylinepilot/interfaces/web_api/routes/health.py`
  - 健康监控路由与品牌化别名从 `dashboard.py` 拆分到独立模块
- 新增：`src/skylinepilot/interfaces/web_api/routes/stats.py`
  - 统计路由从 `dashboard.py` 拆分到独立模块
- 新增：`src/skylinepilot/interfaces/web_api/routes/logs.py`
  - 日志路由从 `dashboard.py` 拆分到独立模块
- 新增：`src/skylinepilot/interfaces/web_api/routes/schedules.py`
  - 定时任务路由与品牌化别名从 `dashboard.py` 拆分到独立模块
- 新增：`src/skylinepilot/interfaces/web_api/routes/batch.py`
  - 批量操作路由从 `dashboard.py` 拆分到独立模块
- 新增：`src/skylinepilot/interfaces/mcp/tools/contact_ops.py` / `profile_ops.py`
  - MCP 联系人/资料工具域的数据访问逻辑抽离
- 新增：`src/skylinepilot/interfaces/mcp/tools/contact_service.py` / `profile_service.py`
  - MCP 联系人/资料工具域服务编排层
- 新增：`src/skylinepilot/core/accounts/__init__.py` / `src/skylinepilot/core/templates/__init__.py`
  - 核心域模块入口补齐
- 新增：`pytest.ini`
  - pytest 默认只收集 `tests/` 分层测试，避免 legacy 手工脚本误收集
- 新增：`.github/workflows/ci.yml`
  - 开源仓库 CI 自动校验：pytest + py_compile
- 新增：`tests/unit/test_mcp_services.py`
  - 覆盖 MCP 服务层输出与调用链基本行为
- 新增：`src/skylinepilot/interfaces/web_api/routes/templates.py`
  - 模板路由从 `dashboard.py` 拆分到独立模块
- 新增：`src/skylinepilot/core/accounts/service.py`
  - 账号查询服务层
- 新增：`src/skylinepilot/core/templates/service.py`
  - 模板服务层与规则封装
- 新增：`src/skylinepilot/interfaces/mcp/tools/contacts.py` / `profile.py`
  - MCP 工具域模块（联系人/资料）
- 新增：`tests/unit/*` / `tests/integration/*`
  - 测试分层迁移启动
- 更新：`requirements.txt` / `pyproject.toml`
  - 增加 `croniter` 依赖，修复 `dashboard.py` 导入链缺失依赖问题
- 新增：`requirements-dev.txt`
  - 提供最小测试依赖（pytest）
- 新增：`AGENTS.md`（本文件）
  - 建立仓库级架构镜像与职责边界说明

---

## 6) 开发约定（简版）

1. 新增功能优先进入 `core`，避免继续堆积到根目录大文件。  
2. 任何架构级变更（文件移动、模块重组）必须同步更新本文件。  
3. 保持“兼容壳层”直到迁移完成，避免破坏现有用户工作流。  
