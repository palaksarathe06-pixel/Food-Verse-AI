"""
tabs/tab_meal_planner.py
Tab 5 – Personalized Meal Planner (Epic 5)
User profile form → BMR / TDEE calculation → Gemini generates an adaptive
7-day meal schedule with automated grocery shopping list.
"""

import streamlit as st
import plotly.graph_objects as go

from utils.gemini_client import generate_text, parse_json_response
from utils.prompts import MEAL_PLAN_PROMPT
from utils.demo_data import DEMO_MEAL_PLAN


# ── BMR / TDEE Calculation ──

def _calculate_bmr(gender: str, weight: float, height: float, age: int) -> float:
    """Mifflin-St Jeor equation."""
    if gender.lower() == "male":
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161


def _calculate_tdee(bmr: float, activity: str) -> float:
    """Multiply BMR by activity factor."""
    factors = {
        "Sedentary (office job)": 1.2,
        "Lightly Active (1-3 days/week)": 1.375,
        "Moderately Active (3-5 days/week)": 1.55,
        "Very Active (6-7 days/week)": 1.725,
        "Extremely Active (athlete)": 1.9,
    }
    return bmr * factors.get(activity, 1.55)


def _target_calories(tdee: float, goal: str) -> float:
    """Adjust TDEE based on fitness goal."""
    if goal == "Fat Loss":
        return tdee * 0.8  # 20% deficit
    elif goal == "Muscle Gain":
        return tdee * 1.15  # 15% surplus
    return tdee  # Maintenance


