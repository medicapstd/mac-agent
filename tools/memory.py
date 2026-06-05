import sys, json, os

mem_file = os.path.expanduser("~/Documents/All_Projects/AI_Agents/Mac_Agent/memory/data.json")

if not os.path.exists(mem_file):
    with open(mem_file, "w") as f:
        json.dump({}, f)

with open(mem_file, "r") as f:
    data = json.load(f)

action = sys.argv[1]

if action == "set":
    key = sys.argv[2]
    value = sys.argv[3]
    data[key] = value
    with open(mem_file, "w") as f:
        json.dump(data, f, indent=2)
    print("Saved.")

elif action == "get":
    key = sys.argv[2]
    print(data.get(key, "Not found"))

elif action == "all":
    print(json.dumps(data, indent=2))
