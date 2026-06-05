import sys

path = sys.argv[1]
content = sys.argv[2]

with open(path, "w") as f:
    f.write(content)

print("Written successfully.")
