import os
import sys
import shutil

path = os.path.expanduser(sys.argv[1])

folders = {
    ".py": "Code",
    ".js": "Code",
    ".html": "Code",
    ".css": "Code",
    ".pdf": "Documents",
    ".docx": "Documents",
    ".txt": "Documents",
    ".png": "Images",
    ".jpg": "Images",
    ".jpeg": "Images",
    ".zip": "Archives",
    ".rar": "Archives"
}

for file in os.listdir(path):
    full = os.path.join(path, file)

    if os.path.isfile(full):
        ext = os.path.splitext(file)[1].lower()

        if ext in folders:
            target_folder = os.path.join(path, folders[ext])
            os.makedirs(target_folder, exist_ok=True)

            shutil.move(full, os.path.join(target_folder, file))
            print(f"Moved {file} -> {folders[ext]}")
