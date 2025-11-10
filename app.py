from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

APP_ROOT = os.path.dirname(__file__)
STORE_PATH = os.path.join(APP_ROOT, "store.json")
VERSION_FILE = os.path.join(APP_ROOT, "version.txt")

def load_store():
    if not os.path.exists(STORE_PATH):
        initial = {"Warm-up": [], "Workout": [], "Cool-down": []}
        with open(STORE_PATH, "w") as f:
            json.dump(initial, f)
        return initial
    with open(STORE_PATH, "r") as f:
        return json.load(f)

def save_store(store):
    with open(STORE_PATH, "w") as f:
        json.dump(store, f, indent=2)

app = Flask(__name__)
store = load_store()

@app.route("/")
def index():
    version = "unknown"
    try:
        with open(VERSION_FILE, "r") as vf:
            version = vf.read().strip()
    except Exception:
        pass
    return jsonify({
        "app": "ACEest Fitness API",
        "version": version,
        "endpoints": ["/log (POST)", "/summary (GET)", "/health"]
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok", "time": datetime.utcnow().isoformat()})

@app.route("/log", methods=["POST"])
def log_session():
    data = request.json or {}
    category = data.get("category")
    exercise = data.get("exercise")
    duration = data.get("duration")

    if category not in ["Warm-up", "Workout", "Cool-down"]:
        return jsonify({"error": "invalid category"}), 400
    if not exercise or not isinstance(duration, int) or duration <= 0:
        return jsonify({"error": "invalid payload"}), 400

    entry = {
        "exercise": exercise,
        "duration": duration,
        "timestamp": datetime.utcnow().isoformat()
    }
    store = load_store()
    store[category].append(entry)
    save_store(store)
    return jsonify({"message": "logged", "entry": entry}), 201

@app.route("/summary", methods=["GET"])
def summary():
    store = load_store()
    totals = {cat: sum(e["duration"] for e in entries) for cat, entries in store.items()}
    total_time = sum(totals.values())
    return jsonify({"totals": totals, "total_time": total_time, "sessions": store})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)