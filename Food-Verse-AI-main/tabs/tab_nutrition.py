"""
tabs/tab_nutrition.py
Tab 1 – Food Recognition & Nutrition Audit (Epic 2)
Upload a meal photo → Gemini Vision identifies the dish, cuisine, ingredients,
and provides a full macro/micro nutrient breakdown with health badges.
"""

import streamlit as st
from PIL import Image
import plotly.graph_objects as go

from utils.gemini_client import generate_with_image, parse_json_response
from utils.prompts import NUTRITION_AUDIT_PROMPT
from utils.demo_data import DEMO_NUTRITION


def _render_macro_chart(data: dict):
    """Render an interactive donut chart for macro breakdown."""
    labels = ["Protein", "Carbs", "Fats", "Fiber"]
    values = [
        data.get("protein_g", 0),
        data.get("carbs_g", 0),
        data.get("fats_g", 0),
        data.get("fiber_g", 0),
    ]
    colors = ["#FF6B6B", "#4ECDC4", "#FBBF24", "#A855F7"]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.55,
                marker=dict(colors=colors, line=dict(color="#0E1117", width=2)),
                textinfo="label+percent",
                textfont=dict(size=13, color="#FAFAFA", family="Inter"),
                hovertemplate="<b>%{label}</b><br>%{value}g (%{percent})<extra></extra>",
            )
        ]
    )
    fig.update_layout(
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=20, b=20, l=20, r=20),
        height=300,
        annotations=[
            dict(
                text=f"<b>{data.get('calories', 0)}</b><br><span style='font-size:11px;color:#94A3B8'>kcal</span>",
                x=0.5, y=0.5,
                font=dict(size=24, color="#FAFAFA", family="Outfit"),
                showarrow=False,
            )
        ],
    )
    return fig


def _get_score_color(score: int) -> str:
    if score >= 80:
        return "#00D2A0"
    elif score >= 60:
        return "#FBBF24"
    else:
        return "#FF6B6B"


