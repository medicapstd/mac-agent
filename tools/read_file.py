import sys

path = sys.argv[1]

with open(path, "r") as f:
    print(f.read())
