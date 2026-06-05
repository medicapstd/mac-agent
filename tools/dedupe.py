import os
import sys
import shutil
from collections import defaultdict

path = os.path.expanduser(sys.argv[1])
trash = os.path.expanduser("~/TrashDuplicates")

os.makedirs(trash, exist_ok=True)

files = defaultdict(list)

for root, dirs, filenames in os.walk(path):
    dirs[:] = [d for d in dirs if d not in {".venv","venv","__pycache__",".git","node_modules"}]

    for f in filenames:
        if f == ".DS_Store":
            continue

        full = os.path.join(root, f)
        try:
            size = os.path.getsize(full)
        except:
            continue

        key = (f.lower(), size)
        files[key].append(full)

moved = 0

for key, group in files.items():
    if len(group) > 1:
        keep = group[0]
        for dup in group[1:]:
            target = os.path.join(trash, os.path.basename(dup))
            shutil.move(dup, target)
            print(f"Moved duplicate: {dup}")
            moved += 1

print(f"\nTotal moved: {moved}")
print(f"Saved in: {trash}")