def _render_daily_calorie_chart(plan: dict):
    """Bar chart showing daily calorie totals across the week."""
    days = []
    totals = []
    target = plan.get("user_profile", {}).get("daily_calories", 0)

    weekly = plan.get("weekly_plan", {})
    for day_name in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
        day_data = weekly.get(day_name, {})
        total = sum(meal.get("calories", 0) for meal in day_data.values())
        days.append(day_name[:3])
        totals.append(total)

    colors = ["#FF6B6B" if t > target * 1.1 else "#00D2A0" if t <= target else "#FBBF24" for t in totals]

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=days,
            y=totals,
            marker=dict(color=colors, cornerradius=6),
            text=[f"{t}" for t in totals],
            textposition="outside",
            textfont=dict(color="#FAFAFA", size=12, family="Inter"),
            hovertemplate="<b>%{x}</b><br>%{y} kcal<extra></extra>",
        )
    )
    # Target line
    fig.add_hline(
        y=target,
        line_dash="dot",
        line_color="#A855F7",
        annotation_text=f"Target: {int(target)} kcal",
        annotation_font_color="#A855F7",
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(color="#94A3B8", showgrid=False),
        yaxis=dict(color="#64748B", showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
        margin=dict(t=30, b=30, l=40, r=20),
        height=280,
        showlegend=False,
    )
    return fig


def render():
    """Main render function for the Meal Planner tab."""
    st.markdown(
        """
        <div style="margin-bottom:1rem;">
            <h2 style="font-family:'Outfit',sans-serif; font-weight:700; margin-bottom:0.2rem;">
                📅 Personalized Meal Planner
            </h2>
            <p style="color:#94A3B8; font-size:0.95rem;">
                Enter your profile to calculate BMR/TDEE and generate an adaptive 7-day meal schedule with a grocery list.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── User Profile Form ──
    st.markdown(
        """
        <div class="glass-card">
            <span style="font-weight:600; color:#A855F7;">👤 Your Profile</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input("Age", min_value=10, max_value=100, value=28, key="mp_age")
        gender = st.selectbox("Gender", ["Male", "Female"], key="mp_gender")
    with col2:
        weight = st.number_input("Weight (kg)", min_value=30.0, max_value=250.0, value=75.0, step=0.5, key="mp_weight")
        height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=175.0, step=0.5, key="mp_height")
    with col3:
        activity = st.selectbox(
            "Activity Level",
            [
                "Sedentary (office job)",
                "Lightly Active (1-3 days/week)",
                "Moderately Active (3-5 days/week)",
                "Very Active (6-7 days/week)",
                "Extremely Active (athlete)",
            ],
            index=2,
            key="mp_activity",
        )
        diet = st.selectbox(
            "Dietary Constraints",
            ["None", "Vegan", "Vegetarian", "Keto", "Diabetic-Friendly", "Gluten-Free"],
            key="mp_diet",
        )

    goal = st.selectbox(
        "Fitness Goal",
        ["Fat Loss", "Maintenance", "Muscle Gain"],
        key="mp_goal",
    )

    # ── Calculate BMR / TDEE ──
    bmr = _calculate_bmr(gender, weight, height, age)
    tdee = _calculate_tdee(bmr, activity)
    target_cal = _target_calories(tdee, goal)

    # Show calculated values
    mc1, mc2, mc3 = st.columns(3)
    with mc1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value">{int(bmr)}</div>
                <div class="metric-label">BMR (kcal/day)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with mc2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value">{int(tdee)}</div>
                <div class="metric-label">TDEE (kcal/day)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with mc3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value">{int(target_cal)}</div>
                <div class="metric-label">Target Calories</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    col_gen, col_demo = st.columns([3, 1])
    with col_gen:
        generate_btn = st.button(
            "📅 Generate 7-Day Meal Plan",
            key="generate_meal_plan",
            use_container_width=True,
            type="primary",
        )
    with col_demo:
        use_demo = st.button("🎮 Try Demo", key="demo_meal_plan", use_container_width=True)

    plan = None

    if generate_btn:
        with st.spinner("🍽️ Crafting your personalized meal plan..."):
            if st.session_state.get("api_configured"):
                prompt = MEAL_PLAN_PROMPT.format(
                    age=age, gender=gender, weight=weight,
                    activity=activity, diet=diet, goal=goal,
                    bmr=int(bmr), tdee=int(tdee), target_cal=int(target_cal),
                )
                raw = generate_text(prompt, temperature=0.7)
                plan = parse_json_response(raw)
                if not plan or not plan.get("weekly_plan"):
                    st.warning("Could not parse AI response. Showing demo data.")
                    plan = DEMO_MEAL_PLAN
            else:
                st.info("💡 No API key — showing demonstration results.")
                plan = DEMO_MEAL_PLAN

    elif use_demo:
        plan = DEMO_MEAL_PLAN

    if plan:
        _render_meal_plan(plan)


def _render_meal_plan(plan: dict):
    """Render the full 7-day meal plan."""
    st.markdown("<br>", unsafe_allow_html=True)

    profile = plan.get("user_profile", {})
    macro_split = profile.get("macro_split", {})

    # ── Macro Split Badges ──
    st.markdown(
        f"""
        <div class="glass-card" style="border-left:4px solid #A855F7;">
            <div style="display:flex; gap:1rem; flex-wrap:wrap; align-items:center;">
                <span style="font-weight:600; color:#A855F7;">🎯 Macro Split:</span>
                <span class="badge badge-coral">🥩 Protein {macro_split.get('protein', 'N/A')}</span>
                <span class="badge badge-blue">🍞 Carbs {macro_split.get('carbs', 'N/A')}</span>
                <span class="badge badge-yellow">🧈 Fats {macro_split.get('fats', 'N/A')}</span>
                <span class="badge badge-green">🎯 Goal: {profile.get('goal', 'N/A')}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Weekly Calorie Chart ──
    st.markdown("##### 📊 Weekly Calorie Overview")
    fig = _render_daily_calorie_chart(plan)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Day-by-Day Plan ──
    st.markdown("##### 🗓️ Your 7-Day Meal Schedule")
    weekly = plan.get("weekly_plan", {})

    day_colors = {
        "Monday": "#FF6B6B", "Tuesday": "#FF8E53", "Wednesday": "#FBBF24",
        "Thursday": "#00D2A0", "Friday": "#4ECDC4", "Saturday": "#A855F7", "Sunday": "#FF6B6B",
    }

    for day_name in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
        day_data = weekly.get(day_name, {})
        if not day_data:
            continue

        day_total = sum(meal.get("calories", 0) for meal in day_data.values())
        color = day_colors.get(day_name, "#4ECDC4")

        with st.expander(f"📅 {day_name} — {day_total} kcal total", expanded=(day_name == "Monday")):
            meal_icons = {"breakfast": "🌅", "lunch": "☀️", "snack": "🍎", "dinner": "🌙"}

            for meal_type in ["breakfast", "lunch", "snack", "dinner"]:
                meal = day_data.get(meal_type)
                if not meal:
                    continue

                icon = meal_icons.get(meal_type, "🍽️")
                st.markdown(
                    f"""
                    <div class="day-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div>
                                <span class="meal-type">{icon} {meal_type}</span><br>
                                <span class="meal-name">{meal.get('meal', 'N/A')}</span>
                            </div>
                            <div style="text-align:right;">
                                <span style="font-family:'Outfit',sans-serif; font-weight:700; color:{color}; font-size:1.1rem;">
                                    {meal.get('calories', 0)} kcal
                                </span><br>
                                <span class="meal-macros">
                                    P: {meal.get('protein', '?')} · C: {meal.get('carbs', '?')} · F: {meal.get('fats', '?')}
                                </span>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Grocery List ──
    grocery = plan.get("grocery_list", {})
    if grocery:
        st.markdown("##### 🛒 Automated Grocery Shopping List")

        category_colors = {
            "Proteins": "#FF6B6B",
            "Grains & Carbs": "#FBBF24",
            "Fruits & Vegetables": "#00D2A0",
            "Pantry & Others": "#A855F7",
        }
        category_icons = {
            "Proteins": "🥩",
            "Grains & Carbs": "🌾",
            "Fruits & Vegetables": "🥬",
            "Pantry & Others": "🥫",
        }

        cols = st.columns(len(grocery))
        for col, (category, items) in zip(cols, grocery.items()):
            with col:
                icon = category_icons.get(category, "📦")
                color = category_colors.get(category, "#4ECDC4")
                st.markdown(
                    f"""
                    <div class="grocery-category" style="border-bottom-color:{color}; color:{color};">
                        {icon} {category}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                for item in items:
                    st.markdown(
                        f'<div class="grocery-item">• {item}</div>',
                        unsafe_allow_html=True,
                    )

        st.markdown("<br>", unsafe_allow_html=True)
        import json
        plan_json_str = json.dumps(plan, indent=2)
        st.download_button(
            label="📥 Export Meal Plan & Grocery List (JSON)",
            data=plan_json_str,
            file_name="foodverse_meal_plan.json",
            mime="application/json",
            use_container_width=True,
        )
