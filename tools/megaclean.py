import os
import shutil
from pathlib import Path

home = str(Path.home())

targets = [
    f"{home}/Desktop",
    f"{home}/Downloads",
    f"{home}/Documents",
]

mapping = {
    ".png":"Images", ".jpg":"Images", ".jpeg":"Images",
    ".pdf":"Documents", ".docx":"Documents", ".txt":"Documents",
    ".py":"Code", ".js":"Code", ".html":"Code", ".css":"Code",
    ".zip":"Archives", ".rar":"Archives",
    ".mp4":"Videos", ".mov":"Videos"
}

for folder in targets:
    if not os.path.exists(folder):
        continue

    print(f"\nCleaning {folder}")

    for item in os.listdir(folder):
        full = os.path.join(folder, item)

        if os.path.isfile(full):
            ext = os.path.splitext(item)[1].lower()

            if ext in mapping:
                target_dir = os.path.join(folder, mapping[ext])
                os.makedirs(target_dir, exist_ok=True)

                new_path = os.path.join(target_dir, item)

                if not os.path.exists(new_path):
                    shutil.move(full, new_path)
                    print(f"Moved {item} -> {mapping[ext]}")
