# SkylinePilot MCP 测试基线（本轮）

更新时间：2026-02-13

## 运行环境

- Python venv: `.venv`
- 安装命令：
  - `python3 -m venv .venv`
  - `.venv/bin/pip install -r requirements.txt -r requirements-dev.txt`

## 已执行测试

```bash
.venv/bin/python -m pytest -q \
  tests/unit/test_marketing_engine_unit.py \
  tests/unit/test_web_api_response.py \
  tests/unit/test_mcp_domain_formatters.py \
  tests/integration/test_dashboard_route_mounts.py \
  test_marketing_engine.py
```

结果：`9 passed`

---

## 当前分层测试基线（更新）

```bash
.venv/bin/python -m pytest
```

说明：
- 通过 `pytest.ini`，默认只收集 `tests/` 分层测试目录。
- 当前结果：`11 passed`

## 额外校验

- `py_compile`：64 个 Python 文件，0 语法错误。
- `dashboard.app` 导入成功，关键路由已挂载（accounts/templates/marketing）。
