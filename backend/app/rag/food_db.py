"""
Comprehensive Food Safety and Adulteration Knowledge Base.
Curated from authentic regulatory and research bodies:
- FSSAI (Food Safety and Standards Authority of India) - DART (Detect Adulteration with Rapid Test)
- WHO (World Health Organization) Food Safety Guidelines
- FAO (Food and Agriculture Organization of the United Nations)
- CSIR-CFTRI (Central Food Technological Research Institute, Mysore)
- AGMARK (Agricultural Marketing and Quality Certification, Government of India)
"""

FOOD_KNOWLEDGE_BASE = {
    "milk": {
        "foodName": "Milk",
        "category": "Dairy Products",
        "aliases": ["cow milk", "buffalo milk", "dairy milk", "raw milk", "packaged milk", "paalu"],
        "adulterants": [
            "Excess Water (dilution)",
            "Starch (thickening agent)",
            "Urea / Ammonium Sulphate",
            "Detergent / Synthetic Milk compounds",
            "Neutralizers (Sodium Carbonate / Bicarbonate)"
        ],
        "whyAdulterated": "Milk is adulterated primarily for economic gain—diluted with water to increase liquid volume, and then added with starches, urea, or detergent to artificially restore thickness, lactometer density, and foamy appearance.",
        "healthRisks": [
            "Contaminated water causes water-borne infections (diarrhoea, typhoid, gastrointestinal distress).",
            "Detergents and synthetic chemicals can cause severe stomach irritation, nausea, ulcers, and long-term renal/liver toxicity.",
            "Urea causes strain on the kidneys and disrupts internal metabolic functions.",
            "Dilution robs growing children and infants of essential proteins, calcium, and fats."
        ],
        "testMethod": "Starch Detection (Iodine Test) & Slip Test for Synthetic Admixtures",
        "testProcedure": "1. Boil 2-3 ml of milk sample in a test tube or glass and cool to room temperature.\n2. Add 2 to 3 drops of standard tincture of iodine (dilute iodine solution).\n3. Slip Test: Put a drop of milk on a polished, slanting glass plate.",
        "observation": "For Iodine Test: An intense blue or blue-black coloration indicates the presence of added starch (pure milk shows only pale yellowish iodine color).\nFor Slip Test: Pure milk flows slowly, leaving a distinct white trail; water-adulterated milk flows immediately without leaving a trail.",
        "safeTips": [
            "Always verify the mandatory FSSAI license number and batch code on sealed milk pouches.",
            "Ensure packaging is tamper-evident with intact thermosealing.",
            "Avoid purchasing loose raw milk from unverified vendors without boil-testing.",
            "Prefer certified cooperative brands (e.g., Amul, Vijaya, Nandini, Mother Dairy) that adhere to cold-chain hygiene standards.",
            "Check best-before or use-by dates prominently printed on the pouch."
        ],
        "storageTips": [
            "Store pasteurized milk in the refrigerator below 4°C (40°F) immediately upon purchase.",
            "Boil raw milk thoroughly to at least 72°C for 15 seconds or bring to rolling boil before consumption.",
            "Use clean, covered stainless steel or glass containers; avoid prolonged exposure to direct sunlight.",
            "Consume opened pasteurized packets within 24 to 48 hours."
        ],
        "sources": [
            {
                "name": "FSSAI DART (Detect Adulteration with Rapid Test) Manual",
                "url": "https://www.fssai.gov.in/dart/"
            },
            {
                "name": "World Health Organization (WHO) - Dairy & Food Safety",
                "url": "https://www.who.int/news-room/fact-sheets/detail/food-safety"
            },
            {
                "name": "CSIR-CFTRI Milk Testing & Quality Standards",
                "url": "https://cftri.res.in"
            }
        ]
    },
    "turmeric": {
        "foodName": "Turmeric Powder",
        "category": "Spices",
        "aliases": ["turmeric", "haldi", "pasupu", "curcuma", "turmeric root"],
        "adulterants": [
            "Metanil Yellow (non-permitted coal-tar dye)",
            "Lead Chromate (yellow industrial pigment)",
            "Chalk Powder / Gypsum / Yellow earth",
            "Starch from cassava or wild arrowroot"
        ],
        "whyAdulterated": "Added to give cheap, low-grade, or exhausted rhizome powder a vibrant golden-yellow hue, and chalk/starch is added to artificially inflate bulk weight at lower production costs.",
        "healthRisks": [
            "Metanil Yellow is a neurotoxic, carcinogenic dye; animal studies show testicular damage and metabolic toxicity.",
            "Lead Chromate contains toxic heavy metals (Lead) that cause irreversible neurotoxicity, anaemia, cognitive impairment in children, and chronic kidney damage.",
            "Chalk and yellow earth cause digestive tract irritation and mineral calcification."
        ],
        "testMethod": "Metanil Yellow Acid Coloration Check & Water Settling Test",
        "testProcedure": "1. Take 1 teaspoon of turmeric powder in a transparent glass of warm water.\n2. Do not stir violently; observe how it settles.\n3. Acid Check: In a sample of turmeric water, add a few drops of concentrated acid (dilute hydrochloric acid or strong lemon juice).",
        "observation": "Pure turmeric settles steadily to the bottom, leaving a transparent light-yellow water layer. Adulterated powder turns the water cloudy dark yellow instantly. For Acid Check: If Metanil Yellow is present, the solution turns bright magenta-pink and does not vanish upon further dilution with water.",
        "safeTips": [
            "Look for the AGMARK certification and FSSAI seal on turmeric powder packages.",
            "Prefer buying whole turmeric bulbs (curcuma fingers) and milling them at a trustworthy local flour mill.",
            "Avoid intensely bright neon-yellow loose spices sold in open heaps at roadside shacks.",
            "Check for nutritional labeling and pesticide residue clearances where available."
        ],
        "storageTips": [
            "Store in an airtight, opaque glass or food-grade stainless steel jar.",
            "Keep in a cool, dry pantry away from direct sunlight, which degrades natural curcumin.",
            "Always use a dry spoon to prevent moisture condensation and fungal mold growth."
        ],
        "sources": [
            {
                "name": "FSSAI Spices & Condiments Quality Standards",
                "url": "https://www.fssai.gov.in"
            },
            {
                "name": "Spices Board of India - Quality & Testing Guidelines",
                "url": "http://www.indianspices.com"
            },
            {
                "name": "FAO/WHO Codex Alimentarius for Spices and Culinary Herbs",
                "url": "https://www.fao.org/fao-who-codexalimentarius/"
            }
        ]
    },
    "chilli powder": {
        "foodName": "Chilli Powder",
        "category": "Spices",
        "aliases": ["red chilli powder", "red chili", "mirchi powder", "mirapakaya podi", "lal mirch"],
        "adulterants": [
            "Brick Powder",
            "Sudan Dyes (Sudan I, II, III, IV industrial red dyes)",
            "Rhodamine B (carcinogenic artificial dye)",
            "Sawdust / Wood meal",
            "Soapstone / Chalk powder"
        ],
        "whyAdulterated": "To impart an intense, brilliant deep-red coloration to low-pungency or old chilli waste, and to drastically increase commercial bulk weight with inexpensive mineral powders.",
        "healthRisks": [
            "Sudan Dyes and Rhodamine B are internationally classified as genotoxic carcinogens.",
            "Brick powder and sawdust cause abrasive stomach ulcerations, acute gastritis, and severe gastrointestinal lesions.",
            "Insoluble stone powders strain digestive pathways and promote bowel irritation."
        ],
        "testMethod": "Water Dispersion & Grit Settling Test",
        "testProcedure": "1. Add a teaspoon of chilli powder to a transparent glass filled with clean water.\n2. Do not stir; observe the particles as they settle.\n3. Rub the residue settled at the bottom between your fingertips.",
        "observation": "Pure chilli powder settles slowly and floats partially on the surface without leaving sudden bright red streaks. Artificial dye or brick powder leaves an immediate red cascading streak in the water and settles to a gritty, harsh sediment that scratches between your fingers.",
        "safeTips": [
            "Check for AGMARK Grade I certification and FSSAI registration.",
            "Buy whole dry red chillies (with stems intact) and grind them at home or reputable mills.",
            "Reject loose chilli powders exhibiting an unnaturally deep scarlet or oily neon-red tone.",
            "Inspect packaging for vacuum sealing or multi-layered nitrogen flushed foil."
        ],
        "storageTips": [
            "Store in tightly sealed airtight containers in a dark, dry cupboard.",
            "Keep moisture strictly away; dampness triggers aflatoxin (fungal toxin) production.",
            "Store bulk quantities with a few whole bay leaves or cloves to deter pantry pests."
        ],
        "sources": [
            {
                "name": "FSSAI DART Guide on Spices",
                "url": "https://www.fssai.gov.in/dart/"
            },
            {
                "name": "WHO International Agency for Research on Cancer (IARC) - Sudan Dyes",
                "url": "https://www.iarc.who.int"
            }
        ]
    },
    "sugar": {
        "foodName": "Sugar",
        "category": "Sweeteners",
        "aliases": ["refined sugar", "white sugar", "cane sugar", "table sugar", "panchadara", "chini"],
        "adulterants": [
            "Chalk Powder / Gypsum",
            "Washing Soda / Sodium Carbonate",
            "Urea",
            "White Sand / Insoluble Silica grit"
        ],
        "whyAdulterated": "Adulterated to increase bag weight and maintain bright crystal-white luster using cheaper alkaline minerals and industrial carbonates.",
        "healthRisks": [
            "Chalk powder and gypsum lead to kidney stones, urinary calculi, and severe stomach discomfort.",
            "Washing soda disrupts stomach pH, causing chemical burns to the esophagus, vomiting, and metabolic alkalosis.",
            "Urea damages kidney filtration barriers and triggers gastrointestinal toxicity."
        ],
        "testMethod": "Water Dissolution & Effervescence Check",
        "testProcedure": "1. Take 1 tablespoon of sugar sample and dissolve it thoroughly in a clean glass of water.\n2. Observe the clarity of the solution and the bottom of the glass.\n3. To test for washing soda/chalk: Add a few drops of vinegar or lemon juice to the sugar solution.",
        "observation": "Pure sugar dissolves completely and leaves a sparkling clear or faintly translucent solution with zero sediment. Chalk powder or sand will settle to the bottom as an opaque white sediment. If washing soda is present, bubbling effervescence (carbon dioxide gas) will be observed when acid/vinegar is added.",
        "safeTips": [
            "Inspect crystals: Pure refined sugar crystals are translucent, uniform in geometry, and sparkle under light.",
            "Avoid yellowish or powdery loose sugar bags with excessive white residue on the bag corners.",
            "Look for FSSAI approved factory packaging with lot numbers.",
            "Smell the sugar sample: Pure sugar is completely odorless; urea or chemical adulterants leave a faint ammoniacal odor."
        ],
        "storageTips": [
            "Store in an airtight jar in a dry pantry; sugar is hygroscopic and quickly absorbs atmospheric moisture.",
            "Place a dry wooden clove or star anise in the container to repel ants naturally.",
            "Never insert wet spoons into the sugar container."
        ],
        "sources": [
            {
                "name": "FSSAI Food Quality Standards - Sugars and Honey",
                "url": "https://www.fssai.gov.in"
            },
            {
                "name": "Codex Alimentarius Standard for Sugars (CXS 212-1999)",
                "url": "https://www.fao.org/fao-who-codexalimentarius/"
            }
        ]
    },
    "honey": {
        "foodName": "Honey",
        "category": "Sweeteners",
        "aliases": ["pure honey", "raw honey", "wild honey", "tene", "shahad", "bee honey"],
        "adulterants": [
            "High Fructose Corn Syrup (HFCS)",
            "Invert Sugar Syrup / Rice Syrup / C4 Cane Syrups",
            "Jaggery / Molasses Solution",
            "Water dilution"
        ],
        "whyAdulterated": "Honey is one of the highest-value natural sweeteners on the market; industrial sugar syrups mimic the viscosity, sweetness, and refractive index of honey at a fraction of the cost.",
        "healthRisks": [
            "Excessive high-fructose syrups elevate liver fat, promote obesity, and accelerate Type 2 diabetes risk.",
            "Spikes blood glucose rapidly unlike raw honey which has natural enzymes and antioxidants.",
            "Industrial syrups may contain heavy metal residues and processing chemicals."
        ],
        "testMethod": "Water Dispersion Test & Cotton Wick Flame Check",
        "testProcedure": "1. Water Test: Gently drop a tablespoon of honey into a clear glass of plain water without stirring.\n2. Cotton Wick Check: Dip a clean dry cotton wick into the honey and ignite it with a matchstick.",
        "observation": "For Water Test: Pure honey is dense and sinks directly to the bottom in an intact blob without dissolving immediately. Adulterated honey containing sugar syrup disperses into the water quickly on the way down.\nFor Wick Test: Pure honey burns cleanly; honey diluted with excess water will crackle, sputter, or refuse to burn.",
        "safeTips": [
            "Check for NMR (Nuclear Magnetic Resonance) tested certification and FSSAI standards on the jar label.",
            "Do not confuse natural crystallization with adulteration—pure raw honey naturally crystallizes at lower temperatures.",
            "Avoid unbranded clear amber syrups sold in plastic bottles without nutritional disclosures.",
            "Inspect the ingredient panel: Ensure it says 100% Pure Honey with no added sugars or rice syrup."
        ],
        "storageTips": [
            "Store honey at room temperature in a tightly sealed glass container.",
            "Do NOT refrigerate pure honey as this accelerates crystallization unnecessarily.",
            "Keep the lid tightly secured to prevent airborne moisture absorption."
        ],
        "sources": [
            {
                "name": "FSSAI Guidelines on Honey Purity and NMR Testing",
                "url": "https://www.fssai.gov.in"
            },
            {
                "name": "Centre for Science and Environment (CSE) Honey Adulteration Investigation",
                "url": "https://www.cseindia.org"
            },
            {
                "name": "FAO Codex Standard for Honey (Codex Stan 12-1981)",
                "url": "https://www.fao.org/fao-who-codexalimentarius/"
            }
        ]
    },
    "edible oil": {
        "foodName": "Edible Oil",
        "category": "Edible Oils",
        "aliases": ["cooking oil", "vegetable oil", "mustard oil", "sunflower oil", "groundnut oil", "nune", "tel"],
        "adulterants": [
            "Argemone Oil (toxic weed oil from Argemone mexicana)",
            "Non-edible Mineral Oil / Hydrocarbons",
            "Recycled Rancid Frying Oil",
            "Castor Oil / Low-grade Palm Stearin"
        ],
        "whyAdulterated": "Mineral oils, argemone oil, and cheap palm fractions are mixed into premium cooking oils (like cold-pressed mustard, sesame, or groundnut oil) to slash production expenses.",
        "healthRisks": [
            "Argemone oil causes Epidemic Dropsy—characterized by severe edema, cardiac arrest, glaucoma, and gastrointestinal failure.",
            "Mineral oil causes liver and intestinal damage and impairs fat-soluble vitamin (A, D, E, K) absorption.",
            "Recycled rancid oils contain high free radicals and polar compounds linked to cardiovascular disease and cancer."
        ],
        "testMethod": "Nitric Acid Test Indication for Argemone Oil & Cold Refrigeration Check",
        "testProcedure": "1. Nitric Acid Indication (Laboratory check): 5 ml of oil sample mixed with 5 ml of concentrated nitric acid.\n2. Household Cold Test: Place 50 ml of oil in a clean glass jar in the refrigerator (not freezer) for 2 to 3 hours.",
        "observation": "Nitric Acid Check: Presence of a crimson red ring at the junction of the two layers indicates argemone oil contamination (laboratory test).\nHousehold Cold Test: Pure single-seed oils remain uniform; cheap blended palm stearin or impure fats will solidify into cloudy, waxy layers at the base.",
        "safeTips": [
            "Buy branded oils packaged in sealed tamper-proof tins or food-grade PET bottles displaying the FSSAI logo and AGMARK seal.",
            "Avoid purchasing loose oil sold from unlabelled open drums in local markets.",
            "Check the Total Polar Compounds (TPC) limit compliance (< 25%) when buying from commercial suppliers.",
            "Ensure the packaging states 'Single Source' or clearly lists the declared blended percentages under FSSAI rules."
        ],
        "storageTips": [
            "Store edible oils in dark, cool locations away from kitchen stoves and direct sunlight.",
            "Never reuse frying oil more than once or twice; discard oil if it turns dark, viscous, or smokes at low heat.",
            "Keep oil containers tightly closed to prevent atmospheric oxidation (rancidity)."
        ],
        "sources": [
            {
                "name": "FSSAI Regulations on Edible Vegetable Oils",
                "url": "https://www.fssai.gov.in"
            },
            {
                "name": "WHO Guidelines on Trans Fats and Safe Cooking Oils",
                "url": "https://www.who.int"
            },
            {
                "name": "National Institute of Nutrition (NIN) Dietary Guidelines for Oils & Fats",
                "url": "https://www.nin.res.in"
            }
        ]
    },
    "ghee": {
        "foodName": "Ghee (Clarified Butter)",
        "category": "Dairy Products",
        "aliases": ["deshi ghee", "pure ghee", "cow ghee", "buffalo ghee", "neyyi"],
        "adulterants": [
            "Vanaspati (Hydrogenated Vegetable Oil)",
            "Mashed Potatoes / Sweet Potatoes / Starch",
            "Animal Tallow / Industrial Lard",
            "Artificial Butter Essence and Coal-tar Colors"
        ],
        "whyAdulterated": "Ghee commands a high market price; adding hydrogenated fats (Vanaspati) or starch yields 3-4x profit margins while replicating the solid grain and fatty texture of real ghee.",
        "healthRisks": [
            "Vanaspati contains high levels of industrial trans fats, which skyrocket LDL (bad) cholesterol and cardiovascular attack risks.",
            "Animal fats and unhygienic adulterants introduce microbial toxins and digestive infections.",
            "Synthetic butter flavorings and dyes strain liver detoxification pathways."
        ],
        "testMethod": "Sugar-HCl Test (Baudouin Check) & Iodine Starch Test",
        "testProcedure": "1. Starch Test: Melt 5 ml of ghee sample, cool, and add 2-3 drops of iodine tincture.\n2. Palm Heat Check: Take a small spoon of ghee and place it directly on your palm.\n3. Baudouin Test (Laboratory): 5 ml melted ghee + 5 ml concentrated HCl + pinch of sugar, shake vigorously.",
        "observation": "Starch Check: Appearance of a blue tint indicates added mashed potato or starch.\nPalm Heat Check: Pure ghee melts instantly within seconds from your natural body heat; adulterated ghee with Vanaspati or wax remains solid or melts sluggishly.\nBaudouin Check: Crimson or rose-red coloration confirms presence of Vanaspati (sesame oil marker).",
        "safeTips": [
            "Always purchase ghee bearing the Special Grade AGMARK seal with a green border and FSSAI mark.",
            "Pure cow ghee has a distinct grainy (danedar) texture and a pleasant, mild nutty aroma.",
            "Never purchase unbranded loose ghee sold without manufacturing and batch provenance.",
            "Inspect the packaging: Look for nitrogen-flushed tins or foil-lined aseptic cartons."
        ],
        "storageTips": [
            "Store ghee in an opaque stainless steel or dark glass jar in a cool, dry cupboard.",
            "Ghee has naturally low moisture and can stay fresh for 6-12 months without refrigeration.",
            "Always use a sterile, completely dry spoon to avoid microbial growth."
        ],
        "sources": [
            {
                "name": "AGMARK Rules for Creamery Butter and Ghee",
                "url": "https://dmi.gov.in"
            },
            {
                "name": "FSSAI DART Booklet - Dairy Products",
                "url": "https://www.fssai.gov.in/dart/"
            }
        ]
    },
    "tea": {
        "foodName": "Tea (Tea Leaves / Dust)",
        "category": "Beverages",
        "aliases": ["black tea", "tea powder", "chai patti", "tea leaves", "green tea", "teea aaku"],
        "adulterants": [
            "Exhausted / Used Dried Tea Leaves (re-colored)",
            "Iron Filings (from machinery milling)",
            "Artificial Coal-Tar Dyes (e.g., Prussian Blue, Indigo, Malachite Green)",
            "Sawdust / Leather fluffs / Starch grains"
        ],
        "whyAdulterated": "Recycling exhausted tea leaves collected from hotels and reprocessing them with chemical dyes and iron powders mimics premium CTC tea grains at negligible cost.",
        "healthRisks": [
            "Iron filings cause severe internal gastrointestinal micro-cuts, abdominal pain, and intestinal bleeding.",
            "Artificial dyes are synthetic poisons associated with cellular toxicity, liver damage, and carcinogenic mutations.",
            "Exhausted leaves harbor microbial mold, aflatoxins, and unhygienic pathogens."
        ],
        "testMethod": "Filter Paper Rub Test & Magnet Attraction Test",
        "testProcedure": "1. Wet Filter Paper Test: Spread tea leaves on a moist white filter paper or wet tissue paper. Press down gently.\n2. Magnet Test: Spread tea powder in a thin layer on a clean plate and move a strong magnet closely over it.",
        "observation": "Filter Paper Test: Pure tea leaves do not bleed color onto wet paper at room temperature. Chemically dyed or recycled tea leaves will immediately release distinct yellow, orange, or red stains on the paper.\nMagnet Test: If iron filings are present, they will visibly jump and cling to the magnet surface.",
        "safeTips": [
            "Look for the Tea Board of India 'India Tea' certification logo and FSSAI number.",
            "Ensure the packaging is hermetically sealed in multi-layer foil to protect aroma.",
            "Reject loose tea sold with an unusually glossy or artificially blackened appearance.",
            "Avoid excessively dusty blends with uneven grain sizes and harsh chemical odours."
        ],
        "storageTips": [
            "Store in an airtight container away from light, moisture, and strong-smelling spices (tea absorbs smells).",
            "Keep in a cool, dry pantry shelf.",
            "Avoid keeping the tea caddy near steam or stovetops."
        ],
        "sources": [
            {
                "name": "Tea Board of India Quality & Safety Standards",
                "url": "http://www.teaboard.gov.in"
            },
            {
                "name": "FSSAI Regulations on Tea & Coffee Beverages",
                "url": "https://www.fssai.gov.in"
            }
        ]
    },
    "coffee": {
        "foodName": "Coffee (Coffee Powder)",
        "category": "Beverages",
        "aliases": ["coffee powder", "filter coffee", "instant coffee", "ground coffee", "kaapi"],
        "adulterants": [
            "Excessive Chicory Powder (beyond declared statutory limit)",
            "Roasted Date Seed / Tamarind Seed Powder",
            "Roasted Barley / Cereal Grain Powder",
            "Coal-tar brown colorings"
        ],
        "whyAdulterated": "Chicory roots and roasted date/tamarind seeds are inexpensive fillers that mimic the dark color, bitter profile, and roasted aroma of real Arabica/Robusta coffee beans.",
        "healthRisks": [
            "Unregulated seed powders can trigger severe digestive allergies, stomach cramps, and irritable bowel symptoms.",
            "Excessive undeclared chicory causes chronic diarrhea and flatulence in sensitive individuals.",
            "Deprives consumers of genuine coffee polyphenols and bioactive compounds."
        ],
        "testMethod": "Cold Water Float & Streak Test",
        "testProcedure": "1. Take a transparent glass filled with clean cold water.\n2. Gently sprinkle 1 teaspoon of coffee powder over the surface of the water.\n3. Do not stir; watch the sinking behavior and water color for 2 to 3 minutes.",
        "observation": "Pure coffee powder particles are rich in aromatic oils and remain floating on the water surface for several minutes without immediately coloring the water. Chicory and roasted seed powder absorb water rapidly, sink quickly to the bottom, and leave a dark brown/caramel colored trail as they sink.",
        "safeTips": [
            "Carefully check the front and back labels: Under FSSAI laws, blends MUST declare exact percentages (e.g., 'Coffee 70%, Chicory 30%'). Pure coffee must state '100% Pure Coffee'.",
            "Purchase whole roasted beans from trusted estates and grind them freshly.",
            "Ensure packaging has a one-way aroma degassing valve and FSSAI credentials.",
            "Avoid loose, pungent brown powder sold in roadside tea/coffee stalls without ingredient lists."
        ],
        "storageTips": [
            "Store in an airtight, non-reactive glass or vacuum container.",
            "Keep in a dark, dry cabinet; avoid humidity and high heat.",
            "Use within 3 to 4 weeks of breaking the seal for optimal freshness and safety."
        ],
        "sources": [
            {
                "name": "Coffee Board of India Quality Guidelines",
                "url": "https://www.coffeeboard.gov.in"
            },
            {
                "name": "FSSAI Beverage Regulations on Coffee & Chicory",
                "url": "https://www.fssai.gov.in"
            }
        ]
    },
    "rice": {
        "foodName": "Rice",
        "category": "Grains",
        "aliases": ["raw rice", "boiled rice", "basmati rice", "biyyam", "chawal", "white rice"],
        "adulterants": [
            "Coating with Talc Powder or Chalk (mineral whitening)",
            "Liquid Paraffin / Mineral Oil Polish (for synthetic sheen)",
            "Mixing with Low-grade Broken Rice / Stones / Marble chips",
            "Urea soaking (to simulate aged basmati aroma)"
        ],
        "whyAdulterated": "Low-grade, weathered, or discolored rice is polished with talcum powder or mineral oil to make grains look pearlescent, translucent, and premium, fetching high prices.",
        "healthRisks": [
            "Talc and mineral oil coatings are difficult to wash out and can cause stomach irritation and chronic gastrointestinal inflammation.",
            "Mineral oil impairs nutrient absorption and carries petroleum residue risks.",
            "Stones and grit cause dental fractures and digestive complications."
        ],
        "testMethod": "Water Washing Cloudiness Test & Cooking Behavior Check",
        "testProcedure": "1. Soak a handful of rice in a clear glass of water and stir gently for 30 seconds.\n2. Observe the clarity of the water.\n3. Heat a small spoonful of grains directly on a flame using metal tongs.",
        "observation": "Pure rice will produce a naturally mild starchy haze when washed. Rice coated with heavy talc or chalk leaves an intense, milky white sediment at the bottom. For flame test: Pure rice grains char and smell like toasted cereal; plastic-coated or oil-polished grains emit a chemical stench or burn unnaturally with black sooty smoke.",
        "safeTips": [
            "Check for AGMARK certification, particularly for premium Basmati varieties.",
            "Inspect grains closely: Genuine aged rice has uniform natural ivory tone, not an artificial plastic gloss.",
            "Always wash rice thoroughly 2-3 times with fresh drinking water prior to cooking.",
            "Ensure sealed branded bags with clear batch numbers, FSSAI logo, and packaging dates."
        ],
        "storageTips": [
            "Store rice in a clean, airtight stainless steel or food-grade plastic drum.",
            "Add dried neem leaves, cloves, or turmeric roots to deter weevils and flour beetles naturally.",
            "Ensure storage containers are elevated off concrete floors to prevent moisture migration."
        ],
        "sources": [
            {
                "name": "FSSAI Cereals and Cereal Products Standards",
                "url": "https://www.fssai.gov.in"
            },
            {
                "name": "Department of Agriculture & Farmers Welfare - AGMARK Standards",
                "url": "https://agricoop.nic.in"
            }
        ]
    },
    "black pepper": {
        "foodName": "Black Pepper",
        "category": "Spices",
        "aliases": ["kali mirch", "black peppercorns", "miriyalu", "pepper"],
        "adulterants": [
            "Papaya Seeds (dried)",
            "Exhausted / Light Berries",
            "Mineral Oil coated berries"
        ],
        "whyAdulterated": "Dried papaya seeds bear an uncanny visual resemblance, size, and wrinkled surface to black peppercorns, allowing vendors to cut costs by up to 50%.",
        "healthRisks": [
            "Papaya seeds contain carpine and other active compounds that can cause stomach irritation, liver strain, and reproductive toxicity in pregnant women.",
            "Exhausted berries have zero piperine therapeutic value."
        ],
        "testMethod": "Alcohol / Water Float Test",
        "testProcedure": "1. Place sample peppercorns in a glass filled with water or alcohol (rubbing alcohol/ethanol).",
        "observation": "Pure mature black peppercorns sink steadily to the bottom due to high density. Papaya seeds and hollow exhausted berries float readily to the surface. Also, pressing a papaya seed with fingernails crushes it easily and reveals a distinct foul repulsive odour.",
        "safeTips": [
            "Buy whole black peppercorns that are heavy, dark, and uniform in size.",
            "Look for AGMARK Grade I markings on the spice pouch.",
            "Crush a few berries between your fingers: Pepper is hard to crush and emits a pungent spicy aroma."
        ],
        "storageTips": [
            "Keep in airtight glass containers in a dry, dark place.",
            "Grind peppercorns freshly when cooking rather than stocking pre-ground pepper."
        ],
        "sources": [
            {
                "name": "FSSAI DART Spices Guidelines",
                "url": "https://www.fssai.gov.in/dart/"
            }
        ]
    },
    "salt": {
        "foodName": "Common Salt / Table Salt",
        "category": "Packaged Foods",
        "aliases": ["table salt", "iodized salt", "uppu", "namak", "rock salt"],
        "adulterants": [
            "White Chalk Powder",
            "Insoluble Stone / Gypsum Powder",
            "Sand Grit"
        ],
        "whyAdulterated": "To increase bulk weight of salt packets using inexpensive industrial quarry by-products.",
        "healthRisks": [
            "Insoluble stone and chalk powder cause severe kidney stones, urinary tract irritation, and indigestion.",
            "May lack necessary mandatory iodine required to prevent goitre and mental development issues."
        ],
        "testMethod": "Water Clarity Dissolution Test",
        "testProcedure": "1. Stir 1 teaspoon of salt into a glass of clean warm water.",
        "observation": "Pure table salt dissolves completely, leaving a crystal clear solution. Chalk or white stone powder causes a thick white milky cloudiness that settles to the bottom as an insoluble white deposit.",
        "safeTips": [
            "Ensure the packet displays the 'Double Fortified' or 'Iodized Salt' FSSAI emblem with minimum 15 ppm iodine.",
            "Check for tamper-evident laminate packing."
        ],
        "storageTips": [
            "Store in ceramic, glass, or plastic jars with airtight seals; avoid metal containers which corrode.",
            "Keep away from steam to avoid clumping."
        ],
        "sources": [
            {
                "name": "FSSAI Salt Quality Standards",
                "url": "https://www.fssai.gov.in"
            }
        ]
    }
}

