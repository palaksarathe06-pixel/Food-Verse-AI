"""
tabs/tab_recipe.py
Tab 4 – Smart Kitchen Recipe Assistant (Epic 4)
Pantry inventory input → Gemini generates creative, nutritious recipes
with cooking time, difficulty, step-by-step instructions, and substitutions.
"""

import streamlit as st

from PIL import Image
from utils.gemini_client import (
    generate_text,
    generate_with_image,
    generate_with_audio,
    parse_json_response,
)
from utils.prompts import RECIPE_PROMPT
from utils.demo_data import DEMO_RECIPES


def render():
    """Main render function for the Recipe Assistant tab."""
    st.markdown(
        """
        <div style="margin-bottom:1rem;">
            <h2 style="font-family:'Outfit',sans-serif; font-weight:700; margin-bottom:0.2rem;">
                👨‍🍳 Smart Kitchen Recipe Assistant
            </h2>
            <p style="color:#94A3B8; font-size:0.95rem;">
                Input your available ingredients via text, fridge photo, or voice query — AI crafts tailored recipes with step-by-step guidance.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "pantry_text" not in st.session_state:
        st.session_state.pantry_text = "Chicken breast, bell peppers, onion, garlic, olive oil, rice, tomatoes, lemon"

    # ── Multimodal Input Methods ──
    input_mode = st.radio(
        "Choose Input Method",
        ["✍️ Text Input", "📸 Scan Fridge / Pantry Photo", "🎙️ Voice Query / Audio Note"],
        horizontal=True,
        key="recipe_input_mode",
    )

    if input_mode == "📸 Scan Fridge / Pantry Photo":
        uploaded_pantry_img = st.file_uploader(
            "Upload a photo of your fridge or pantry shelf",
            type=["jpg", "jpeg", "png", "webp"],
            key="pantry_photo_uploader",
        )
        if uploaded_pantry_img is not None:
            col_p1, col_p2 = st.columns([1, 2])
            with col_p1:
                pantry_pil = Image.open(uploaded_pantry_img)
                st.image(pantry_pil, caption="Uploaded Pantry/Fridge", use_container_width=True)
            with col_p2:
                if st.button("🔍 Detect Ingredients from Photo", use_container_width=True, type="secondary"):
                    with st.spinner("AI scanning ingredients..."):
                        if st.session_state.get("api_configured"):
                            vision_prompt = (
                                "Look at this fridge/pantry photo. Identify and list all raw food ingredients, "
                                "produce, dairy, meats, condiments, and grains visible. "
                                "Return ONLY a clean comma-separated list of ingredient names."
                            )
                            detected = generate_with_image(vision_prompt, pantry_pil)
                            if detected and not detected.startswith("["):
                                st.session_state.pantry_text = detected.strip()
                                st.success("✅ Ingredients detected and loaded into pantry below!")
                            else:
                                st.warning("Could not auto-detect ingredients. Please enter manually.")
                        else:
                            st.session_state.pantry_text = "Eggs, milk, cheddar cheese, spinach, mushrooms, butter"
                            st.info("Demo: Auto-filled sample fridge ingredients.")

    elif input_mode == "🎙️ Voice Query / Audio Note":
        uploaded_audio = st.file_uploader(
            "Upload a voice note describing what you have or want to cook (WAV, MP3, M4A)",
            type=["wav", "mp3", "m4a", "ogg"],
            key="pantry_audio_uploader",
        )
        if uploaded_audio is not None:
            st.audio(uploaded_audio)
            if st.button("🎧 Transcribe & Extract Ingredients", use_container_width=True, type="secondary"):
                with st.spinner("AI analyzing voice recording..."):
                    if st.session_state.get("api_configured"):
                        mime = "audio/wav" if uploaded_audio.name.endswith(".wav") else "audio/mp3"
                        audio_prompt = (
                            "Extract all food ingredients and dish requests mentioned in this audio recording. "
                            "Return ONLY a clean comma-separated list of ingredients."
                        )
                        detected_audio = generate_with_audio(audio_prompt, uploaded_audio.getvalue(), mime_type=mime)
                        if detected_audio and not detected_audio.startswith("["):
                            st.session_state.pantry_text = detected_audio.strip()
                            st.success("✅ Voice query processed and loaded into pantry below!")
                        else:
                            st.warning("Could not process audio. Please enter manually.")
                    else:
                        st.session_state.pantry_text = "Salmon fillet, asparagus, lemon, garlic, olive oil, quinoa"
                        st.info("Demo: Auto-filled voice note ingredients.")

    # ── Ingredient Input Text Area ──
    ingredients_input = st.text_area(
        "Available Ingredients (comma-separated)",
        value=st.session_state.pantry_text,
        placeholder="e.g., Chicken breast, bell peppers, onion, garlic, olive oil, rice, tomatoes, lemon...",
        height=90,
        key="recipe_ingredients_input",
    )

    col1, col2 = st.columns(2)
    with col1:
        diet_pref = st.selectbox(
            "Dietary Preference",
            ["No Restriction", "Vegetarian", "Vegan", "Keto", "Gluten-Free", "Dairy-Free", "Low-Carb"],
            key="recipe_diet",
        )
    with col2:
        cooking_skill = st.selectbox(
            "Cooking Skill Level",
            ["Beginner", "Intermediate", "Advanced"],
            key="recipe_skill",
        )

    col_gen, col_demo = st.columns([3, 1])

    with col_gen:
        generate_btn = st.button(
            "🍳 Generate Recipes",
            key="generate_recipes",
            use_container_width=True,
            type="primary",
        )

    with col_demo:
        use_demo = st.button("🎮 Try Demo", key="demo_recipe", use_container_width=True)

    recipes = None

    if generate_btn and ingredients_input.strip():
        with st.spinner("👨‍🍳 Crafting delicious recipes for you..."):
            if st.session_state.get("api_configured"):
                preferences = f"Diet: {diet_pref}, Skill: {cooking_skill}"
                prompt = RECIPE_PROMPT.format(
                    ingredients=ingredients_input.strip(),
                    preferences=preferences,
                )
                raw = generate_text(prompt, temperature=0.8)
                parsed = parse_json_response(raw)
                if isinstance(parsed, list) and len(parsed) > 0:
                    recipes = parsed
                elif isinstance(parsed, dict) and "recipes" in parsed:
                    recipes = parsed["recipes"]
                else:
                    st.warning("Could not parse AI response. Showing demonstration recipes.")
                    recipes = DEMO_RECIPES
            else:
                st.info("💡 No API key — showing demonstration results.")
                recipes = DEMO_RECIPES

    elif generate_btn and not ingredients_input.strip():
        st.warning("Please enter at least a few ingredients to generate recipes.")

    elif use_demo:
        recipes = DEMO_RECIPES

    if recipes:
        _render_recipes(recipes)


def _render_recipes(recipes: list):
    """Render recipe cards with full details."""
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:1rem;">
            <span class="live-dot"></span>
            <span style="color:#00D2A0; font-weight:600; font-size:0.9rem;">
                {len(recipes)} Recipe{'s' if len(recipes) != 1 else ''} Generated
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for idx, recipe in enumerate(recipes):
        difficulty = recipe.get("difficulty", "Easy")
        diff_badge = "badge-green" if difficulty == "Easy" else "badge-yellow" if difficulty == "Medium" else "badge-coral"

        st.markdown(
            f"""
            <div class="recipe-card">
                <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap;">
                    <div class="recipe-title">🍽️ {recipe.get('name', f'Recipe {idx+1}')}</div>
                    <div>
                        <span class="badge {diff_badge}">{difficulty}</span>
                        <span class="badge badge-blue">⏱ {recipe.get('cooking_time', 'N/A')}</span>
                        <span class="badge badge-purple">🍴 {recipe.get('servings', '?')} servings</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.expander(f"📖 View Full Recipe: {recipe.get('name', '')}", expanded=(idx == 0)):
            col_ing, col_extra = st.columns(2)

            with col_ing:
                st.markdown("**🥘 Ingredients Used (from your pantry)**")
                for ing in recipe.get("ingredients_used", []):
                    st.markdown(f"<span style='color:#4ECDC4;'>●</span> {ing}", unsafe_allow_html=True)

            with col_extra:
                extras = recipe.get("additional_ingredients", [])
                if extras:
                    st.markdown("**🛒 Additional Ingredients Needed**")
                    for ing in extras:
                        st.markdown(f"<span style='color:#FF8E53;'>●</span> {ing}", unsafe_allow_html=True)

            st.markdown("---")

            # Step-by-step instructions
            st.markdown("**📝 Step-by-Step Instructions**")
            for i, step in enumerate(recipe.get("instructions", []), 1):
                st.markdown(
                    f"""
                    <div class="step-item">
                        <div class="step-number">{i}</div>
                        <div class="step-text">{step}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown("---")

            # Nutrition per serving
            nutrition = recipe.get("nutrition_per_serving", {})
            if nutrition:
                st.markdown("**📊 Nutrition Per Serving**")
                nc1, nc2, nc3, nc4 = st.columns(4)
                with nc1:
                    st.metric("🔥 Calories", nutrition.get("calories", "N/A"))
                with nc2:
                    st.metric("🥩 Protein", nutrition.get("protein", "N/A"))
                with nc3:
                    st.metric("🍞 Carbs", nutrition.get("carbs", "N/A"))
                with nc4:
                    st.metric("🧈 Fats", nutrition.get("fats", "N/A"))

            # Substitutions
            subs = recipe.get("substitutions", [])
            if subs:
                st.markdown("**🔄 Ingredient Substitutions**")
                for sub in subs:
                    st.markdown(
                        f"""<div style="padding:0.2rem 0; color:#FAFAFA; font-size:0.9rem;">
                            <span style="color:#A855F7;">↔</span> {sub}
                        </div>""",
                        unsafe_allow_html=True,
                    )
