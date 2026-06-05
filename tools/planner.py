import sys

goal = " ".join(sys.argv[1:])

steps = [
    f"Goal: {goal}",
    "1. Understand the request",
    "2. Identify needed tools",
    "3. Break into small actions",
    "4. Execute step by step",
    "5. Verify result",
    "6. Save useful memory"
]

for s in steps:
    print(s)
