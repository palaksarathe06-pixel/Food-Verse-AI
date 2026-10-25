"""
🍽️ Food Verse AI — Multimodal Food Intelligence Agent
=====================================================
A production-ready Streamlit application for the Skill Wallet Capstone Project 3.
Analyzes food images, estimates nutrients, detects freshness/spoilage,
monitors kitchen hygiene, generates recipes, and creates personalized meal plans.

Author: Food Verse AI Team
Platform ID: 6ac4ca021dcde6d7857c169a
"""

import streamlit as st

# ── Page Configuration (must be first Streamlit call) ──
st.set_page_config(
    page_title="Food Verse AI — Multimodal Food Intelligence",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": (
            "## 🍽️ Food Verse AI\n"
            "Multimodal Food Intelligence Agent — Skill Wallet Capstone Project 3\n\n"
            "Powered by Google Gemini 1.5 Flash"
        ),
    },
)

# ── Imports ──
from utils.styles import get_custom_css
from utils.gemini_client import configure_gemini, DEFAULT_API_KEY, get_active_model_name
from tabs import tab_nutrition, tab_freshness, tab_hygiene, tab_recipe, tab_meal_planner

# ── Inject Custom CSS ──
st.markdown(get_custom_css(), unsafe_allow_html=True)

# ── Session State Defaults & Auto-configuration ──
if "api_configured" not in st.session_state:
    # Auto-initialize with integrated user API key
    if configure_gemini(DEFAULT_API_KEY):
        st.session_state.api_configured = True
        st.session_state.api_key = DEFAULT_API_KEY
    else:
        st.session_state.api_configured = False
        st.session_state.api_key = ""


# ═══════════════════════════════════════════════════
#  SIDEBAR — Configuration & Persona
# ═══════════════════════════════════════════════════

with st.sidebar:
    st.markdown(
        """
        <div style="text-align:center; padding:1.5rem 0 1rem;">
            <span style="font-size:2.8rem;">🍽️</span>
            <h2 style="font-family:'Outfit',sans-serif; font-weight:800; margin:0.3rem 0 0;
            background: linear-gradient(135deg, #FF6B6B, #FF8E53, #FBBF24);
            -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;">
                Food Verse AI
            </h2>
            <p style="color:#64748B; font-size:0.8rem; margin-top:0.2rem;">
                Multimodal Food Intelligence Agent
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ── AI Engine Status ──
    st.markdown(
        """
        <div style="margin-bottom:0.5rem;">
            <span style="font-weight:600; color:#FAFAFA; font-size:0.9rem;">⚡ AI Engine Status</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.api_configured:
        model_display = get_active_model_name()
        st.markdown(
            f"""
            <div style="background:rgba(0,210,160,0.08); border:1px solid rgba(0,210,160,0.25);
            border-radius:10px; padding:0.7rem; text-align:center;">
                <span class="live-dot"></span>
                <span style="color:#00D2A0; font-weight:600; font-size:0.85rem;">Online · Multimodal AI</span>
                <br><span style="color:#94A3B8; font-size:0.75rem;">Model: {model_display}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div style="background:rgba(251,191,36,0.08); border:1px solid rgba(251,191,36,0.2);
            border-radius:10px; padding:0.7rem; text-align:center;">
                <span style="color:#FBBF24; font-size:0.85rem; font-weight:500;">
                    🎮 Demo Mode Active
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ── Navigation Info ──
    st.markdown(
        """
        <div style="margin-bottom:0.5rem;">
            <span style="font-weight:600; color:#FAFAFA; font-size:0.9rem;">📚 Intelligence Pillars</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    pillars = [
        ("🍽️", "Nutrition Audit", "Identify dishes & estimate nutrients"),
        ("🥬", "Freshness Diagnostic", "Detect spoilage & freshness stage"),
        ("🏪", "Kitchen Hygiene", "Audit food safety compliance"),
        ("👨‍🍳", "Recipe Assistant", "Generate recipes from pantry"),
        ("📅", "Meal Planner", "Personalized 7-day meal plans"),
    ]

    for icon, title, desc in pillars:
        st.markdown(
            f"""
            <div style="padding:0.4rem 0;">
                <span style="font-size:1rem;">{icon}</span>
                <span style="color:#FAFAFA; font-weight:500; font-size:0.85rem;"> {title}</span>
                <br><span style="color:#64748B; font-size:0.75rem; padding-left:1.5rem;">{desc}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ── Tech Stack Info ──
    st.markdown(
        """
        <div style="text-align:center; padding:0.5rem 0;">
            <span style="color:#64748B; font-size:0.7rem;">
                Powered by<br>
                <span style="color:#94A3B8; font-weight:600;">Streamlit · Gemini 1.5 · Plotly · Pillow</span>
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════
#  MAIN CONTENT
# ═══════════════════════════════════════════════════

# ── Hero Header ──
st.markdown(
    """
    <div class="hero-header">
        <h1>🍽️ Food Verse AI</h1>
        <p>
            Multimodal Food Intelligence Agent — Analyze meals, detect freshness,
            audit kitchens, generate recipes, and plan personalized meals with AI.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Tab Navigation ──
tab_labels = [
    "🍽️ Nutrition Audit",
    "🥬 Freshness Diagnostic",
    "🏪 Kitchen Hygiene",
    "👨‍🍳 Recipe Assistant",
    "📅 Meal Planner",
]

tabs = st.tabs(tab_labels)

with tabs[0]:
    tab_nutrition.render()

with tabs[1]:
    tab_freshness.render()

with tabs[2]:
    tab_hygiene.render()

with tabs[3]:
    tab_recipe.render()

with tabs[4]:
    tab_meal_planner.render()

# ── Footer ──
st.markdown(
    """
    <div class="app-footer">
        🍽️ <strong>Food Verse AI</strong> — Multimodal Food Intelligence Agent<br>
        Skill Wallet Capstone Project 3 · Platform ID: 6ac4ca021dcde6d7857c169a<br>
        Built with ❤️ using Streamlit & Google Gemini 1.5
    </div>
    """,
    unsafe_allow_html=True,
)
