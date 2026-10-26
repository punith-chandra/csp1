from typing import Dict, Any, List
from urllib.parse import quote_plus
from concurrent.futures import ThreadPoolExecutor
import hashlib
from datetime import datetime
from app.rag.knowledge_retriever import retriever
from app.rag.food_db import is_definitely_non_food
from app.services.gemini_service import analyze_food_with_llm
from app.services.open_food_facts import find_global_food_product
from app.services.usda_food_data import find_usda_food_nutrition
from app.services.web_food_information import find_wikipedia_food_information
from app.database.db import log_search

def build_official_advisory(data: Dict[str, Any]) -> str:
    """
    Generates a formal, official government & institutional advisory text
    in the style of FSSAI Gazettes, WHO Technical Guidelines, and Academic SOPs.
    """
    food_name = data.get("foodName", "Staple Commodity").upper()
    category = data.get("category", "General Food Commodity")
    adulterants = ", ".join(data.get("adulterants", ["Unspecified foreign matter"]))
    why = data.get("whyAdulterated", "Economic adulteration aimed at artificial weight enhancement.")
    health_risks = "\n".join([f"  • {r}" for r in data.get("healthRisks", ["General gastrointestinal toxicity"])])
    test_method = data.get("testMethod", "Visual & Physical Clarification Protocol")
    test_proc = data.get("testProcedure", "Standard physical dissolution in water.")
    observation = data.get("observation", "Uniform physical properties without unnatural separation.")
    safe_tips = "\n".join([f"  • {t}" for t in data.get("safeTips", ["Inspect FSSAI 14-digit license number and batch code."])])
    storage_tips = "\n".join([f"  • {t}" for t in data.get("storageTips", ["Store in hermetically sealed food-grade containers."])])
    sources_str = ", ".join([s.get("name", "") for s in data.get("sources", [])])
    
    hash_code = hashlib.md5(food_name.encode()).hexdigest()[:6].upper()
    ref_id = f"FSSAI-CSP-2026/SOP-{hash_code}"

    official_text = f"""================================================================================
OFFICIAL TECHNICAL ADVISORY & RAPID SCREENING PROTOCOL
COMMUNITY SERVICE PROJECT • SRI VASAVI ENGINEERING COLLEGE (AUTONOMOUS)
DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING • TANUKU, ANDHRA PRADESH
GUIDE: MR. SYED AKHEEL HASSAN GORI | REF ID: {ref_id}
================================================================================

DOCUMENT TITLE: STATUTORY FOOD SAFETY & ADULTERATION AWARENESS DOSSIER
TARGET COMMODITY: {food_name}
REGULATORY CLASSIFICATION: {category.upper()}
STANDARDS CONFORMITY: FSSAI DART MANUAL & CODEX ALIMENTARIUS GUIDELINES

--------------------------------------------------------------------------------
CLAUSE 1: REGULATORY IDENTITY & APPLICABILITY
--------------------------------------------------------------------------------
This technical directive establishes community awareness guidelines for the 
statutory identification, risk assessment, and non-destructive preliminary screening 
of {food_name} under provisions aligned with the Food Safety and Standards Act, 2006.

--------------------------------------------------------------------------------
CLAUSE 2: DOCUMENTED ADULTERATION MECHANISMS & COMMERCIAL MOTIVES
--------------------------------------------------------------------------------
Primary reported adulterants in commerce:
  • {adulterants}

Economic and forensic rationale:
  {why}

--------------------------------------------------------------------------------
CLAUSE 3: TOXICOLOGICAL PROFILE & PUBLIC HEALTH HAZARDS
--------------------------------------------------------------------------------
Exposure to substandard or adulterated {food_name} presents documented clinical risks:
{health_risks}

--------------------------------------------------------------------------------
CLAUSE 4: APPROVED HOUSEHOLD PRELIMINARY SCREENING PROTOCOL (SOP)
--------------------------------------------------------------------------------
Protocol Designation: {test_method}

Standard Operating Procedure (SOP):
{test_proc}

Prescribed Diagnostic Observation:
  {observation}

--------------------------------------------------------------------------------
CLAUSE 5: STATUTORY PURCHASING DIRECTIVES & COMPLIANCE CRITERIA
--------------------------------------------------------------------------------
Consumers are advised to mandate the following verifications prior to procurement:
{safe_tips}

--------------------------------------------------------------------------------
CLAUSE 6: PRESCRIBED PRESERVATION, STORAGE & HYGIENE DIRECTIVES
--------------------------------------------------------------------------------
Preservation conditions to prevent decomposition and secondary contamination:
{storage_tips}

--------------------------------------------------------------------------------
CLAUSE 7: STATUTORY REGULATORY DISCLAIMER & ACCREDITED LABORATORY REFERRAL
--------------------------------------------------------------------------------
STATUTORY DECLARATION: This household screening procedure constitutes a PRELIMINARY
AWARENESS INDICATION ONLY and does NOT provide scientific or legal certification of 
adulteration. In accordance with Section 38/47 of the Food Safety & Standards Act, 
conclusive scientific and prosecutorial verification strictly requires quantitative 
testing by a certified NABL / FSSAI Notified Laboratory.
Do not consume or handle suspicious chemical substances during testing.

Grievance Redressal: Consumers encountering suspected commercial adulteration are 
instructed to log official complaints via the National Consumer Helpline (1915) 
or the FSSAI Food Safety Voice Portal (Toll-Free: 1800-112-100).

--------------------------------------------------------------------------------
CLAUSE 8: GAZETTED REFERENCES & REGULATORY AUTHORITIES
--------------------------------------------------------------------------------
Primary Authority Citations: {sources_str}
Prepared by: CSE Project Team, Sri Vasavi Engineering College (Autonomous), Tanuku.
================================================================================"""
    return official_text

