"""
utils/demo_data.py
Pre-built demonstration data used when no API key is configured.
Allows the full UI to be exercised without incurring API costs.
"""

# ---------- Tab 1 – Food Recognition Demo ----------
DEMO_NUTRITION = {
    "dish_name": "Grilled Chicken Caesar Salad",
    "cuisine": "American / Mediterranean",
    "ingredients": [
        "Grilled chicken breast",
        "Romaine lettuce",
        "Parmesan cheese",
        "Caesar dressing",
        "Croutons",
        "Lemon juice",
    ],
    "portion_size": "350 g (1 large bowl)",
    "calories": 420,
    "protein_g": 38,
    "carbs_g": 18,
    "fats_g": 22,
    "fiber_g": 4,
    "health_score": 78,
    "allergens": ["Dairy", "Gluten", "Eggs"],
    "health_badges": ["High Protein", "Low Carb", "Rich in Vitamin A"],
    "notes": "A well-balanced meal rich in lean protein. Consider reducing dressing for lower fat content.",
}

# ---------- Tab 2 – Freshness Diagnostic Demo ----------
DEMO_FRESHNESS = {
    "item_name": "Roma Tomatoes",
    "category": "Vegetables",
    "freshness_stage": "Moderately Fresh",
    "confidence": 0.82,
    "visual_indicators": [
        "Slight wrinkling near stem area",
        "Color is mostly uniform red with minor soft spots",
        "No visible mold or discoloration",
        "Skin firmness appears acceptable",
    ],
    "safety_advice": "Consume within 24h",
    "detailed_recommendation": (
        "These tomatoes are still safe to eat but are past peak freshness. "
        "Use them in cooked dishes like sauces, soups, or stews rather than "
        "raw salads. Store in the refrigerator at 4°C to slow further degradation."
    ),
    "storage_tips": [
        "Refrigerate immediately at 1-4 °C",
        "Do not store near ethylene-producing fruits (bananas, apples)",
        "Use within 1-2 days for best quality",
        "If making sauce, cook today and freeze for up to 3 months",
    ],
}

# ---------- Tab 3 – Kitchen Hygiene Demo ----------
DEMO_HYGIENE = {
    "overall_score": 72,
    "summary": (
        "The kitchen shows moderate compliance with food safety standards. "
        "Key issues were identified around glove usage and cross-contamination risks."
    ),
    "violations": [
        {
            "category": "Glove Usage",
            "severity": "High",
            "description": "Staff member handling raw chicken without changing gloves before touching vegetables.",
            "recommendation": "Implement mandatory glove change protocol between raw protein and produce handling.",
        },
        {
            "category": "Hair/Hairnet Compliance",
            "severity": "Medium",
            "description": "One staff member's hairnet does not fully cover hair.",
            "recommendation": "Provide properly sized hairnets and enforce full coverage.",
        },
        {
            "category": "Surface Sanitization",
            "severity": "Low",
            "description": "Cutting board shows minor staining but appears recently cleaned.",
            "recommendation": "Replace cutting boards showing deep grooves or permanent stains.",
        },
        {
            "category": "Cross-Contamination",
            "severity": "High",
            "description": "Raw poultry stored on shelf directly above ready-to-eat salad ingredients.",
            "recommendation": "Store raw proteins on lowest shelf, ready-to-eat items on upper shelves.",
        },
    ],
    "positive_observations": [
        "Temperature display visible and within range (3°C)",
        "Hand washing station accessible and stocked",
        "Floor area clean and dry",
    ],
}

