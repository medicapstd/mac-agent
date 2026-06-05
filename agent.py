import requests
import sys

SERVER = "http://127.0.0.1:8765"

COMMAND_MAP = {
    "battery": ("battery", {}),
    "open": lambda args: (
        "open_app",
        {"app": " ".join(args) if args else "Finder"}
    ),
    "downloads": ("folder_size", {"path": "~/Downloads"}),
    "tools": ("list_tools", {}),
"ultraclean": ("ultraclean", {}),
}

def main():
    if len(sys.argv) < 2:
        print("Usage: agent <command> [args...]")
        return

    cmd = sys.argv[1].lower()
    extra = sys.argv[2:]

    if cmd == "log":
        r = requests.get(f"{SERVER}/log")
        data = r.json()

        for entry in data["log"]:
            print(
                f"[{entry['time'][:19]}] "
                f"{entry['tool']} -> "
                f"{entry['result'][:60]}"
            )
        return

    mapping = COMMAND_MAP.get(cmd)

    if mapping is None:
        print(f"Unknown command: {cmd}")
        return

    if callable(mapping):
        tool, args = mapping(extra)
    else:
        tool, args = mapping

    r = requests.post(
        f"{SERVER}/run",
        json={"tool": tool, "args": args}
    )

    data = r.json()
    print(data.get("result", data.get("error", "No response")))

if __name__ == "__main__":
    main()
