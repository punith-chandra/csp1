import logging
import re
from difflib import SequenceMatcher
from typing import Any, Dict, Optional
from urllib.parse import quote

import httpx

logger = logging.getLogger(__name__)

OPEN_FOOD_FACTS_SEARCH_URL = "https://world.openfoodfacts.org/cgi/search.pl"


def _normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def _product_match_score(query: str, product_name: str) -> float:
    normalized_query = _normalize(query)
    normalized_name = _normalize(product_name)
    if not normalized_query or not normalized_name:
        return 0.0
    if normalized_query == normalized_name:
        return 1.0
    if normalized_query in normalized_name:
        return min(0.9, len(normalized_query) / len(normalized_name) + 0.3)
    query_words = set(normalized_query.split())
    name_words = set(normalized_name.split())
    if query_words and query_words.issubset(name_words):
        return 0.8
    return SequenceMatcher(None, normalized_query, normalized_name).ratio()


def find_global_food_product(query: str) -> Optional[Dict[str, Any]]:
    """Find a matching packaged food product in the global Open Food Facts catalog."""
    try:
        response = httpx.get(
            OPEN_FOOD_FACTS_SEARCH_URL,
            params={
                "search_terms": query,
                "search_simple": 1,
                "action": "process",
                "json": 1,
                "page_size": 8,
                "fields": (
                    "product_name,brands,categories,countries,ingredients_text,"
                    "code,url,nutrition_grades,nutriments"
                ),
            },
            headers={"User-Agent": "FoodPureAI/1.0 (food safety awareness project)"},
            timeout=4.0,
        )
        response.raise_for_status()
        products = response.json().get("products", [])
    except (httpx.HTTPError, ValueError) as exc:
        logger.warning("Open Food Facts lookup failed for %r: %s", query, exc)
        return None

    candidates = []
    for product in products:
        name = (product.get("product_name") or "").strip()
        score = _product_match_score(query, name)
        if name and score >= 0.62:
            candidates.append((score, product))
    if not candidates:
        return None

    _, product = max(candidates, key=lambda candidate: candidate[0])
    product_name = product.get("product_name", "").strip()
    product_url = product.get("url") or (
        f"https://world.openfoodfacts.org/product/{quote(str(product.get('code', '')))}"
        if product.get("code")
        else "https://world.openfoodfacts.org/"
    )
    nutriments = product.get("nutriments") or {}
    nutrition_fields = {
        "energyKcal": "energy-kcal_100g",
        "proteinsG": "proteins_100g",
        "carbohydratesG": "carbohydrates_100g",
        "sugarsG": "sugars_100g",
        "fatG": "fat_100g",
        "fiberG": "fiber_100g",
        "saltG": "salt_100g",
    }
    return {
        "name": product_name,
        "brand": (product.get("brands") or "").strip(),
        "category": (product.get("categories") or "").split(",")[0].strip(),
        "countries": (product.get("countries") or "").strip(),
        "ingredients": (product.get("ingredients_text") or "").strip()[:500],
        "barcode": (product.get("code") or "").strip(),
        "nutritionGrade": (product.get("nutrition_grades") or "").strip().upper(),
        "nutritionPer100g": {
            label: nutriments[key]
            for label, key in nutrition_fields.items()
            if nutriments.get(key) not in (None, "")
        },
        "url": product_url,
    }