# ---------- Tab 4 – Recipe Assistant Demo ----------
DEMO_RECIPES = [
    {
        "name": "One-Pan Lemon Herb Chicken with Roasted Vegetables",
        "cooking_time": "40 minutes",
        "difficulty": "Easy",
        "servings": 4,
        "ingredients_used": ["Chicken breast", "Bell peppers", "Onion", "Garlic", "Olive oil", "Lemon"],
        "additional_ingredients": ["Fresh rosemary", "Salt", "Black pepper"],
        "instructions": [
            "Preheat oven to 200°C (400°F).",
            "Cut chicken into uniform pieces and season with salt, pepper, and lemon zest.",
            "Chop bell peppers and onion into chunks, mince garlic.",
            "Toss vegetables with olive oil, salt, and pepper on a large baking sheet.",
            "Nestle chicken pieces among the vegetables.",
            "Squeeze lemon juice over everything and add rosemary sprigs.",
            "Roast for 35-40 minutes until chicken reaches 74°C (165°F) internal temperature.",
            "Rest for 5 minutes before serving.",
        ],
        "nutrition_per_serving": {"calories": 310, "protein": "32g", "carbs": "12g", "fats": "15g"},
        "substitutions": [
            "Replace chicken with tofu for a vegan option",
            "Use sweet potatoes instead of bell peppers for more carbs",
        ],
    },
    {
        "name": "Garlic Butter Shrimp Pasta",
        "cooking_time": "25 minutes",
        "difficulty": "Easy",
        "servings": 3,
        "ingredients_used": ["Pasta", "Garlic", "Olive oil", "Butter"],
        "additional_ingredients": ["Shrimp", "Red pepper flakes", "Parsley", "Parmesan"],
        "instructions": [
            "Cook pasta according to package directions, reserve 1 cup pasta water.",
            "Heat olive oil and butter in a large skillet over medium-high heat.",
            "Add minced garlic and red pepper flakes, sauté 30 seconds.",
            "Add shrimp in a single layer, cook 2 minutes per side until pink.",
            "Toss in cooked pasta with a splash of pasta water.",
            "Garnish with parsley and parmesan before serving.",
        ],
        "nutrition_per_serving": {"calories": 480, "protein": "28g", "carbs": "52g", "fats": "18g"},
        "substitutions": [
            "Use gluten-free pasta for celiac-friendly version",
            "Replace shrimp with mushrooms for vegetarian option",
        ],
    },
]

