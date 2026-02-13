# Changelog

本项目变更记录遵循 Keep a Changelog 思路，版本语义遵循 SemVer。

## [Unreleased]

### Added
- 新增 `growth_docs/TOOLS.md`，补齐 MCP 工具文档入口。

### Changed
- 文档巡检并修复占位符链接（`yourusername` -> `tytsxai`）。
- `SUPPORT.md` 更新支持入口，补充安全漏洞私密提交通道。
- `CONTRIBUTING.md` 更新仓库地址示例与 Issues/Discussions 链接。
- `CODE_OF_CONDUCT.md` 更新行为准则举报路径为仓库官方通道。
- `PROJECT_CHECKLIST.md` 与 `growth_docs/SEO_OPTIMIZATION_SUMMARY.md` 同步仓库地址。
- `AGENTS.md` 同步记录本轮文档治理变更。
- `tests/conftest.py` 增补防复发注释，固化测试导入路径约束。
- `pytest.ini` 增补分层测试收敛说明，防止 legacy 脚本误收集。
- `README.md` 新增“新人维护必跑检查”命令，统一本地回归流程。
- `BUGFIXES.md` 新增“防复发维护清单”，沉淀字段兼容与观测性约束。

## [1.0.0] - 2026-01-02

### Added
- SkylinePilot MCP 首个可发布版本文档与能力基线。
