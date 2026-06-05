import os
import sys
from collections import Counter

path = os.path.expanduser(sys.argv[1])

if not os.path.exists(path):
    print("Path not found.")
    sys.exit()

types = Counter()
total = 0

for root, dirs, files in os.walk(path):
    for f in files:
        total += 1
        ext = os.path.splitext(f)[1].lower() or "[no extension]"
        types[ext] += 1

print(f"Folder: {path}")
print(f"Total files: {total}")
print("\nTop file types:")

for ext, count in types.most_common(10):
    print(f"{ext}: {count}")
