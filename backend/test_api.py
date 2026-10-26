import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from app.main import app

def run_api_tests():
    print("Testing FastAPI endpoints using TestClient...")
    with TestClient(app) as client:
        # Test root endpoint
        r0 = client.get("/")
        assert r0.status_code == 200, f"Root returned {r0.status_code}"
        print("[OK] Root endpoint returned 200 OK")

        # Test valid food: Milk
        r1 = client.post("/api/analyze-food", json={"food": "milk"})
        assert r1.status_code == 200, f"Milk returned {r1.status_code}"
        d1 = r1.json()
        assert d1["isFood"] is True
        assert d1["foodName"] == "Milk"
        assert len(d1["adulterants"]) > 0
        print(f"[OK] Valid food test passed: {d1['foodName']}, Adulterants count: {len(d1['adulterants'])}")

        # Test non-food: Laptop
        r2 = client.post("/api/analyze-food", json={"food": "laptop"})
        assert r2.status_code == 200, f"Laptop returned {r2.status_code}"
        d2 = r2.json()
        assert d2["isFood"] is False
        assert d2["classification"] == "non_food"
        assert len(d2["sources"]) >= 1
        assert "message" in d2
        print(f"[OK] Non-food rejection test passed: '{d2.get('foodName')}' -> {d2['message']}")

        # Test unknown item is not mislabeled as food or confirmed non-food
        r_unknown = client.post("/api/analyze-food", json={"food": "mystery gadget"})
        assert r_unknown.status_code == 200
        d_unknown = r_unknown.json()
        assert d_unknown["isFood"] is False
        assert d_unknown["classification"] == "uncertain"
        assert len(d_unknown["sources"]) >= 1
        print("[OK] Unknown item is marked uncertain and includes web search links")

        # Test recognized powder-based food
        r_chilli = client.post("/api/analyze-food", json={"food": "chilli powder"})
        assert r_chilli.status_code == 200
        assert r_chilli.json()["isFood"] is True
        assert r_chilli.json()["classification"] == "food"
        print("[OK] Chilli powder is recognized as food")

        # Test Dashboard stats
        r3 = client.get("/api/dashboard-stats")
        assert r3.status_code == 200
        d3 = r3.json()
        assert d3["surveySummary"]["awarePercentage"] == 65
        assert d3["surveySummary"]["unawarePercentage"] == 35
        print(f"[OK] Dashboard stats test passed: Aware {d3['surveySummary']['awarePercentage']}%, Unaware {d3['surveySummary']['unawarePercentage']}%")

        # Test chat endpoint
        r4 = client.post("/api/chat", json={"message": "Is turmeric safe?", "foodContext": "Turmeric"})
        assert r4.status_code == 200
        d4 = r4.json()
        assert len(d4["reply"]) > 10
        print(f"[OK] Chat endpoint passed: '{d4['reply'][:60]}...'")

        # Test foods list
        r5 = client.get("/api/foods")
        assert r5.status_code == 200
        assert len(r5.json()) >= 10
        print(f"[OK] Curated foods database passed: {len(r5.json())} food profiles loaded")

    print("\n>>> ALL API & SYSTEM ENDPOINTS PASSED WITH 100% SUCCESS! <<<")

if __name__ == "__main__":
    run_api_tests()
