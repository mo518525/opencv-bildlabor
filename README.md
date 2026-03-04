# opencv-bildlabor

Saubere OpenCV-Projektstruktur mit drei klar zugeordneten Aufgaben.

## Struktur

```text
src/opencv_bildlabor/tasks/
  task_4_2_pixel_ops.py
  task_4_3_masked_hue_shift.py
  task_4_4_lab_color_transfer.py

configs/
  task_4_2.json
  task_4_3.json
  task_4_4.json

data/
  task_4_2/yoshi_input.png
  task_4_3/yoshi_input.png
  task_4_3/mask_input.png
  task_4_4/input_source.png
  task_4_4/target_source.png

outputs/
  task_4_2/yoshi_output.png
  task_4_3/yoshi_hue_output.png
  task_4_4/color_transfer_output.png
```

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## Ausfuehren

Dispatcher:

```powershell
python src/opencv_bildlabor/run.py --task task_4_2 --no-show
python src/opencv_bildlabor/run.py --task task_4_3 --no-show
python src/opencv_bildlabor/run.py --task task_4_4 --no-show
```

Direkt pro Aufgabe:

```powershell
python src/opencv_bildlabor/tasks/task_4_2_pixel_ops.py --config configs/task_4_2.json --no-show
python src/opencv_bildlabor/tasks/task_4_3_masked_hue_shift.py --config configs/task_4_3.json --no-show
python src/opencv_bildlabor/tasks/task_4_4_lab_color_transfer.py --config configs/task_4_4.json --no-show
```

## Zuordnung Aufgabe -> Code -> Dateien

| Aufgabe | Script | Inputs | Output |
|---|---|---|---|
| 4.2 | `task_4_2_pixel_ops.py` | `data/task_4_2/yoshi_input.png` | `outputs/task_4_2/yoshi_output.png` |
| 4.3 | `task_4_3_masked_hue_shift.py` | `data/task_4_3/yoshi_input.png`, `data/task_4_3/mask_input.png` | `outputs/task_4_3/yoshi_hue_output.png` |
| 4.4 | `task_4_4_lab_color_transfer.py` | `data/task_4_4/input_source.png`, `data/task_4_4/target_source.png` | `outputs/task_4_4/color_transfer_output.png` |
