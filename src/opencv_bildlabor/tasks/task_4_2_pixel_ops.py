from __future__ import annotations

import argparse
from pathlib import Path
import sys

import cv2
import numpy as np

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from utils.config_io import load_config, resolve_project_path

DEFAULT_CONFIG = Path(__file__).resolve().parents[3] / "configs" / "task_4_2.json"


def _draw_center_square(image: np.ndarray, size: int, color_bgr: list[int]) -> None:
    h, w = image.shape[:2]
    size = max(1, int(size))

    x0 = max(0, (w - size) // 2)
    y0 = max(0, (h - size) // 2)
    x1 = min(w, x0 + size)
    y1 = min(h, y0 + size)
    image[y0:y1, x0:x1] = np.asarray(color_bgr, dtype=np.uint8)


def run(config_path: Path | None = None, show_windows: bool | None = None) -> Path:
    config_file = config_path or DEFAULT_CONFIG
    config = load_config(config_file)

    input_path = resolve_project_path(config.get("input_image", "data/task_4_2/yoshi_input.png"))
    output_path = resolve_project_path(
        config.get("output_image", "outputs/task_4_2/yoshi_output.png")
    )

    square_cfg = config.get("center_square", {})
    square_size = int(square_cfg.get("size", 10))
    square_color = square_cfg.get("color_bgr", [0, 0, 255])
    row_step = int(config.get("black_row_step", 5))

    effective_show = bool(config.get("show_windows", False))
    if show_windows is not None:
        effective_show = show_windows

    image = cv2.imread(str(input_path))
    if image is None:
        raise FileNotFoundError(f"Input image not found: {input_path}")

    modified = image.copy()
    _draw_center_square(modified, square_size, square_color)
    if row_step > 0:
        modified[::row_step, :, :] = 0

    output_path.parent.mkdir(parents=True, exist_ok=True)
    success = cv2.imwrite(str(output_path), modified)
    if not success:
        raise RuntimeError(f"Failed to save output image: {output_path}")

    if effective_show:
        cv2.imshow("Original", image)
        cv2.imshow("Modified", modified)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    print(f"Saved: {output_path}")
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply pixel operations to an image.")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--show", dest="show_windows", action="store_true")
    parser.add_argument("--no-show", dest="show_windows", action="store_false")
    parser.set_defaults(show_windows=None)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(config_path=args.config, show_windows=args.show_windows)