NON_FOOD_TERMS = {
    "laptop", "computer", "phone", "mobile", "smartphone", "tablet", "mouse", "keyboard",
    "monitor", "cpu", "television", "tv", "charger", "cable", "printer", "earphones",
    "headphones", "car", "bike", "motorcycle", "bicycle", "scooter", "truck", "bus",
    "train", "aeroplane", "airplane", "chair", "table", "desk", "bed", "sofa", "fan",
    "light", "bulb", "lamp", "door", "window", "curtain", "pen", "pencil", "eraser",
    "notebook", "book", "paper", "scissor", "scissors", "bag", "backpack", "shoe",
    "shoes", "sandal", "sandals", "shirt", "pant", "tshirt", "dress", "jeans", "jacket",
    "watch", "clock", "mirror", "plastic", "metal", "wood", "stone", "brick", "cement",
    "soap", "shampoo", "detergent", "perfume", "battery", "wire", "key", "lock",
    "camera", "drone", "robot", "software", "python", "react", "javascript", "code",
    "ai", "hardware", "wallet", "coin", "currency", "umbrella"
}

def is_definitely_non_food(query: str) -> bool:
    clean = query.strip().lower()
    if not clean:
        return False

    # Known food names and aliases should never be classified as non-food just because
    # they include a generic ingredient word such as "powder" or "oil".
    if clean in FOOD_KNOWLEDGE_BASE:
        return False
    for item in FOOD_KNOWLEDGE_BASE.values():
        if clean == item.get("foodName", "").lower():
            return False
        if any(clean == alias.lower() for alias in item.get("aliases", [])):
            return False

    words = clean.replace("-", " ").replace("_", " ").split()
    for w in words:
        if w in NON_FOOD_TERMS:
            return True
    return False

def get_food_by_name(name: str):
    clean = name.strip().lower()
    # Direct match
    if clean in FOOD_KNOWLEDGE_BASE:
        return FOOD_KNOWLEDGE_BASE[clean]
    # Check aliases
    for key, item in FOOD_KNOWLEDGE_BASE.items():
        if clean == key:
            return item
        if any(clean == alias or clean in alias or alias in clean for alias in item.get("aliases", [])):
            return item
    return None
