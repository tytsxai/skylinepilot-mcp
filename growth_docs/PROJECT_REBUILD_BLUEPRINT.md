# Telegram MCP 全面改造蓝图（核心功能不变）

> 文档目标：在**不改变核心业务能力**（123 个 MCP 工具、多账号管理、登录、代理、批量、定时、Web 管理台）的前提下，完成项目的命名升级、风格统一、架构重组与工程化增强。  
> 文档状态：`Draft v1`（基于当前仓库实际代码结构分析）  
> 分析时间：2026-02-13

---

## 1. 现状快照（基于仓库真实结构）

### 1.1 代码与目录现状

- 代码主体为**单层平铺**：大部分 Python 文件直接位于仓库根目录。
- 关键文件体量偏大：
  - `main.py`: **4277 行**（123 个 `@mcp.tool`，工具集高度集中）
  - `dashboard.py`: **995 行**（FastAPI 路由与业务逻辑耦合）
  - `account_manager.py`: **958 行**（账号管理、登录状态、配置持久化混合）
  - `console_ui/dashboard.html`: **2329 行**（HTML/CSS/JS 单文件）
- 现有技术栈存在混用：
  - FastAPI（`dashboard.py`）
  - Flask（`web_login.py`）
  - 还存在多个登录脚本（`qr_login.py` / `qr_web_login.py` / `web_login.py` / `login.py`）

### 1.2 当前已验证的核心能力（保留范围）

1. MCP 工具调用能力（聊天、消息、联系人、群组、媒体、搜索、定时、AI 润色）
2. 多账号管理（Session 导入、二维码登录、手机号流程）
3. 代理管理（全局/按账号）
4. 批量操作（批量发送、健康检查、导出 Session）
5. Web 管理后台（账号/代理/日志/模板/统计/任务）

---

## 2. 改造边界（必须遵守）

### 2.1 不变项（红线）

- **核心功能不删减**：123 MCP 工具与现有管理能力全部保留。
- **外部行为兼容优先**：先做“壳层兼容 + 内部重构”，避免一次性破坏。
- **账号数据可迁移**：`runtime_data/config.json`、session 等历史数据可直接迁移。

### 2.2 可改项（升级空间）

- 项目命名（品牌升级）
- 目录结构与模块边界
- API 风格与响应规范
- UI 视觉风格与交互一致性
- 测试组织、发布流程、文档体系

---

## 3. 新命名与品牌升级方案

## 3.1 推荐新项目名（主推）

- **中文名**：`电报自动化控制台`
- **英文名**：`SkylinePilot MCP`
- **定位语**：`Production-grade Telegram Automation Console`

说明：  
- “Pilot”强调“自动化驾驶舱”，比“Complete”更聚焦产品定位。  
- 保留 `MCP` 关键词，避免生态识别断裂。  

### 3.2 包名与可执行入口（建议）

| 维度 | 当前 | 建议 |
|---|---|---|
| PyPI/项目名 | `skylinepilot-mcp` | `skylinepilot-mcp` |
| CLI 命令 | `telegram-mcp`（兼容） | `skylinepilot`（主推荐） |
| MCP server 名称 | `telegram-complete` | `skylinepilot-core` |
| Dashboard 标题 | Telegram 多账号管理 | SkylinePilot 控制台 |

---

## 4. 风格统一方案（代码 + API + UI）

### 4.1 代码风格统一

1. **单一入口原则**：  
   - MCP 服务入口：`src/skylinepilot/server.py`  
   - Web 控制台入口：`src/skylinepilot/web/app.py`
2. **职责分层**：  
   - `core/`：业务逻辑  
   - `infra/`：Telethon、存储、代理、外部依赖  
   - `interfaces/`：MCP 工具层、HTTP API 层
3. **配置统一**：  
   - 使用 `settings.py` 管理环境变量与默认值  
   - 移除散落常量（例如 API_ID/API_HASH 多点定义）

### 4.2 API 风格统一（REST 与错误模型）

统一响应信封：

```json
{
  "ok": true,
  "data": {},
  "error": null,
  "request_id": "..."
}
```

统一错误结构：

```json
{
  "ok": false,
  "data": null,
  "error": {
    "code": "ACCOUNT_NOT_FOUND",
    "message": "账号不存在"
  },
  "request_id": "..."
}
```

### 4.3 UI 风格统一（Design Token）

- 颜色体系：primary / success / warning / danger 全局 token 化
- 间距体系：`4/8/12/16/24/32`
- 字体层级：`h1/h2/body/caption` 明确标准
- 组件规范：按钮、表格、弹窗、状态 badge 统一视觉语言
- 前端结构：将单文件 `dashboard.html` 拆分为组件（Vue SFC 或最小模块化 JS）

---

## 5. 目标架构（理想形态）

