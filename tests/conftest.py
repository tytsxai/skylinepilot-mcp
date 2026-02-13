"""
测试环境公共引导。

职责：
1) 确保仓库根目录在 sys.path 中，便于导入根目录模块（如 marketing_engine）。
2) 确保 src 目录可被稳定导入（如 src.skylinepilot.*）。

维护约束（防复发）：
1) 这里的路径注入顺序不要随意调整：仓库根目录优先，再是 src 目录。
2) 遇到 `ModuleNotFoundError: src / marketing_engine`，先检查本文件是否被误删或被移动。
3) 新增测试若依赖新顶层包，应在这里集中维护导入路径，不要在单个测试文件里零散改 sys.path。
"""

from __future__ import annotations

import sys
from pathlib import Path


def _ensure_path(path: Path) -> None:
    """将路径幂等地加入 sys.path 头部，避免重复注入。"""
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"

_ensure_path(REPO_ROOT)
_ensure_path(SRC_DIR)
