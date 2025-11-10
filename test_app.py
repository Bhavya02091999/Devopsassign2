import os
import json
import pytest
from app import app, STORE_PATH

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        orig = None
        if os.path.exists(STORE_PATH):
            with open(STORE_PATH, "r") as f:
                orig = f.read()
        with open(STORE_PATH, "w") as f:
            json.dump({"Warm-up": [], "Workout": [], "Cool-down": []}, f)
        yield c
        if orig is not None:
            with open(STORE_PATH, "w") as f:
                f.write(orig)

def test_health(client):
    rv = client.get("/health")
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["status"] == "ok"

def test_log_and_summary(client):
    payload = {"category": "Workout", "exercise": "Push-ups", "duration": 15}
    rv = client.post("/log", json=payload)
    assert rv.status_code == 201
    data = rv.get_json()
    assert data["entry"]["exercise"] == "Push-ups"

    rv2 = client.get("/summary")
    assert rv2.status_code == 200
    s = rv2.get_json()
    assert s["totals"]["Workout"] == 15
    assert s["total_time"] == 15

def test_invalid_category(client):
    rv = client.post("/log", json={"category": "Yoga", "exercise": "A", "duration": 10})
    assert rv.status_code == 400