def render():
    """Main render function for the Nutrition Audit tab."""
    st.markdown(
        """
        <div style="margin-bottom:1rem;">
            <h2 style="font-family:'Outfit',sans-serif; font-weight:700; margin-bottom:0.2rem;">
                🍽️ Food Recognition & Nutrition Audit
            </h2>
            <p style="color:#94A3B8; font-size:0.95rem;">
                Upload a meal photo and let AI identify the dish, estimate nutrients, and generate health insights.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded = st.file_uploader(
        "Upload a meal or dish photo",
        type=["jpg", "jpeg", "png", "webp"],
        key="nutrition_uploader",
        help="Supported formats: JPG, PNG, WebP",
    )

    col_upload, col_action = st.columns([3, 1])

    with col_action:
        use_demo = st.button("🎮 Try Demo", key="demo_nutrition", use_container_width=True)

    # Determine which data to show
    data = None
    image_to_show = None

    if uploaded is not None:
        image = Image.open(uploaded)
        image_to_show = image

        with st.spinner("🔬 Analyzing your meal with AI..."):
            if st.session_state.get("api_configured"):
                raw = generate_with_image(NUTRITION_AUDIT_PROMPT, image)
                data = parse_json_response(raw)
                if not data:
                    st.warning("Could not parse AI response. Showing demo data instead.")
                    data = DEMO_NUTRITION
            else:
                st.info("💡 No API key configured — showing demonstration results.")
                data = DEMO_NUTRITION

    elif use_demo:
        data = DEMO_NUTRITION

    if data:
        _render_results(data, image_to_show)


def _render_results(data: dict, image=None):
    """Render the full nutrition analysis results."""

    # ── Header Row ──
    col_img, col_info = st.columns([1, 2])

    with col_img:
        if image:
            st.image(image, use_container_width=True, caption="Uploaded Meal")
        else:
            st.markdown(
                """
                <div style="background:linear-gradient(135deg, rgba(255,107,107,0.1), rgba(78,205,196,0.1));
                border-radius:14px; padding:3rem; text-align:center; border:1px solid rgba(255,255,255,0.08);">
                    <span style="font-size:3rem;">🍽️</span>
                    <p style="color:#94A3B8; margin-top:0.5rem;">Demo Mode</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with col_info:
        raw_badges = data.get('health_badges', [])
        health_badges = [raw_badges] if isinstance(raw_badges, str) else (raw_badges if isinstance(raw_badges, list) else [])

        st.markdown(
            f"""
            <div class="glass-card">
                <h3 style="font-family:'Outfit',sans-serif; font-weight:700; margin:0;">
                    {data.get('dish_name', 'Unknown Dish')}
                </h3>
                <p style="color:#94A3B8; margin:0.3rem 0 0.8rem;">
                    🌍 {data.get('cuisine', 'N/A')} &nbsp;·&nbsp; 📏 {data.get('portion_size', 'N/A')}
                </p>
                <div>
                    {''.join(f'<span class="badge badge-green">{b}</span>' for b in health_badges)}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Allergen warnings
        raw_allergens = data.get("allergens", [])
        allergens = [raw_allergens] if isinstance(raw_allergens, str) else (raw_allergens if isinstance(raw_allergens, list) else [])
        if allergens:
            st.markdown(
                f"""
                <div style="background:rgba(255,107,107,0.08); border:1px solid rgba(255,107,107,0.2);
                border-radius:10px; padding:0.7rem 1rem; margin-top:0.5rem;">
                    <span style="font-weight:600; color:#FF6B6B;">⚠️ Allergens:</span>
                    <span style="color:#FAFAFA;"> {', '.join(allergens)}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Metrics Row ──
    c1, c2, c3, c4, c5 = st.columns(5)
    metrics = [
        (c1, "🔥", str(data.get("calories", 0)), "Calories"),
        (c2, "🥩", f"{data.get('protein_g', 0)}g", "Protein"),
        (c3, "🍞", f"{data.get('carbs_g', 0)}g", "Carbs"),
        (c4, "🧈", f"{data.get('fats_g', 0)}g", "Fats"),
        (c5, "🌾", f"{data.get('fiber_g', 0)}g", "Fiber"),
    ]
    for col, icon, value, label in metrics:
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div style="font-size:1.5rem; margin-bottom:0.3rem;">{icon}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts & Details Row ──
    col_chart, col_score, col_ingredients = st.columns([1.2, 0.8, 1])

    with col_chart:
        st.markdown("##### 📊 Macro Breakdown")
        fig = _render_macro_chart(data)
        st.plotly_chart(fig, use_container_width=True)

    with col_score:
        score = data.get("health_score", 0)
        color = _get_score_color(score)
        st.markdown(
            f"""
            <div style="text-align:center; padding-top:1rem;">
                <div class="score-ring" style="background: conic-gradient({color} {score * 3.6}deg, rgba(255,255,255,0.05) 0deg);">
                    <div class="score-ring-inner">
                        <div class="score-value" style="color:{color};">{score}</div>
                        <div class="score-label">Health Score</div>
                    </div>
                </div>
                <p style="color:#94A3B8; font-size:0.85rem; margin-top:0.5rem;">
                    {"Excellent" if score >= 80 else "Good" if score >= 60 else "Needs Improvement"}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_ingredients:
        st.markdown("##### 🧾 Detected Ingredients")
        for ingredient in data.get("ingredients", []):
            st.markdown(
                f"""<div style="padding:0.3rem 0; color:#FAFAFA; font-size:0.9rem;">
                    <span style="color:#4ECDC4; margin-right:0.5rem;">●</span> {ingredient}
                </div>""",
                unsafe_allow_html=True,
            )

    # ── Notes ──
    notes = data.get("notes", "")
    if notes:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="glass-card" style="border-left:4px solid #4ECDC4;">
                <span style="font-weight:600; color:#4ECDC4;">💡 Nutritionist's Note</span>
                <p style="color:#FAFAFA; margin-top:0.5rem; font-size:0.95rem;">{notes}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
