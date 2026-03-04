from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[3]


def resolve_project_path(value: str | Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


def load_config(config_path: str | Path) -> dict[str, Any]:
    path = resolve_project_path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open("r", encoding="utf-8-sig") as file_handle:
        data = json.load(file_handle)

    if not isinstance(data, dict):
        raise ValueError(f"Config must contain a mapping at top level: {path}")

    return data
