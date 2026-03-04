from __future__ import annotations

import argparse
from pathlib import Path
from typing import Callable

from tasks.task_4_2_pixel_ops import run as run_task_4_2_pixel_ops
from tasks.task_4_3_masked_hue_shift import run as run_task_4_3_masked_hue_shift
from tasks.task_4_4_lab_color_transfer import run as run_task_4_4_lab_color_transfer

Runner = Callable[[Path | None, bool | None], Path]

TASKS: dict[str, Runner] = {
    "task_4_2": run_task_4_2_pixel_ops,
    "task_4_3": run_task_4_3_masked_hue_shift,
    "task_4_4": run_task_4_4_lab_color_transfer,
    "pixel_ops": run_task_4_2_pixel_ops,
    "masked_hue_shift": run_task_4_3_masked_hue_shift,
    "lab_color_transfer": run_task_4_4_lab_color_transfer,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run one OpenCV task.")
    parser.add_argument("--task", required=True, choices=sorted(TASKS.keys()))
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Optional config path. Defaults to the task-specific config file.",
    )
    parser.add_argument("--show", dest="show_windows", action="store_true")
    parser.add_argument("--no-show", dest="show_windows", action="store_false")
    parser.set_defaults(show_windows=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_path = TASKS[args.task](config_path=args.config, show_windows=args.show_windows)
    print(f"Task '{args.task}' finished. Output: {output_path}")


if __name__ == "__main__":
    main()