def analyze_food_item(food_input: str) -> Dict[str, Any]:
    """
    Main service function to analyze food item, reject non-food objects,
    and return structured food adulteration awareness data with official text.
    """
    clean_input = food_input.strip()

    # Step 1: Check for empty input
    if not clean_input:
        return {
            "isFood": False,
            "classification": "uncertain",
            "foodName": "",
            "message": "Please enter a food item.",
            "suggestion": "Try searching for Milk, Turmeric, Honey, Sugar, Ghee, or Edible Oil."
        }

    # Step 2: Non-food item fast check
    if is_definitely_non_food(clean_input):
        log_search(clean_input, is_food=False, category=None)
        ref_id = f"ADVISORY-REJ-NF-{hashlib.md5(clean_input.encode()).hexdigest()[:5].upper()}"
        official_non_food_text = f"""================================================================================
STATUTORY COMMODITY JURISDICTION DIRECTIVE
REF ID: {ref_id} | DATE: {datetime.now().strftime('%Y-%m-%d')}
================================================================================
NOTICE OF NON-FOOD STATUS: "{clean_input.title()}"

CLAUSE 1: STATUTORY AMBIT & JURISDICTION
Pursuant to Section 3(1)(j) of the Food Safety and Standards Act (2006), the 
queried article "{clean_input.title()}" is officially classified as a manufactured, 
mechanical, or inanimate non-ingestible object.

CLAUSE 2: NON-APPLICABILITY OF FOOD SAFETY EVALUATION
Food Safety AI and associated regulatory screening models have jurisdiction 
strictly over substances intended for human oral nutrition and consumption. 
Adulteration screening protocols cannot be administered on non-food articles.

CLAUSE 3: DIRECTIVE FOR COMMODITY RE-SUBMISSION
The user is instructed to re-submit valid edible agricultural staples or food 
commodities, such as: Milk, Rice, Turmeric, Honey, Sugar, Ghee, or Edible Oil.
================================================================================"""
        return {
            "isFood": False,
            "classification": "non_food",
            "foodName": clean_input.title(),
            "message": f"'{clean_input.title()}' does not appear to be a food item.",
            "suggestion": "Please enter a food item such as: Milk, Rice, Turmeric, Honey, Sugar, or Edible Oil.",
            "sources": build_web_search_links(clean_input),
            "officialAdvisoryText": official_non_food_text,
            "documentReference": ref_id
        }

    # Step 3: Search knowledge base via RAG retriever
    matched_data, is_food, confidence = retriever.search_food(clean_input)

    if not is_food:
        log_search(clean_input, is_food=False, category=None)
        ref_id = f"ADVISORY-REJ-NF-{hashlib.md5(clean_input.encode()).hexdigest()[:5].upper()}"
        return {
            "isFood": False,
            "classification": "non_food",
            "foodName": clean_input.title(),
            "message": f"'{clean_input.title()}' does not appear to be a food item.",
            "suggestion": "Please enter a food item such as: Milk, Rice, Turmeric, Honey, Sugar, or Edible Oil.",
            "sources": build_web_search_links(clean_input),
            "documentReference": ref_id
        }

    with ThreadPoolExecutor(max_workers=3) as executor:
        product_lookup = executor.submit(find_global_food_product, clean_input)
        wikipedia_lookup = executor.submit(find_wikipedia_food_information, clean_input)
        usda_lookup = executor.submit(find_usda_food_nutrition, clean_input)
        global_product = product_lookup.result()
        web_information = wikipedia_lookup.result()
        usda_nutrition = usda_lookup.result()

    if not matched_data and confidence == 0:
        if global_product or web_information or usda_nutrition:
            food_name = (
                global_product["name"]
                if global_product
                else web_information["title"]
                if web_information
                else clean_input.title()
            )
            category = (
                (global_product or {}).get("category")
                or (usda_nutrition or {}).get("category")
                or "Food item (online reference)"
            )
            log_search(food_name, is_food=True, category=category)
            product_sources = [
                {"name": "WHO Food Safety", "url": "https://www.who.int/news-room/fact-sheets/detail/food-safety"},
                {"name": "Codex Alimentarius", "url": "https://www.fao.org/fao-who-codexalimentarius/"}
            ]
            if global_product:
                product_sources.insert(
                    0,
                    {"name": "Open Food Facts product record", "url": global_product["url"]},
                )
            if web_information:
                product_sources.insert(
                    0,
                    {"name": f"Wikipedia: {web_information['title']}", "url": web_information["url"]},
                )
            if usda_nutrition:
                product_sources.insert(
                    0,
                    {"name": "USDA FoodData Central", "url": usda_nutrition["url"]},
                )
            online_sources = []
            if web_information:
                online_sources.append("Wikipedia")
            if global_product:
                online_sources.append("Open Food Facts")
            if usda_nutrition:
                online_sources.append("USDA FoodData Central")
            result = {
                "isFood": True,
                "classification": "food",
                "foodName": food_name,
                "category": category,
                "adulterants": [],
                "whyAdulterated": (
                    "Online reference information can describe a food, but it does not establish "
                    "that this item is adulterated or verify its purity."
                ),
                "healthRisks": [],
                "testMethod": "Check the package and label (this is not a purity test)",
                "testProcedure": (
                    "1. Make sure the package is sealed and undamaged.\n"
                    "2. Read the ingredients, allergen notice, and date on the label.\n"
                    "3. If anything looks unsafe, do not taste it; contact your local food-safety authority."
                ),
                "observation": (
                    "This online reference identifies a food item only. It cannot confirm "
                    "the contents, safety, or authenticity of the item you have."
                ),
                "safeTips": [
                    "Compare the product name and brand with the package in your hand.",
                    "Check the seal, ingredients, allergen notice, and expiry or best-before date.",
                    "Use the food-safety authority for your country to report a concern."
                ],
                "storageTips": [
                    "Follow the storage directions printed on the package.",
                    "Keep food sealed and separate from chemicals and cleaning products."
                ],
                "sources": product_sources,
                "dataSource": (
                    f"{', '.join(online_sources)} data; available fields vary by food"
                ),
                "disclaimer": (
                    "Online reference and catalog details may be incomplete or incorrect. They do not "
                    "verify the food or product you own. For suspected adulteration, contact your local "
                    "food-safety authority; laboratory testing is required for confirmation."
                ),
            }
            _attach_online_information(
                result, global_product, web_information, usda_nutrition
            )
            return result

        result = {
            "isFood": False,
            "classification": "uncertain",
            "foodName": clean_input.title(),
            "message": f"We could not confidently classify '{clean_input.title()}' as food or non-food.",
            "suggestion": "Check the item name using these web searches, or try a food item from the suggestions.",
            "sources": build_web_search_links(clean_input)
        }
        return result

    # If matched with high confidence from our curated FSSAI database
    if matched_data and confidence >= 0.7:
        log_search(matched_data["foodName"], is_food=True, category=matched_data.get("category"))
        official_text = build_official_advisory(matched_data)
        ref_id = f"FSSAI-CSP-2026/SOP-{hashlib.md5(matched_data['foodName'].encode()).hexdigest()[:6].upper()}"
        result = {
            "isFood": True,
            "classification": "food",
            "foodName": matched_data["foodName"],
            "category": matched_data.get("category", "General Food"),
            "adulterants": matched_data.get("adulterants", []),
            "whyAdulterated": matched_data.get("whyAdulterated", ""),
            "healthRisks": matched_data.get("healthRisks", []),
            "testMethod": matched_data.get("testMethod", ""),
            "testProcedure": matched_data.get("testProcedure", ""),
            "observation": matched_data.get("observation", ""),
            "safeTips": matched_data.get("safeTips", []),
            "storageTips": matched_data.get("storageTips", []),
            "sources": matched_data.get("sources", []),
            "disclaimer": "This is only a preliminary awareness check. Laboratory testing is required for confirmation. Do not consume or handle suspicious substances during testing.",
            "officialAdvisoryText": official_text,
            "documentReference": ref_id,
            "issuingAuthority": "Sri Vasavi Engineering College (A) • Department of CSE • FSSAI DART Aligned"
        }
        _attach_online_information(
            result, global_product, web_information, usda_nutrition
        )
        return result

    # Fallback to general staple or LLM analysis
    rag_context = f"Analyze food item: {clean_input} for adulteration awareness under FSSAI / Codex standards."
    llm_result = analyze_food_with_llm(clean_input, rag_context)

    if llm_result:
        if not llm_result.get("isFood", True):
            log_search(clean_input, is_food=False, category=None)
            return {
                "isFood": False,
                "foodName": clean_input.title(),
                "message": f"'{clean_input.title()}' does not appear to be a food item.",
                "suggestion": "Please enter a food item such as: Milk, Rice, Turmeric, Honey, Sugar, or Edible Oil."
            }
        log_search(llm_result.get("foodName", clean_input.title()), is_food=True, category="General Food")
        official_text = build_official_advisory(llm_result)
        llm_result["officialAdvisoryText"] = official_text
        llm_result["classification"] = "food"
        llm_result["documentReference"] = f"FSSAI-CSP-2026/SOP-{hashlib.md5(clean_input.encode()).hexdigest()[:6].upper()}"
        _attach_online_information(
            llm_result, global_product, web_information, usda_nutrition
        )
        return llm_result

    # Basic fallback
    fallback_data = {
        "isFood": True,
        "classification": "food",
        "foodName": clean_input.title(),
        "category": "General Food Item",
        "adulterants": ["Extraneous matter / water dilution", "Substandard bulk fillers", "Non-permitted artificial colorants"],
        "whyAdulterated": f"Economic adulteration aimed at inflating physical mass and commercial margins of {clean_input.title()}.",
        "healthRisks": ["Acute gastrointestinal discomfort", "Metabolic disruption from non-permitted additives", "Microbial load risk"],
        "testMethod": "Preliminary Physical Inspection & Dissolution Clarity Check",
        "testProcedure": "1. Inspect olfactory and visual consistency.\n2. Dilute sample in clear drinking water and examine settling velocity and coloration.",
        "observation": "Standard unadulterated products manifest uniform dispersion; synthetic additives trigger immediate turbidity or sediment.",
        "safeTips": ["Mandate verified 14-digit FSSAI licensing and batch packaging codes.", "Reject unlabelled loose commodities sold without date stamps."],
        "storageTips": ["Store in airtight opaque containers shielded from humidity and thermal degradation."],
        "sources": [{"name": "FSSAI (Food Safety and Standards Authority of India)", "url": "https://www.fssai.gov.in"}]
    }
    fallback_data["officialAdvisoryText"] = build_official_advisory(fallback_data)
    fallback_data["documentReference"] = f"FSSAI-CSP-2026/SOP-{hashlib.md5(clean_input.encode()).hexdigest()[:6].upper()}"
    _attach_online_information(
        fallback_data, global_product, web_information, usda_nutrition
    )
    return fallback_data


