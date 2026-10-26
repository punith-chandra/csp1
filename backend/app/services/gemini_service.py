import os
import json
import logging
from typing import Optional, Dict, Any, List
import httpx
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()

SYSTEM_PROMPT = """
You are 'Food Safety AI', an intelligent, trustworthy Food Adulteration Awareness Assistant developed for the Community Service Project 'FROM FARM TO FORK' by students of Sri Vasavi Engineering College (Autonomous), Tanuku.

CRITICAL RULES & SAFETY GUIDELINES:
1. Do NOT claim that a simple home test scientifically proves adulteration.
2. Always use cautious wording:
   - "Preliminary awareness check"
   - "Possible indication"
   - "Laboratory testing is required for confirmation."
3. Strictly avoid dangerous chemical experiments or unsafe handling procedures.
4. If the user input is NOT a food item (e.g. laptop, chair, car, phone), explicitly state that it is not a food item.
5. Base food safety answers on trusted authorities: FSSAI (Food Safety and Standards Authority of India), WHO, FAO, CSIR-CFTRI, and AGMARK.
6. Use plain language for a general audience. Explain unfamiliar terms and give short numbered steps when a process is requested.
7. Tone must be professional, objective, encouraging, and educational.
"""

def generate_with_gemini_raw(prompt: str) -> Optional[str]:
    """Calls Gemini REST API via httpx using GOOGLE_API_KEY if configured."""
    api_key = os.getenv("GOOGLE_API_KEY", "").strip()
    if not api_key or api_key == "your_api_key_here":
        return None

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 1024
        }
    }

    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "")
            else:
                logger.warning(f"Gemini API returned status {response.status_code}: {response.text}")
    except Exception as e:
        logger.error(f"Error calling Gemini API: {e}")

    return None

def analyze_food_with_llm(food_name: str, rag_context: str) -> Optional[Dict[str, Any]]:
    """
    Uses Gemini to synthesize structured food safety response based on RAG context.
    Returns JSON if successful, or None to fall back to direct RAG template.
    """
    prompt = f"""{SYSTEM_PROMPT}

You are analyzing the food item: '{food_name}'.
Available food/product context (do not claim this came from a regulator unless the context says so):
{rag_context}

Return a valid JSON object matching this structure EXACTLY:
{{
    "isFood": true,
    "foodName": "{food_name.title()}",
    "adulterants": ["Adulterant 1", "Adulterant 2"],
    "whyAdulterated": "Brief explanation why adulteration occurs for this item",
    "healthRisks": ["Health risk 1", "Health risk 2"],
    "testMethod": "Name of simple preliminary awareness check",
    "testProcedure": "1-2 lines simple procedure",
    "observation": "Expected preliminary observation",
    "safeTips": ["Safe buying tip 1", "Safe buying tip 2"],
    "storageTips": ["Storage tip 1", "Storage tip 2"],
    "sources": [
        {{"name": "FSSAI DART Manual", "url": "https://www.fssai.gov.in/dart/"}},
        {{"name": "WHO Food Safety", "url": "https://www.who.int/news-room/fact-sheets/detail/food-safety"}}
    ]
}}

If '{food_name}' is clearly NOT a food item (e.g., electronic gadget, furniture, vehicle):
Return:
{{
    "isFood": false,
    "foodName": "{food_name}",
    "message": "This is not a food item.",
    "suggestion": "Please enter a food item such as: Milk, Rice, Turmeric, Honey, Sugar or Edible Oil."
}}

Output ONLY the raw JSON object. Do not enclose in markdown ticks if possible.
"""
    raw_response = generate_with_gemini_raw(prompt)
    if not raw_response:
        return None

    try:
        clean_text = raw_response.strip()
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:]
        if clean_text.startswith("```"):
            clean_text = clean_text[3:]
        if clean_text.endswith("```"):
            clean_text = clean_text[:-3]
        return json.loads(clean_text.strip())
    except Exception as e:
        logger.error(f"Failed to parse Gemini JSON: {e}")
        return None

