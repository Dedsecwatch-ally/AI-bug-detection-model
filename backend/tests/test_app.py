import pytest
from fastapi.testclient import TestClient
import os
import sys
from pathlib import Path

# Ensure the project root is on sys.path so tests can import backend as a package
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Also add backend/src so local imports like `from model import ...` work
BACKEND_SRC = ROOT / "backend" / "src"
if str(BACKEND_SRC) not in sys.path:
    sys.path.insert(0, str(BACKEND_SRC))

# Import the app object
from backend.src.app import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def patch_generate_review(monkeypatch):
    # patch the model generate_review to avoid loading heavy models during tests
    def fake_generate_review(prompt, max_new_tokens=400):
        return "FAKE_REVIEW: found issue X"
    monkeypatch.setenv("BUG_MODEL", "dev")
    monkeypatch.setattr("backend.src.app.generate_review", fake_generate_review)
    yield


def test_review_success():
    payload = {"code": "def foo():\n    return 1"}
    res = client.post("/review", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "review" in data
    assert "static_report" in data
    assert data["review"].startswith("FAKE_REVIEW")


def test_missing_code():
    res = client.post("/review", json={})
    # FastAPI/Pydantic returns 422 for missing required fields (validation error)
    assert res.status_code == 422


def test_oversize_code():
    large = "a" * 25000
    res = client.post("/review", json={"code": large})
    assert res.status_code == 413
