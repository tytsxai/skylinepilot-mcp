# SkylinePilot MCP 改造执行进度

更新时间：2026-02-13

---

## 已完成（本轮）

1. 品牌升级
   - 项目名统一为 **SkylinePilot MCP**
   - `pyproject.toml` 包名改为 `skylinepilot-mcp`
   - 新增 CLI 别名：`skylinepilot`

2. 文档体系升级
   - `README.md` 全面改写为增长导向版本
   - `growth_docs/PROJECT_REBUILD_BLUEPRINT.md` 改造蓝图
   - `growth_docs/BRAND_STYLE_GUIDE.md` 品牌风格指南
   - `growth_docs/MARKETING_GROWTH_PLAYBOOK.md` 营销增长作战手册
   - `growth_docs/SOCIAL_MEDIA_TEMPLATE.md` 社媒模板重写

3. 产品文案升级
   - `dashboard.py` 标题升级
   - `console_ui/dashboard.html` 核心标题与提示语升级
   - `main.py` MCP server 名称支持品牌化环境变量

4. 营销能力代码落地（新增）
   - 新增 `marketing_engine.py`
   - 新增 API：
     - `GET /api/marketing/playbooks`
     - `POST /api/marketing/generate`
     - `POST /api/marketing/score`
     - `POST /api/marketing/save-as-template`
   - 新增测试：`test_marketing_engine.py`

5. 架构迁移骨架启动
   - 新增 `src/skylinepilot/` 目录骨架
   - 新增 MCP/Web 兼容入口封装

6. Web API 拆分第一刀（进行中）
   - 新增统一响应层：`src/skylinepilot/interfaces/web_api/response.py`
   - 新增营销路由模块：`src/skylinepilot/interfaces/web_api/routes/marketing.py`
   - `dashboard.py` 改为通过 `app.include_router(marketing_router)` 挂载营销路由
   - 营销路由已从 `dashboard.py` 主文件迁出

7. 测试基建最小补齐
   - 新增 `requirements-dev.txt`（pytest）

8. Web API 拆分第二刀（继续推进）
   - 新增账号只读路由：`src/skylinepilot/interfaces/web_api/routes/accounts_read.py`
   - 新增账号写操作路由：`src/skylinepilot/interfaces/web_api/routes/accounts_write.py`
   - 新增模板路由：`src/skylinepilot/interfaces/web_api/routes/templates.py`
   - `dashboard.py` 已通过 `include_router` 挂载上述模块
   - `dashboard.py` 中账号相关 API 已全部迁出，主文件路由数量继续下降（兼容壳层形态）
   - 新增代理路由：`src/skylinepilot/interfaces/web_api/routes/proxies.py`
   - 代理相关 API 与 `/api/workspace/proxies` 已迁出 `dashboard.py`
   - 新增健康路由：`src/skylinepilot/interfaces/web_api/routes/health.py`
   - 新增统计路由：`src/skylinepilot/interfaces/web_api/routes/stats.py`
   - 新增日志路由：`src/skylinepilot/interfaces/web_api/routes/logs.py`
   - 新增调度路由：`src/skylinepilot/interfaces/web_api/routes/schedules.py`
   - 新增批量路由：`src/skylinepilot/interfaces/web_api/routes/batch.py`
   - `dashboard.py` 继续收敛为组合壳层（router mount + lifespan + websocket）
   - `dashboard.py` 主文件路由已降到 2 个（`/` 与 `/ws`）

9. Core 服务层补齐（首批）
   - 新增 `src/skylinepilot/core/accounts/service.py`
   - 新增 `src/skylinepilot/core/templates/service.py`
   - 路由层不再直接承接模板参数规范化规则

10. MCP 工具域拆分（首批低风险）
    - 新增 `src/skylinepilot/interfaces/mcp/tools/contacts.py`
    - 新增 `src/skylinepilot/interfaces/mcp/tools/profile.py`
    - `main.py` 对应工具改为调用域模块，降低重复逻辑
    - 新增 `contact_ops.py` / `profile_ops.py`，开始迁移联系人/资料数据访问逻辑
    - `add/delete/block/unblock contact`、`update_profile`、`mute/unmute` 已改为调用 ops 层
    - 新增 `contact_service.py` / `profile_service.py`，MCP 工具函数改为调用 service 层

11. 测试分层落地（起步）
    - 新增 `tests/unit/`：营销引擎、响应结构、MCP 域格式化测试
    - 新增 `tests/integration/`：dashboard 路由挂载检查
    - 新增 `growth_docs/TEST_BASELINE.md`：记录本轮可复现测试命令与结果
    - 新增 `tests/unit/test_mcp_ops.py`：覆盖联系人/资料 ops 层请求构造路径
    - 新增 `tests/unit/test_mcp_services.py`：覆盖联系人/资料 service 层输出行为

12. 依赖修复
    - `requirements.txt` / `pyproject.toml` 增加 `croniter`
    - 修复 `dashboard.py` 导入 `scheduler.py` 时缺依赖问题
    - `requirements.txt` 补齐 `mcp[cli]` / `playwright`，修复测试收集时核心依赖缺失问题

13. 测试入口规范化
    - 新增 `pytest.ini`，默认只收集 `tests/` 分层测试
    - 避免 legacy 手工脚本（根目录 `test_*.py`）被 pytest 误收集导致假失败

14. 开源发布与仓库治理
    - 新仓库已发布为公开：`https://github.com/tytsxai/skylinepilot-mcp`
    - Git 远程已规范化：`origin` 指向公开仓库，`upstream` 指向历史上游仓库
    - 新增 GitHub Actions 工作流：`.github/workflows/ci.yml`
    - README 增加开源状态徽章（CI / License / Repo）

---

## 待执行（下一轮）

1. `main.py` 工具按域拆分（chat/message/contact/group/...）
2. `dashboard.py` 路由层与服务层分离
3. `console_ui/dashboard.html` 组件化拆分
4. API 全面切换统一响应结构（ok/data/error）
5. 测试分层（unit/integration/e2e）

---

## 风险与注意

- 当前仍保留兼容壳层，属于“迁移中形态”。
- 已通过 `.venv + requirements-dev.txt + pytest.ini` 建立分层测试基线。
- 根目录 legacy 手工测试脚本仍存在，默认不纳入自动化收集（避免误报）。