```text
skylinepilot-mcp/
├── src/
│   └── telepilot/
│       ├── core/
│       │   ├── runtime_data/
│       │   ├── messaging/
│       │   ├── scheduler/
│       │   ├── templates/
│       │   └── health/
│       ├── infra/
│       │   ├── telegram_client/
│       │   ├── storage/
│       │   ├── proxy/
│       │   └── logging/
│       ├── interfaces/
│       │   ├── mcp_tools/
│       │   └── web_api/
│       ├── web/
│       │   ├── app.py
│       │   └── console_ui/
│       └── settings.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── growth_docs/
└── scripts/
```

---

## 6. 旧模块到新模块映射（迁移清单）

| 当前文件 | 目标位置 | 迁移说明 |
|---|---|---|
| `main.py` | `src/skylinepilot/interfaces/mcp_tools/*.py` | 按功能拆为 chat/message/contact/group/media/schedule/ai |
| `dashboard.py` | `src/skylinepilot/interfaces/web_api/*.py` + `web/app.py` | 路由与服务层分离 |
| `account_manager.py` | `src/skylinepilot/core/accounts/service.py` | 账号流程下沉到 service 层 |
| `proxy_manager.py` | `src/skylinepilot/infra/proxy/manager.py` | 代理基础设施独立 |
| `scheduler.py` | `src/skylinepilot/core/scheduler/service.py` | 调度逻辑与 API 解耦 |
| `template_manager.py` | `src/skylinepilot/core/templates/service.py` | 模板管理服务化 |
| `health_monitor.py` | `src/skylinepilot/core/health/service.py` | 健康检查能力聚合 |
| `stats_tracker.py` | `src/skylinepilot/core/analytics/service.py` | 统计能力抽象化 |
| `web_login.py` | `src/skylinepilot/interfaces/web_api/login.py` | 与 FastAPI 统一，逐步淘汰 Flask |

---

## 7. 分阶段实施（核心功能持续可用）

### Phase 0：冻结行为基线（1~2 天）

- 补齐“核心路径”回归清单：
  - 登录、发送消息、查询聊天、定时任务、批量操作
- 记录当前 API 与 MCP 工具行为样例（作为迁移验收标准）

### Phase 1：目录与壳层重构（3~5 天）

- 引入 `src/skylinepilot` 目录
- 原文件保留，但改为转发调用新模块（Compatibility Layer）
- 增加统一 `settings` 与日志上下文

### Phase 2：功能拆分与去耦（5~10 天）

- 拆分 `main.py` 的 123 工具到多个模块
- 拆分 `dashboard.py` 路由与服务层
- 抽出统一错误类型与响应模型

### Phase 3：前端风格升级（3~5 天）

- 将 `console_ui/dashboard.html` 拆分
- 统一 Design Token、状态组件、操作反馈
- 保持所有现有功能入口不丢失

### Phase 4：质量与发布（2~4 天）

- 建立 `unit + integration + e2e` 测试分层
- 增加 CI：lint / test / package
- 更新 README、部署文档、迁移文档

---

## 8. 风险与规避

| 风险 | 表现 | 缓解方案 |
|---|---|---|
| 大文件拆分引入回归 | 某些工具参数行为变化 | 先做 Golden Tests，逐类迁移逐类验证 |
| 双框架并存导致维护复杂 | FastAPI + Flask 冲突 | 先隔离 Flask 登录，再逐步合并到 FastAPI |
| 历史配置兼容问题 | 旧账号配置读取失败 | 提供配置迁移脚本 + 启动时自动校验 |
| 前端大改动破坏可用性 | 功能入口丢失 | 分 tab 逐步替换，保留旧页面 fallback |

---

## 9. 验收标准（Definition of Done）

1. 功能完整性：原有核心能力 100% 可用  
2. 结构清晰度：核心模块不再依赖单一超级文件  
3. 风格一致性：命名、接口、UI 统一规范  
4. 可维护性：新增功能无需改动超过 3 个核心模块  
5. 文档一致性：README + AGENTS + 架构文档同步更新

---

## 10. 最小可行实施（MVP）与理想方案

### 10.1 MVP（立刻落地）

- 不改业务行为，只做：
  - 新目录骨架
  - 模块转发壳层
  - 文档与命名统一
  - 基础测试补齐

### 10.2 理想方案（完整升级）

- 完全模块化工具体系
- FastAPI 单栈统一
- 前端组件化 + 设计系统
- 自动化发布与版本化 API

---

## 11. 建议的下一步执行顺序

1. 使用品牌命名：`SkylinePilot MCP` 作为统一对外名称  
2. 执行 Phase 0：产出行为基线测试  
3. 执行 Phase 1：建立新目录与兼容壳层  
4. 执行 Phase 2：拆分 `main.py`（优先聊天/消息/联系人）  
5. 最后做 UI 风格升级与发布文档更新