# ---------- Tab 5 – Meal Planner Demo ----------
DEMO_MEAL_PLAN = {
    "user_profile": {
        "bmr": 1680,
        "tdee": 2310,
        "daily_calories": 1850,
        "goal": "Fat Loss",
        "macro_split": {"protein": "35%", "carbs": "40%", "fats": "25%"},
    },
    "weekly_plan": {
        "Monday": {
            "breakfast": {"meal": "Greek Yogurt Parfait with Berries & Granola", "calories": 380, "protein": "22g", "carbs": "48g", "fats": "12g"},
            "lunch": {"meal": "Grilled Chicken Quinoa Bowl with Avocado", "calories": 520, "protein": "42g", "carbs": "45g", "fats": "18g"},
            "snack": {"meal": "Apple Slices with Almond Butter", "calories": 210, "protein": "6g", "carbs": "24g", "fats": "12g"},
            "dinner": {"meal": "Baked Salmon with Steamed Broccoli & Brown Rice", "calories": 480, "protein": "38g", "carbs": "35g", "fats": "20g"},
        },
        "Tuesday": {
            "breakfast": {"meal": "Spinach & Mushroom Egg White Omelette", "calories": 290, "protein": "28g", "carbs": "8g", "fats": "16g"},
            "lunch": {"meal": "Turkey & Avocado Whole Wheat Wrap", "calories": 450, "protein": "35g", "carbs": "38g", "fats": "18g"},
            "snack": {"meal": "Mixed Nuts & Dark Chocolate (30g)", "calories": 220, "protein": "6g", "carbs": "14g", "fats": "16g"},
            "dinner": {"meal": "Lean Beef Stir-Fry with Mixed Vegetables", "calories": 420, "protein": "36g", "carbs": "28g", "fats": "18g"},
        },
        "Wednesday": {
            "breakfast": {"meal": "Overnight Oats with Chia Seeds & Banana", "calories": 360, "protein": "14g", "carbs": "56g", "fats": "10g"},
            "lunch": {"meal": "Mediterranean Chickpea Salad", "calories": 410, "protein": "18g", "carbs": "48g", "fats": "18g"},
            "snack": {"meal": "Protein Smoothie (Whey, Banana, Milk)", "calories": 280, "protein": "30g", "carbs": "32g", "fats": "4g"},
            "dinner": {"meal": "Grilled Tilapia with Sweet Potato Mash", "calories": 440, "protein": "34g", "carbs": "42g", "fats": "14g"},
        },
        "Thursday": {
            "breakfast": {"meal": "Whole Grain Toast with Avocado & Poached Eggs", "calories": 400, "protein": "20g", "carbs": "32g", "fats": "22g"},
            "lunch": {"meal": "Chicken Caesar Salad (Light Dressing)", "calories": 380, "protein": "36g", "carbs": "14g", "fats": "20g"},
            "snack": {"meal": "Cottage Cheese with Pineapple", "calories": 180, "protein": "18g", "carbs": "20g", "fats": "4g"},
            "dinner": {"meal": "Vegetable Curry with Basmati Rice", "calories": 460, "protein": "14g", "carbs": "62g", "fats": "16g"},
        },
        "Friday": {
            "breakfast": {"meal": "Protein Pancakes with Berries", "calories": 350, "protein": "28g", "carbs": "40g", "fats": "8g"},
            "lunch": {"meal": "Tuna Nicoise Salad", "calories": 420, "protein": "34g", "carbs": "22g", "fats": "22g"},
            "snack": {"meal": "Rice Cakes with Peanut Butter", "calories": 200, "protein": "8g", "carbs": "24g", "fats": "10g"},
            "dinner": {"meal": "Herb-Crusted Chicken with Roasted Vegetables", "calories": 440, "protein": "40g", "carbs": "24g", "fats": "20g"},
        },
        "Saturday": {
            "breakfast": {"meal": "Smoothie Bowl with Acai & Mixed Toppings", "calories": 380, "protein": "12g", "carbs": "58g", "fats": "12g"},
            "lunch": {"meal": "Black Bean & Sweet Potato Burrito Bowl", "calories": 490, "protein": "22g", "carbs": "62g", "fats": "16g"},
            "snack": {"meal": "Greek Yogurt with Honey", "calories": 160, "protein": "16g", "carbs": "20g", "fats": "2g"},
            "dinner": {"meal": "Grilled Shrimp Skewers with Couscous Salad", "calories": 400, "protein": "32g", "carbs": "38g", "fats": "14g"},
        },
        "Sunday": {
            "breakfast": {"meal": "Veggie Frittata with Whole Wheat Toast", "calories": 390, "protein": "24g", "carbs": "30g", "fats": "20g"},
            "lunch": {"meal": "Lentil Soup with Crusty Bread", "calories": 380, "protein": "20g", "carbs": "52g", "fats": "8g"},
            "snack": {"meal": "Trail Mix (40g)", "calories": 200, "protein": "6g", "carbs": "18g", "fats": "14g"},
            "dinner": {"meal": "Pan-Seared Cod with Asparagus & Quinoa", "calories": 420, "protein": "36g", "carbs": "32g", "fats": "16g"},
        },
    },
    "grocery_list": {
        "Proteins": ["Chicken breast (1.5 kg)", "Salmon fillets (400g)", "Shrimp (300g)", "Tilapia (400g)", "Cod fillets (400g)", "Lean beef (300g)", "Turkey deli slices (200g)", "Eggs (1 dozen)", "Greek yogurt (1 kg)", "Cottage cheese (250g)", "Whey protein (500g)", "Tuna canned (2 cans)"],
        "Grains & Carbs": ["Quinoa (500g)", "Brown rice (500g)", "Basmati rice (500g)", "Whole wheat wraps (6)", "Whole grain bread (1 loaf)", "Rolled oats (500g)", "Pasta (500g)", "Couscous (250g)", "Rice cakes (1 pack)", "Granola (250g)"],
        "Fruits & Vegetables": ["Spinach (200g)", "Broccoli (2 heads)", "Mixed salad greens (300g)", "Bell peppers (4)", "Sweet potatoes (4)", "Asparagus (1 bunch)", "Mushrooms (250g)", "Avocados (4)", "Bananas (6)", "Berries mixed (500g)", "Apples (4)", "Lemons (3)", "Pineapple (1 can)"],
        "Pantry & Others": ["Olive oil", "Almond butter", "Peanut butter", "Chia seeds", "Mixed nuts (200g)", "Dark chocolate (100g)", "Honey", "Black beans (2 cans)", "Lentils (500g)", "Chickpeas (2 cans)", "Trail mix (200g)"],
    },
}
