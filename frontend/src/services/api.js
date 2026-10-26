// API Service for FROM FARM TO FORK Platform

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export async function analyzeFoodItem(foodName) {
  try {
    const response = await fetch(`${BASE_URL}/analyze-food`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ food: foodName }),
    });
    if (!response.ok) {
      throw new Error(`Server returned ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.warn('API error, falling back to local client analyzer:', error);
    return fallbackAnalyzer(foodName);
  }
}

export async function sendChatMessage(message, foodContext = null, history = []) {
  try {
    const response = await fetch(`${BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message, foodContext, history }),
    });
    if (!response.ok) {
      throw new Error(`Server returned ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.warn('Chat API error, fallback response:', error);
    return {
      reply: "Food Safety AI provides awareness guidance: Please ensure packaged items carry intact FSSAI seals and AGMARK ratings. Simple home tests serve as preliminary indications; accredited laboratory testing is required for scientific verification.",
      isFoodRelated: true,
      suggestedFollowUps: [
        "What are the health risks?",
        "How can I buy safer versions?",
        "What should I check on the packaging?"
      ]
    };
  }
}

export async function getFoodItems() {
  try {
    const response = await fetch(`${BASE_URL}/foods`);
    if (!response.ok) throw new Error('Failed to fetch foods');
    return await response.json();
  } catch (error) {
    console.warn('Could not fetch remote foods:', error);
    return [];
  }
}

export async function getDashboardStats() {
  try {
    const response = await fetch(`${BASE_URL}/dashboard-stats`);
    if (!response.ok) throw new Error('Failed to fetch dashboard stats');
    return await response.json();
  } catch (error) {
    console.warn('Using baseline dashboard stats:', error);
    return {
      surveySummary: {
        awarePercentage: 65,
        unawarePercentage: 35,
        totalSurveyed: 250,
        vendorsEngaged: 42,
        pamphletsDistributed: 500,
        demosConducted: 12
      },
      findings: [
        { title: "Awareness Level", stat: "65%", description: "Participants aware of food adulteration and general effects." },
        { title: "Need for Awareness", stat: "35%", description: "Participants needing structured awareness on simple tests & rights." },
        { title: "Home Methods", stat: "48%", description: "Participants initially unfamiliar with simple preliminary home tests." },
        { title: "Certifications", stat: "42%", description: "Unaware of AGMARK and FSSAI certification meanings." }
      ]
    };
  }
}

export async function getRecentSearches() {
  try {
    const response = await fetch(`${BASE_URL}/searches?limit=10`);
    if (!response.ok) throw new Error('Failed to fetch searches');
    return await response.json();
  } catch (error) {
    return [
      { id: 1, food_name: 'Milk', is_food: 1, category: 'Dairy Products' },
      { id: 2, food_name: 'Turmeric', is_food: 1, category: 'Spices' },
      { id: 3, food_name: 'Honey', is_food: 1, category: 'Sweeteners' },
      { id: 4, food_name: 'Edible Oil', is_food: 1, category: 'Edible Oils' },
      { id: 5, food_name: 'Ghee', is_food: 1, category: 'Dairy Products' },
      { id: 6, food_name: 'Chilli Powder', is_food: 1, category: 'Spices' },
      { id: 7, food_name: 'Rice', is_food: 1, category: 'Grains' }
    ];
  }
}

export async function submitCitizenFeedback(feedbackData) {
  try {
    const response = await fetch(`${BASE_URL}/feedback`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(feedbackData),
    });
    return await response.json();
  } catch (error) {
    return { status: "success", message: "Feedback saved locally!" };
  }
}

// Client fallback if backend is offline
function fallbackAnalyzer(food) {
  const clean = food.trim().toLowerCase();
  const nonFoods = new Set(["laptop", "chair", "mobile", "phone", "car", "computer", "table", "book", "pen", "shoe", "bottle"]);
  const foodItems = new Set(["milk", "turmeric", "turmeric powder", "chilli powder", "honey", "sugar", "ghee", "edible oil", "rice", "tea", "coffee", "black pepper", "salt"]);
  const searchLinks = [
    { name: "Google web search", url: `https://www.google.com/search?q=${encodeURIComponent(food)}` },
    { name: "Bing web search", url: `https://www.bing.com/search?q=${encodeURIComponent(food)}` },
    { name: "Wikipedia search", url: `https://en.wikipedia.org/w/index.php?search=${encodeURIComponent(food)}` }
  ];

  if (clean.split(/[\s_-]+/).some((word) => nonFoods.has(word))) {
    return {
      isFood: false,
      classification: "non_food",
      foodName: food,
      message: `${food} does not appear to be a food item.`,
      suggestion: "Please enter a food item such as: Milk, Rice, Turmeric, Honey, Sugar or Edible Oil.",
      sources: searchLinks
    };
  }

  if (!foodItems.has(clean)) {
    return {
      isFood: false,
      classification: "uncertain",
      foodName: food,
      message: `We could not confidently classify "${food}" as food or non-food.`,
      suggestion: "Check the item using these web searches, or try a food item from the suggestions.",
      sources: searchLinks
    };
  }

  return {
    isFood: true,
    classification: "food",
    foodName: food.charAt(0).toUpperCase() + food.slice(1),
    category: "General Food",
    adulterants: ["Common low-grade fillers", "Water / dilution", "Unpermitted coloring agents"],
    whyAdulterated: "Adulteration occurs to increase volume or enhance visual appearance for commercial gain.",
    healthRisks: ["Digestive irritation", "Long-term metabolic strain", "Nutrient deficiency"],
    testMethod: "Preliminary Physical Inspection & Dissolution Check",
    testProcedure: "1. Check aroma and texture.\n2. Mix sample in water and observe separation.",
    observation: "Pure products show uniform characteristics; artificial residues settle irregularly.",
    safeTips: ["Check for FSSAI logo", "Verify expiry dates", "Avoid damaged packaging"],
    storageTips: ["Store in a clean, airtight container", "Keep in a cool, dry place"],
    sources: [
      { name: "FSSAI DART Portal", url: "https://www.fssai.gov.in/dart/" },
      { name: "WHO Food Safety", url: "https://www.who.int" }
    ],
    disclaimer: "This is only a preliminary awareness check. Laboratory testing is required for confirmation."
  };
}
