# ~/Documents/All_Projects/AI_Agents/Mac_Agent/agent_server.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import sqlite3
import os
from datetime import datetime
from tool_registry import REGISTRY

app = FastAPI()
DB_PATH = os.path.expanduser("~/Documents/All_Projects/AI_Agents/Mac_Agent/agent_memory.db")

# ── Database ───────────────────────────────────────────────
def init_db():
    con = sqlite3.connect(DB_PATH)
    con.execute("""
        CREATE TABLE IF NOT EXISTS action_log (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp   TEXT NOT NULL,
            tool        TEXT NOT NULL,
            args        TEXT,
            tier        INTEGER,
            result      TEXT,
            confirmed   INTEGER DEFAULT 1,
            duration_ms INTEGER
        )
    """)
    con.commit()
    con.close()

def log_action(tool, args, tier, result, confirmed=1, duration_ms=0):
    con = sqlite3.connect(DB_PATH)
    con.execute(
        "INSERT INTO action_log VALUES (NULL,?,?,?,?,?,?,?)",
        (datetime.now().isoformat(), tool, str(args), 
         tier, str(result)[:500], confirmed, duration_ms)
    )
    con.commit()
    con.close()

# ── Permission check ───────────────────────────────────────
def confirm_tier2(tool_name: str, args: dict, preview: str) -> bool:
    """Block and ask via macOS dialog. Returns True if confirmed."""
    import subprocess
    msg = f"Agent wants to run: {tool_name}\\n\\n{preview}\\n\\nAllow?"
    script = f'display dialog "{msg}" buttons {{"Cancel", "Allow"}} default button "Cancel"'
    result = subprocess.run(["osascript", "-e", script], capture_output=True)
    return result.returncode == 0  # 0 = clicked Allow

# ── Core endpoint ──────────────────────────────────────────
@app.post("/run")
async def run_tool(request: Request):
    body = await request.json()
    tool_name = body.get("tool")
    args = body.get("args", {})

    if not tool_name:
        return JSONResponse({"error": "tool name required"}, status_code=400)

    if tool_name not in REGISTRY:
        return JSONResponse({"error": f"Unknown tool: {tool_name}"}, status_code=404)

    meta = REGISTRY[tool_name]
    tier = meta["tier"]

    # Hard block
    if tier == 3:
        log_action(tool_name, args, tier, "BLOCKED", confirmed=0)
        return JSONResponse({"error": "Blocked: outside permission boundary."})

    # Tier 2: ask first
    if tier == 2:
        preview = f"Args: {args}"
        allowed = confirm_tier2(tool_name, args, preview)
        if not allowed:
            log_action(tool_name, args, tier, "CANCELLED", confirmed=0)
            return JSONResponse({"result": "Cancelled by user."})

    # Execute
    start = datetime.now()
    try:
        result = meta["fn"](args)
    except Exception as e:
        result = f"Tool error: {e}"

    duration_ms = int((datetime.now() - start).total_seconds() * 1000)
    log_action(tool_name, args, tier, result, confirmed=1, duration_ms=duration_ms)

    return JSONResponse({"tool": tool_name, "result": result, "tier": tier})

# ── Utility endpoints ──────────────────────────────────────
@app.get("/ping")
def ping():
    return {"status": "alive", "agent": "Mridul Agent v1", 
            "tools": len(REGISTRY)}

@app.get("/log")
def get_log(limit: int = 20):
    con = sqlite3.connect(DB_PATH)
    rows = con.execute(
        "SELECT timestamp, tool, tier, result, duration_ms FROM action_log "
        "ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    con.close()
    return {"log": [
        {"time": r[0], "tool": r[1], "tier": r[2], 
         "result": r[3][:100], "ms": r[4]} 
        for r in rows
    ]}

@app.get("/tools")
def list_tools():
    return {"tools": [
        {"name": n, "tier": m["tier"], "description": m["description"]}
        for n, m in REGISTRY.items()
    ]}

if __name__ == "__main__":
    import os
    init_db()
    print(f"Agent starting with {len(REGISTRY)} tools registered.")
    uvicorn.run(app, host="127.0.0.1", port=8765, reload=False)
