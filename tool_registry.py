import subprocess
import os
from datetime import datetime

# ── Tier decorator ─────────────────────────────────────────
def tool(name: str, description: str, tier: int = 1):
    def decorator(fn):
        fn._tool_name = name
        fn._description = description
        fn._tier = tier
        return fn
    return decorator


# ── Tier 1 Tools (Auto-execute) ────────────────────────────

@tool("battery", "Get battery status and percentage", tier=1)
def get_battery(args: dict) -> str:
    result = subprocess.run(
        ["pmset", "-g", "batt"],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()


@tool("open_app", "Open any Mac application by name", tier=1)
def open_app(args: dict) -> str:
    app = args.get("app")

    if not app:
        return "Error: app name required"

    result = subprocess.run(
        ["open", "-a", app],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        return f"Opened {app}"

    return f"Failed to open {app}: {result.stderr}"


@tool("folder_size", "Get the size of a folder", tier=1)
def folder_size(args: dict) -> str:
    path = args.get("path", "~/Downloads")
    path = os.path.expanduser(path)

    result = subprocess.run(
        ["du", "-sh", path],
        capture_output=True,
        text=True
    )

    return result.stdout.strip()


@tool("list_folder", "List files in a folder", tier=1)
def list_folder(args: dict) -> str:
    path = args.get("path", "~/Downloads")
    path = os.path.expanduser(path)

    try:
        files = os.listdir(path)
        files = [f for f in files if not f.startswith(".")]

        return f"{len(files)} files in {path}:\n" + "\n".join(files[:20])

    except Exception as e:
        return f"Error: {e}"


@tool("system_info", "Get current Mac system snapshot", tier=1)
def system_info(args: dict) -> str:
    battery = subprocess.run(
        ["pmset", "-g", "batt"],
        capture_output=True,
        text=True
    ).stdout.strip()

    uptime = subprocess.run(
        ["uptime"],
        capture_output=True,
        text=True
    ).stdout.strip()

    return f"Battery:\n{battery}\n\nUptime:\n{uptime}"


@tool("list_tools", "List all available agent tools", tier=1)
def list_tools(args: dict) -> str:
    lines = []

    for name, meta in REGISTRY.items():
        tier_label = ["", "AUTO", "ASK", "BLOCKED"][meta["tier"]]
        lines.append(
            f"[T{meta['tier']}-{tier_label}] "
            f"{name}: {meta['description']}"
        )

    return "\n".join(lines)


# ── Tier 2 Tools (Ask first) ───────────────────────────────

@tool("delete_ds_store", "Delete all .DS_Store files from a path", tier=2)
def delete_ds_store(args: dict) -> str:
    path = os.path.expanduser(args.get("path", "~"))

    subprocess.run(
        ["find", path, "-name", ".DS_Store", "-delete"],
        capture_output=True,
        text=True
    )

    return f"Cleaned .DS_Store files from {path}"


@tool(
    "clean_downloads",
    "Delete files older than N days from Downloads (safe extensions only)",
    tier=2
)
def clean_downloads(args: dict) -> str:
    days = args.get("days", 30)

    downloads = os.path.expanduser("~/Downloads")

    safe_ext = {
        ".zip",
        ".dmg",
        ".pkg",
        ".tmp",
        ".crdownload",
        ".part"
    }

    deleted = []
    now = datetime.now().timestamp()

    for f in os.listdir(downloads):
        fpath = os.path.join(downloads, f)

        if not os.path.isfile(fpath):
            continue

        ext = os.path.splitext(f)[1].lower()
        age_days = (now - os.path.getmtime(fpath)) / 86400

        if ext in safe_ext and age_days > days:
            deleted.append(f)
            os.remove(fpath)

    if deleted:
        return f"Deleted {len(deleted)} files:\n" + "\n".join(deleted)

    return "Nothing to clean."


@tool("ultraclean", "Clean downloads and system junk", tier=2)
def ultraclean(args: dict) -> str:
    downloads = os.path.expanduser("~/Downloads")
    removed = []

    for f in os.listdir(downloads):
        path = os.path.join(downloads, f)

        if os.path.isfile(path):
            ext = os.path.splitext(f)[1].lower()

            if ext in [".zip", ".dmg", ".tmp", ".pkg"]:
                try:
                    os.remove(path)
                    removed.append(f)
                except:
                    pass

    return f"Ultraclean complete. Removed {len(removed)} files."


# ── Build Registry ─────────────────────────────────────────
import sys
import inspect

REGISTRY = {}

current_module = sys.modules[__name__]

for attr_name in dir(current_module):
    obj = getattr(current_module, attr_name)

    if callable(obj) and hasattr(obj, "_tool_name"):
        REGISTRY[obj._tool_name] = {
            "fn": obj,
            "description": obj._description,
            "tier": obj._tier
        }
