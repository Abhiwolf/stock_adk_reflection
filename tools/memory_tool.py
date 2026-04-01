import json
import os
from datetime import datetime

MEMORY_FILE = "portfolio_memory.json"


def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            try:
                raw = f.read().strip()
                if not raw:
                    raise json.JSONDecodeError("Empty file", raw, 0)
                return json.loads(raw)
            except json.JSONDecodeError:
                # Treat corrupt or empty file as no memory
                return {"positions": {}, "history": []}
    return {"positions": {}, "history": []}


def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


def update_memory(memory, ticker, decision_text):

    memory["positions"][ticker] = {
        "last_decision": decision_text,
        "timestamp": datetime.utcnow().isoformat()
    }

    memory["history"].append({
        "ticker": ticker,
        "decision": decision_text,
        "timestamp": datetime.utcnow().isoformat()
    })

    return memory