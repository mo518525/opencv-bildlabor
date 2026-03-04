from __future__ import annotations

import argparse
from pathlib import Path
import sys

import cv2

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from utils.config_io import load_config, resolve_project_path

DEFAULT_CONFIG = Path(__file__).resolve().parents[3] / "configs" / "task_4_3.json"


def run(config_path: Path | None = None, show_windows: bool | None = None) -> Path:
    config_file = config_path or DEFAULT_CONFIG
    config = load_config(config_file)

    input_path = resolve_project_path(config.get("input_image", "data/task_4_3/yoshi_input.png"))
    mask_path = resolve_project_path(config.get("mask_image", "data/task_4_3/mask_input.png"))
    output_path = resolve_project_path(
        config.get("output_image", "outputs/task_4_3/yoshi_hue_output.png")
    )
    hue_value = int(config.get("hue_value", 90)) % 180

    effective_show = bool(config.get("show_windows", False))
    if show_windows is not None:
        effective_show = show_windows

    image = cv2.imread(str(input_path))
    mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)

    if image is None:
        raise FileNotFoundError(f"Input image not found: {input_path}")
    if mask is None:
        raise FileNotFoundError(f"Mask image not found: {mask_path}")
    if image.shape[:2] != mask.shape[:2]:
        raise ValueError(
            f"Mask and image dimensions differ. Image: {image.shape[:2]}, Mask: {mask.shape[:2]}"
        )

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    h[mask == 255] = hue_value
    modified = cv2.cvtColor(cv2.merge([h, s, v]), cv2.COLOR_HSV2BGR)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    success = cv2.imwrite(str(output_path), modified)
    if not success:
        raise RuntimeError(f"Failed to save output image: {output_path}")

    if effective_show:
        cv2.imshow("Mask", mask)
        cv2.imshow("Modified", modified)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    print(f"Saved: {output_path}")
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply hue shift in masked image regions.")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--show", dest="show_windows", action="store_true")
    parser.add_argument("--no-show", dest="show_windows", action="store_false")
    parser.set_defaults(show_windows=None)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(config_path=args.config, show_windows=args.show_windows)
