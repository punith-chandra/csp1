import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database.db import init_db, get_recent_searches, get_survey_statistics
from app.services.food_service import analyze_food_item
from app.services.gemini_service import chat_with_food_safety_ai

def run_tests():
    print("1. Initializing SQLite Database...")
    init_db()
    print("   Database initialized successfully!")

    print("\n2. Testing Food Item: 'Milk'...")
    milk_res = analyze_food_item("milk")
    assert milk_res["isFood"] is True, "Expected Milk to be recognized as food"
    assert "adulterants" in milk_res
    print(f"   Success! Food: {milk_res['foodName']}, Adulterants: {len(milk_res['adulterants'])} found")
    print(f"   Test Method: {milk_res['testMethod']}")

    print("\n3. Testing Non-Food Item: 'Laptop'...")
    laptop_res = analyze_food_item("laptop")
    assert laptop_res["isFood"] is False, "Expected Laptop to be rejected"
    print(f"   Success! Message: {laptop_res['message']}")

    print("\n4. Testing Food Item: 'Turmeric'...")
    turmeric_res = analyze_food_item("turmeric")
    assert turmeric_res["isFood"] is True
    print(f"   Success! Observation: {turmeric_res['observation'][:60]}...")

    print("\n4b. Testing Powder-based food item: 'Chilli Powder'...")
    chilli_res = analyze_food_item("chilli powder")
    assert chilli_res["isFood"] is True, "Expected chilli powder to be recognized as food"
    assert chilli_res["foodName"].lower() == "chilli powder"
    print(f"   Success! Food: {chilli_res['foodName']}, Adulterants: {len(chilli_res['adulterants'])} found")

    print("\n5. Testing AI Chat fallback...")
    chat_reply = chat_with_food_safety_ai("What are the health risks of adulterated food?")
    assert len(chat_reply) > 20
    print(f"   Chat reply preview: {chat_reply[:70]}...")

    print("\n6. Checking SQLite search history & survey metrics...")
    stats = get_survey_statistics()
    print(f"   Aware %: {stats['metrics'].get('aware_percentage')}%")
    print(f"   Unaware %: {stats['metrics'].get('unaware_percentage')}%")
    print(f"   Recent searches logged in DB: {len(get_recent_searches())}")

    print("\n>>> ALL BACKEND TESTS PASSED CLEANLY! <<<")

if __name__ == "__main__":
    run_tests()
