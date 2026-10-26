import logging
import re
from difflib import SequenceMatcher
from typing import Dict, Optional
from urllib.parse import quote

import httpx

logger = logging.getLogger(__name__)

WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"
WIKIPEDIA_SUMMARY_URL = "https://en.wikipedia.org/api/rest_v1/page/summary/"
FOOD_TERMS = re.compile(
    r"\b(food|edible|fruit|vegetable|grain|cereal|spice|ingredient|dish|"
    r"beverage|drink|meat|fish|seafood|legume|seed|nut|dairy|cheese|oil)\b",
    re.IGNORECASE,
)


def _normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def find_wikipedia_food_information(query: str) -> Optional[Dict[str, str]]:
    """Return an introductory reference only when the result appears food-related."""
    headers = {"User-Agent": "FoodPureAI/1.0 (food safety awareness project)"}
    try:
        search_response = httpx.get(
            WIKIPEDIA_API_URL,
            params={
                "action": "query",
                "list": "search",
                "srsearch": query,
                "srnamespace": 0,
                "srlimit": 5,
                "format": "json",
            },
            headers=headers,
            timeout=3.0,
        )
        search_response.raise_for_status()
        results = search_response.json().get("query", {}).get("search", [])
        normalized_query = _normalize(query)
        candidates = []
        for result in results:
            title = result.get("title", "")
            normalized_title = _normalize(title)
            score = SequenceMatcher(None, normalized_query, normalized_title).ratio()
            if normalized_query and normalized_query in normalized_title:
                score = max(score, 0.8)
            if title and score >= 0.55:
                candidates.append((score, result))
        if not candidates:
            return None

        _, match = max(candidates, key=lambda candidate: candidate[0])
        title = match["title"]
        summary_response = httpx.get(
            f"{WIKIPEDIA_SUMMARY_URL}{quote(title.replace(' ', '_'), safe='')}",
            headers=headers,
            timeout=3.0,
        )
        summary_response.raise_for_status()
        summary = summary_response.json()
    except (httpx.HTTPError, ValueError, KeyError) as exc:
        logger.warning("Wikipedia food lookup failed for %r: %s", query, exc)
        return None

    extract = (summary.get("extract") or "").strip()
    if not extract or not FOOD_TERMS.search(extract):
        return None

    article_url = (
        summary.get("content_urls", {})
        .get("desktop", {})
        .get("page")
    )
    if not article_url:
        article_url = f"https://en.wikipedia.org/wiki/{quote(title.replace(' ', '_'))}"

    return {
        "title": summary.get("title") or title,
        "summary": extract[:1200],
        "url": article_url,
    }
