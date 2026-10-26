import logging
import os
import re
from difflib import SequenceMatcher
from typing import Any, Dict, Optional

import httpx

logger = logging.getLogger(__name__)

USDA_SEARCH_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
NUTRIENTS = {
    1008: "energy",
    1003: "protein",
    1004: "totalFat",
    1005: "carbohydrates",
    1079: "fiber",
    2000: "totalSugars",
    1093: "sodium",
}
DATA_TYPE_PRIORITY = {
    "foundation": 3,
    "sr legacy": 2,
    "survey (fndds)": 1,
    "branded": 0,
}


def _normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def find_usda_food_nutrition(query: str) -> Optional[Dict[str, Any]]:
    """Find a matching USDA food record and its available nutrient values."""
    api_key = os.getenv("USDA_API_KEY", "DEMO_KEY").strip()
    try:
        response = httpx.get(
            USDA_SEARCH_URL,
            params={
                "query": query,
                "api_key": api_key,
                "pageSize": 10,
            },
            timeout=5.0,
        )
        response.raise_for_status()
        foods = response.json().get("foods", [])
    except (httpx.HTTPError, ValueError) as exc:
        logger.warning("USDA FoodData Central lookup failed for %r: %s", query, exc)
        return None

    normalized_query = _normalize(query)
    query_words = set(normalized_query.split())
    candidates = []
    for food in foods:
        description = food.get("description", "")
        normalized_description = _normalize(description)
        if not normalized_description:
            continue
        description_words = set(normalized_description.split())
        if query_words and query_words.issubset(description_words):
            score = 1.0
        else:
            word_coverage = (
                len(query_words & description_words) / len(query_words)
                if query_words
                else 0
            )
            fuzzy_score = SequenceMatcher(
                None, normalized_query, normalized_description
            ).ratio()
            score = max(word_coverage, fuzzy_score)
        if score >= 0.78:
            data_type = (food.get("dataType") or "").lower()
            candidates.append((
                score,
                DATA_TYPE_PRIORITY.get(data_type, 0),
                food,
            ))
    if not candidates:
        return None

    _, _, food = max(candidates, key=lambda candidate: (candidate[0], candidate[1]))
    nutrients = {}
    for nutrient in food.get("foodNutrients", []):
        name = NUTRIENTS.get(nutrient.get("nutrientId"))
        value = nutrient.get("value")
        if name and value is not None:
            nutrients[name] = {
                "value": value,
                "unit": nutrient.get("unitName", ""),
            }

    food_id = food.get("fdcId")
    return {
        "description": food.get("description", ""),
        "category": food.get("foodCategory", ""),
        "dataType": food.get("dataType", ""),
        "nutritionPer100g": nutrients,
        "url": (
            f"https://fdc.nal.usda.gov/food-details/{food_id}/nutrients"
            if food_id
            else "https://fdc.nal.usda.gov/"
        ),
    }
