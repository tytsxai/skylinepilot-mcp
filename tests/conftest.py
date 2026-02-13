"""
测试环境公共引导。

职责：
1) 确保仓库根目录在 sys.path 中，便于导入根目录模块（如 marketing_engine）。
2) 确保 src 目录可被稳定导入（如 src.skylinepilot.*）。
"""

from __future__ import annotations

import sys
from pathlib import Path


def _ensure_path(path: Path) -> None:
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"

_ensure_path(REPO_ROOT)
_ensure_path(SRC_DIR)

