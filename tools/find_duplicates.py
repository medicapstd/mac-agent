import os
import sys
from collections import defaultdict

path = os.path.expanduser(sys.argv[1])

ignore_dirs = {
    "venv", ".venv", "__pycache__", "site-packages",
    ".git", "node_modules"
}

ignore_files = {
    ".DS_Store"
}

files = defaultdict(list)

for root, dirs, filenames in os.walk(path):
    dirs[:] = [d for d in dirs if d not in ignore_dirs]

    for f in filenames:
        if f in ignore_files:
            continue

        full = os.path.join(root, f)

        try:
            size = os.path.getsize(full)
        except:
            continue

        key = (f.lower(), size)
        files[key].append(full)

found = False

for key, group in files.items():
    if len(group) > 1:
        found = True
        print("\nPossible duplicates:")
        for item in group:
            print(item)

if not found:
    print("No useful duplicates found.")
