import os
import sys
from collections import Counter

path = os.path.expanduser(sys.argv[1])

if not os.path.exists(path):
    print("Path not found.")
    sys.exit()

files = []
types = Counter()

for root, dirs, filenames in os.walk(path):
    for f in filenames:
        files.append(f)
        ext = os.path.splitext(f)[1].lower() or "[no extension]"
        types[ext] += 1

print(f"Scanned: {path}")
print(f"Total files: {len(files)}")
print("\nTop file types:")

for ext, count in types.most_common(10):
    print(f"{ext}: {count}")
