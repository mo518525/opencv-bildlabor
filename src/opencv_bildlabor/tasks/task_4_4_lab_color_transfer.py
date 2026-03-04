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

DEFAULT_CONFIG = Path(__file__).resolve().parents[3] / "configs" / "task_4_4.json"


def _match_channel(channel_in: np.ndarray, channel_target: np.ndarray) -> np.ndarray:
    mean_in, std_in = channel_in.mean(), channel_in.std()
    mean_target, std_target = channel_target.mean(), channel_target.std()

    std_in = std_in if std_in > 1e-6 else 1.0
    std_target = std_target if std_target > 1e-6 else 1.0

    normalized = (channel_in - mean_in) / std_in
    return normalized * std_target + mean_target


def run(config_path: Path | None = None, show_windows: bool | None = None) -> Path:
    config_file = config_path or DEFAULT_CONFIG
    config = load_config(config_file)

    input_path = resolve_project_path(config.get("input_image", "data/task_4_4/input_source.png"))
    target_path = resolve_project_path(config.get("target_image", "data/task_4_4/target_source.png"))
    output_path = resolve_project_path(
        config.get("output_image", "outputs/task_4_4/color_transfer_output.png")
    )

    effective_show = bool(config.get("show_windows", False))
    if show_windows is not None:
        effective_show = show_windows

    input_img = cv2.imread(str(input_path))
    target_img = cv2.imread(str(target_path))
    if input_img is None:
        raise FileNotFoundError(f"Input image not found: {input_path}")
    if target_img is None:
        raise FileNotFoundError(f"Target image not found: {target_path}")

    input_float = input_img.astype(np.float32) / 255.0
    target_float = target_img.astype(np.float32) / 255.0

    input_lab = cv2.cvtColor(input_float, cv2.COLOR_BGR2Lab)
    target_lab = cv2.cvtColor(target_float, cv2.COLOR_BGR2Lab)

    l_in, a_in, b_in = cv2.split(input_lab)
    l_target, a_target, b_target = cv2.split(target_lab)

    l_new = _match_channel(l_in, l_target)
    a_new = _match_channel(a_in, a_target)
    b_new = _match_channel(b_in, b_target)

    transferred_lab = cv2.merge([l_new, a_new, b_new])
    transferred_bgr = cv2.cvtColor(transferred_lab, cv2.COLOR_Lab2BGR)

    transferred_bgr = np.clip(transferred_bgr, 0, 1)
    output_uint8 = (transferred_bgr * 255).astype(np.uint8)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    success = cv2.imwrite(str(output_path), output_uint8)
    if not success:
        raise RuntimeError(f"Failed to save output image: {output_path}")

    if effective_show:
        cv2.imshow("Input", input_img)
        cv2.imshow("Target", target_img)
        cv2.imshow("Color Transfer", output_uint8)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    print(f"Saved: {output_path}")
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply Lab color transfer.")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--show", dest="show_windows", action="store_true")
    parser.add_argument("--no-show", dest="show_windows", action="store_false")
    parser.set_defaults(show_windows=None)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(config_path=args.config, show_windows=args.show_windows)
