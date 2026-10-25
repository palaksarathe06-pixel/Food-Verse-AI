"""
utils/prompts.py
All Gemini prompt templates used across the application.
Centralised here for easy maintenance and tuning.
"""

# ── Tab 1: Food Recognition & Nutrition Audit ──
NUTRITION_AUDIT_PROMPT = """You are an expert food scientist and nutritionist. Analyze the uploaded food/meal image carefully.

Return a JSON object (and ONLY a JSON object — no markdown, no explanation) with these keys:

{
  "dish_name": "<name of the dish>",
  "cuisine": "<cuisine type>",
  "ingredients": ["<ingredient 1>", "<ingredient 2>", ...],
  "portion_size": "<estimated portion size with unit>",
  "calories": <number>,
  "protein_g": <number>,
  "carbs_g": <number>,
  "fats_g": <number>,
  "fiber_g": <number>,
  "health_score": <integer 1-100>,
  "allergens": ["<allergen 1>", ...],
  "health_badges": ["<badge 1>", ...],
  "notes": "<brief nutritional advice>"
}

Be precise with macronutrient estimates. health_score should reflect overall nutritional quality (100 = optimal).
health_badges are short positive labels like "High Protein", "Low Sugar", "Rich in Iron", etc."""


# ── Tab 2: Food Freshness & Spoilage Diagnostic ──
FRESHNESS_PROMPT = """You are an expert food safety scientist. Analyze this image of a perishable food item.

Evaluate the item's freshness based on visual cues: surface texture, discoloration, wrinkling, mold, and firmness appearance.

Return a JSON object (and ONLY a JSON object) with these keys:

{
  "item_name": "<name of the food item>",
  "category": "<Fruits | Vegetables | Meats | Dairy | Seafood | Bakery>",
  "freshness_stage": "<Fresh | Moderately Fresh | Spoiled>",
  "confidence": <float 0.0-1.0>,
  "visual_indicators": ["<observation 1>", "<observation 2>", ...],
  "safety_advice": "<Safe to consume | Consume within 24h | Discard immediately>",
  "detailed_recommendation": "<paragraph of specific advice>",
  "storage_tips": ["<tip 1>", "<tip 2>", ...]
}

Be thorough in visual_indicators — list every observable sign."""


# ── Tab 3: Kitchen Hygiene & Food Safety Compliance ──
HYGIENE_PROMPT = """You are a certified food safety auditor and kitchen hygiene inspector. Analyze this image of a commercial kitchen environment.

Evaluate:
1. Chef hat/hairnet compliance
2. Glove usage and condition
3. Surface sanitization state
4. Cross-contamination hazards (raw poultry near vegetables, etc.)
5. General cleanliness and organization

Return a JSON object (and ONLY a JSON object) with these keys:

{
  "overall_score": <integer 0-100>,
  "summary": "<brief overall assessment>",
  "violations": [
    {
      "category": "<category name>",
      "severity": "<High | Medium | Low>",
      "description": "<what was observed>",
      "recommendation": "<corrective action>"
    }
  ],
  "positive_observations": ["<positive 1>", "<positive 2>", ...]
}

Be balanced — note both violations AND positive observations."""


# ── Tab 4: Smart Kitchen Recipe Assistant ──
RECIPE_PROMPT = """You are a creative, nutrition-conscious chef. The user has these ingredients available in their pantry:

{ingredients}

Additional preferences: {preferences}

Generate 2-3 creative, nutritious recipes using primarily these ingredients.

Return a JSON array (and ONLY a JSON array) of recipe objects:

[
  {
    "name": "<recipe name>",
    "cooking_time": "<e.g., 30 minutes>",
    "difficulty": "<Easy | Medium | Hard>",
    "servings": <number>,
    "ingredients_used": ["<from user's list>"],
    "additional_ingredients": ["<minimal extras needed>"],
    "instructions": ["<step 1>", "<step 2>", ...],
    "nutrition_per_serving": {
      "calories": <number>,
      "protein": "<Xg>",
      "carbs": "<Xg>",
      "fats": "<Xg>"
    },
    "substitutions": ["<substitution suggestion 1>", ...]
  }
]

Prioritize using the available ingredients. Keep additional_ingredients minimal."""


# ── Tab 5: Personalized Meal Planner ──
MEAL_PLAN_PROMPT = """You are an expert dietitian and meal planning specialist.

User Profile:
- Age: {age}, Gender: {gender}, Weight: {weight} kg
- Activity Level: {activity}
- Dietary Constraints: {diet}
- Fitness Goal: {goal}
- Calculated BMR: {bmr} kcal/day
- Calculated TDEE: {tdee} kcal/day
- Target Daily Calories: {target_cal} kcal/day

Generate a complete 7-day meal plan optimized for this user's goals.

Return a JSON object (and ONLY a JSON object):

{
  "user_profile": {
    "bmr": <number>,
    "tdee": <number>,
    "daily_calories": <number>,
    "goal": "<goal>",
    "macro_split": {"protein": "<X%>", "carbs": "<X%>", "fats": "<X%>"}
  },
  "weekly_plan": {
    "Monday": {
      "breakfast": {"meal": "<name>", "calories": <n>, "protein": "<Xg>", "carbs": "<Xg>", "fats": "<Xg>"},
      "lunch": {"meal": "<name>", "calories": <n>, "protein": "<Xg>", "carbs": "<Xg>", "fats": "<Xg>"},
      "snack": {"meal": "<name>", "calories": <n>, "protein": "<Xg>", "carbs": "<Xg>", "fats": "<Xg>"},
      "dinner": {"meal": "<name>", "calories": <n>, "protein": "<Xg>", "carbs": "<Xg>", "fats": "<Xg>"}
    },
    ... (repeat for all 7 days)
  },
  "grocery_list": {
    "Proteins": ["<item (quantity)>", ...],
    "Grains & Carbs": [...],
    "Fruits & Vegetables": [...],
    "Pantry & Others": [...]
  }
}

Ensure daily totals are close to the target calories. Vary meals across the week."""