def chat_with_food_safety_ai(user_message: str, food_context: Optional[str] = None, history: Optional[List[Dict[str, str]]] = None) -> str:
    """
    Multi-turn conversation helper for the Food Safety AI Assistant.
    """
    context_instruction = ""
    if food_context:
        context_instruction = f"Current food being discussed: {food_context}\n"

    history_str = ""
    if history:
        for item in history[-5:]: # Keep last 5 turns
            history_str += f"{item.get('role', 'user').title()}: {item.get('content', '')}\n"

    prompt = f"""{SYSTEM_PROMPT}

{context_instruction}
Recent conversation history:
{history_str}

User inquiry: "{user_message}"

Respond to the user as Food Safety AI. Maintain an empowering, informative tone.
Remember:
- Use phrases like "Preliminary awareness check", "Possible indication", "Laboratory testing is required for confirmation".
- Do not recommend unsafe chemistry.
- Provide practical, realistic consumer guidance.
- Use short sentences and explain each step so a first-time reader can follow it.
- Use the supplied food reference data for specific details. Do not invent nutrition, health, or product facts when they are missing.
- Explain technical terms in plain language and make clear that general reference information does not test the user's food.
"""
    raw = generate_with_gemini_raw(prompt)
    if raw:
        return raw.strip()

    # Fallback response engine if offline / without API key
    lower_msg = user_message.lower()
    if food_context:
        try:
            context_data = json.loads(food_context)
        except json.JSONDecodeError:
            context_data = {}

        if isinstance(context_data, dict) and context_data.get("foodName"):
            food_name = context_data["foodName"]
            details = [
                f"About {food_name}\n"
                "This is general reference information. It is not a test of your own food."
            ]
            if context_data.get("category"):
                details.append(f"Food group: {context_data['category']}")

            if any(term in lower_msg for term in ("nutrition", "nutrient", "calorie")):
                nutrition = context_data.get("nutrition") or {}
                values = nutrition.get("per100g") or {}
                if values:
                    nutrient_labels = {
                        "energy": "Energy",
                        "protein": "Protein",
                        "totalFat": "Total fat",
                        "carbohydrates": "Carbohydrates",
                        "fiber": "Fiber",
                        "totalSugars": "Total sugars",
                        "sodium": "Sodium",
                    }
                    nutrient_text = ", ".join(
                        f"{nutrient_labels.get(name, name.replace('_', ' ').title())}: "
                        f"{value.get('value')} {value.get('unit', '')}".strip()
                        for name, value in values.items()
                    )
                    details.append(
                        f"Nutrition values from {nutrition.get('source', 'the reference source')}:\n"
                        f"{nutrient_text}\n"
                        "These values belong to that database record. They may not match every brand or serving."
                    )
                else:
                    details.append(
                        "Nutrition values were not available in the sources for this food.\n"
                        "Check the nutrition label on the specific package."
                    )
            elif any(term in lower_msg for term in ("ingredient", "label", "brand")):
                product = context_data.get("product") or {}
                product_details = [
                    f"{label}: {product[key]}"
                    for key, label in (
                        ("brand", "Brand"),
                        ("ingredients", "Listed ingredients"),
                        ("countries", "Countries listed"),
                    )
                    if product.get(key)
                ]
                details.append(
                    "Product information\n" + "\n".join(f"- {item}" for item in product_details)
                    if product_details
                    else "No product-label details were available in the online sources."
                )
            elif any(term in lower_msg for term in ("risk", "health", "danger")):
                risks = context_data.get("healthRisks") or []
                details.append(
                    "Possible concerns in the app's general reference\n"
                    + "\n".join(f"- {risk}" for risk in risks)
                    if risks
                    else "No food-specific health-risk information was available in the reference data."
                )
                details.append(
                    "This does not mean your food is contaminated. If a product seems unsafe, do not taste it."
                )
            else:
                overview = context_data.get("overview")
                if overview:
                    details.append(f"Overview\n{overview}")
                adulterants = context_data.get("adulterants") or []
                if adulterants:
                    details.append(
                        "Possible adulterants mentioned in general references\n"
                        + "\n".join(f"- {item}" for item in adulterants)
                        + "\nThese are not findings about your sample."
                    )
                tips = context_data.get("safeTips") or []
                if tips:
                    details.append(
                        "Buying tips\n" + "\n".join(f"- {tip}" for tip in tips[:3])
                    )
                storage = context_data.get("storageTips") or []
                if storage:
                    details.append(
                        "Storage\n" + "\n".join(f"- {tip}" for tip in storage[:2])
                    )

            sources = context_data.get("sources") or []
            if sources:
                details.append(
                    "Sources used\n" + "\n".join(
                        f"- {source.get('name', '')}"
                        for source in sources
                        if source.get("name")
                    )
                )
            details.append(
                "Home checks are only preliminary awareness checks; laboratory testing is required for confirmation."
            )
            return "\n\n".join(details)

    if "health" in lower_msg or "risk" in lower_msg or "danger" in lower_msg:
        return "Adulterated foods can carry various health risks depending on the contaminant. Common adulterants like industrial dyes (such as Metanil Yellow) or detergents can cause digestive distress, kidney load, and toxic exposure over time. For accurate consumer safety, purchase AGMARK or FSSAI-certified sealed foods, and note that household checks are only preliminary indicators—official lab testing is needed for confirmation."
    elif "test" in lower_msg or "check" in lower_msg or "how to" in lower_msg:
        return "Household awareness checks—such as the iodine starch test for milk, the water settling test for spices, or the water dispersion test for honey—provide quick preliminary indications. However, please remember that home tests do not scientifically prove adulteration; laboratory testing under FSSAI protocols is mandatory for scientific confirmation."
    elif "buy" in lower_msg or "purchase" in lower_msg or "store" in lower_msg or "tips" in lower_msg:
        return "When shopping, always check for intact tamper-proof seals, clear FSSAI license numbers, AGMARK certification where applicable, manufacturing/expiry dates, and batch codes. Avoid purchasing unbranded loose powders or oils sold in open unhygienic conditions."
    else:
        return f"Food Safety AI is here to help! Regarding '{user_message}', our awareness project encourages checking certifications (FSSAI, AGMARK), observing preliminary quality indicators, and reporting suspected widespread adulteration to local food safety authorities."