def _attach_online_information(
    result: Dict[str, Any],
    global_product: Any,
    web_information: Any,
    usda_nutrition: Any,
) -> None:
    """Add available public-reference data and citations without replacing curated facts."""
    sources = result.setdefault("sources", [])
    known_urls = {source.get("url") for source in sources}
    if web_information:
        result["webInformation"] = web_information
        if web_information["url"] not in known_urls:
            sources.append({
                "name": f"Wikipedia: {web_information['title']}",
                "url": web_information["url"],
            })
            known_urls.add(web_information["url"])
    if global_product:
        result["productInfo"] = {
            "brand": global_product.get("brand"),
            "countries": global_product.get("countries"),
            "ingredients": global_product.get("ingredients"),
            "barcode": global_product.get("barcode"),
            "nutritionGrade": global_product.get("nutritionGrade"),
            "nutritionPer100g": global_product.get("nutritionPer100g", {}),
            "url": global_product["url"],
        }
        if global_product["url"] not in known_urls:
            sources.append({
                "name": "Open Food Facts product record",
                "url": global_product["url"],
            })
            known_urls.add(global_product["url"])
    if usda_nutrition:
        result["nutritionInformation"] = {
            "source": "USDA FoodData Central",
            "dataType": usda_nutrition.get("dataType"),
            "per100g": usda_nutrition.get("nutritionPer100g", {}),
            "url": usda_nutrition["url"],
        }
        if usda_nutrition["url"] not in known_urls:
            sources.append({
                "name": "USDA FoodData Central",
                "url": usda_nutrition["url"],
            })
    online_sources = []
    if web_information:
        online_sources.append("Wikipedia")
    if global_product:
        online_sources.append("Open Food Facts")
    if usda_nutrition:
        online_sources.append("USDA FoodData Central")
    if online_sources:
        result["dataSource"] = (
            "Curated food-safety reference with " + ", ".join(online_sources) + " data"
        )
    for search_link in build_web_search_links(result.get("foodName", ""))[:2]:
        if search_link["url"] not in known_urls:
            sources.append(search_link)
            known_urls.add(search_link["url"])


def build_web_search_links(query: str) -> List[Dict[str, str]]:
    encoded_query = quote_plus(query)
    return [
        {"name": "Google web search", "url": f"https://www.google.com/search?q={encoded_query}"},
        {"name": "Bing web search", "url": f"https://www.bing.com/search?q={encoded_query}"},
        {"name": "Wikipedia search", "url": f"https://en.wikipedia.org/w/index.php?search={encoded_query}"},
        {"name": "Open Food Facts search", "url": f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={encoded_query}"},
        {"name": "USDA FoodData Central", "url": f"https://fdc.nal.usda.gov/food-search/?query={encoded_query}"},
    ]
