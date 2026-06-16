#!/usr/bin/env python3
"""Ensure GFE-matching subfolder tree for every supermodel in MAGAZINE."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
MAGAZINE_ROOT = SCRIPTS_DIR.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from supermodel_roster_data import SUPERMODEL_NAMES, SUPERMODEL_ROSTER_10

# Mirrors GFE actor layout (Studio/GFE/{Name}/...)
MODEL_SUBFOLDERS = (
    "01_casting_shots",
    "02_reference_views",
    "SCENES",
    "VARIATIONS",
    "CLIPS",
    "PROMOTIONAL",
    "STAGED SHOTS",
)

FLAT_PROMPTS_DIR = MAGAZINE_ROOT / "prompts"


def ensure_model_dirs(model_name: str) -> list[Path]:
    base = MAGAZINE_ROOT / model_name
    created: list[Path] = []
    for sub in MODEL_SUBFOLDERS:
        path = base / sub
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            created.append(path)
        else:
            path.mkdir(parents=True, exist_ok=True)
    return created


def relocate_flat_prompts(model_name: str) -> list[Path]:
    moved: list[Path] = []
    pairs = (
        (f"{model_name}_Supermodel_Magazine_studio.txt", "01_casting_shots"),
        (f"{model_name}_Supermodel_Magazine_runway.txt", "02_reference_views"),
    )
    for filename, subfolder in pairs:
        src = FLAT_PROMPTS_DIR / filename
        if not src.exists():
            continue
        dst = MAGAZINE_ROOT / model_name / subfolder / filename
        if dst.exists():
            continue
        shutil.move(str(src), str(dst))
        moved.append(dst)
    return moved


def main() -> int:
    print(f"MAGAZINE folder structure — {MAGAZINE_ROOT}\n")
    total_new = 0
    total_moved = 0
    for model in SUPERMODEL_ROSTER_10:
        name = model["name"]
        created = ensure_model_dirs(name)
        moved = relocate_flat_prompts(name)
        total_new += len(created)
        total_moved += len(moved)
        folder_status = f"+{len(created)} new" if created else "ok"
        move_status = f", moved {len(moved)} prompt(s)" if moved else ""
        print(f"  {name}: {folder_status}{move_status}")
    print(f"\nModels: {len(SUPERMODEL_NAMES)} | New folders: {total_new} | Prompts relocated: {total_moved}")
    return 0


if __name__ == "__main__":
    sys.exit(main())