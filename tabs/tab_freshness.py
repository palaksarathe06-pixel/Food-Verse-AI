"""
tabs/tab_freshness.py
Tab 2 – Food Freshness & Spoilage Diagnostic (Epic 3)
Upload a photo of a perishable food item → Gemini Vision evaluates surface
texture, discoloration, wrinkling, and mold to classify freshness stage.
"""

import streamlit as st
from PIL import Image
import plotly.graph_objects as go

from utils.gemini_client import generate_with_image, parse_json_response
from utils.prompts import FRESHNESS_PROMPT
from utils.demo_data import DEMO_FRESHNESS


def _freshness_to_css_class(stage: str) -> str:
    stage_lower = stage.lower()
    if "spoiled" in stage_lower:
        return "freshness-spoiled"
    elif "moderate" in stage_lower:
        return "freshness-moderate"
    return "freshness-fresh"


def _freshness_to_emoji(stage: str) -> str:
    stage_lower = stage.lower()
    if "spoiled" in stage_lower:
        return "🔴"
    elif "moderate" in stage_lower:
        return "🟡"
    return "🟢"


def _safety_badge_style(advice: str) -> tuple:
    advice_lower = advice.lower()
    if "discard" in advice_lower:
        return "badge-coral", "🚫"
    elif "24h" in advice_lower or "consume within" in advice_lower:
        return "badge-yellow", "⏰"
    return "badge-green", "✅"


def _render_confidence_gauge(confidence: float):
    """Render a horizontal gauge for confidence level."""
    pct = int(confidence * 100)
    if pct >= 80:
        color = "#00D2A0"
    elif pct >= 60:
        color = "#FBBF24"
    else:
        color = "#FF6B6B"

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=pct,
            number=dict(suffix="%", font=dict(size=32, color="#FAFAFA", family="Outfit")),
            gauge=dict(
                axis=dict(range=[0, 100], tickfont=dict(color="#64748B"), dtick=25),
                bar=dict(color=color, thickness=0.7),
                bgcolor="rgba(255,255,255,0.05)",
                borderwidth=0,
                steps=[
                    dict(range=[0, 40], color="rgba(255,107,107,0.1)"),
                    dict(range=[40, 70], color="rgba(251,191,36,0.1)"),
                    dict(range=[70, 100], color="rgba(0,210,160,0.1)"),
                ],
            ),
            title=dict(text="Detection Confidence", font=dict(size=14, color="#94A3B8", family="Inter")),
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=200,
        margin=dict(t=40, b=10, l=30, r=30),
    )
    return fig


def render():
    """Main render function for the Freshness Diagnostic tab."""
    st.markdown(
        """
        <div style="margin-bottom:1rem;">
            <h2 style="font-family:'Outfit',sans-serif; font-weight:700; margin-bottom:0.2rem;">
                🥬 Food Freshness & Spoilage Diagnostic
            </h2>
            <p style="color:#94A3B8; font-size:0.95rem;">
                Upload a photo of a perishable item — AI will evaluate freshness, identify spoilage signs, and recommend action.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Category selector
    category = st.selectbox(
        "Food Category",
        ["Fruits", "Vegetables", "Meats", "Dairy", "Seafood", "Bakery"],
        key="freshness_category",
    )

    uploaded = st.file_uploader(
        "Upload a perishable food item photo",
        type=["jpg", "jpeg", "png", "webp"],
        key="freshness_uploader",
    )

    col_upload, col_action = st.columns([3, 1])
    with col_action:
        use_demo = st.button("🎮 Try Demo", key="demo_freshness", use_container_width=True)

    data = None
    image_to_show = None

    if uploaded is not None:
        image = Image.open(uploaded)
        image_to_show = image

        with st.spinner("🔍 Analyzing freshness indicators..."):
            if st.session_state.get("api_configured"):
                raw = generate_with_image(FRESHNESS_PROMPT, image)
                data = parse_json_response(raw)
                if not data:
                    st.warning("Could not parse AI response. Showing demo data.")
                    data = DEMO_FRESHNESS
            else:
                st.info("💡 No API key — showing demonstration results.")
                data = DEMO_FRESHNESS

    elif use_demo:
        data = DEMO_FRESHNESS

    if data:
        _render_results(data, image_to_show)


def _render_results(data: dict, image=None):
    """Render freshness analysis results."""
    stage = data.get("freshness_stage", "Unknown")
    css_class = _freshness_to_css_class(stage)
    emoji = _freshness_to_emoji(stage)
    safety = data.get("safety_advice", "N/A")
    badge_class, safety_icon = _safety_badge_style(safety)

    # ── Header Row ──
    col_img, col_result = st.columns([1, 2])

    with col_img:
        if image:
            st.image(image, use_container_width=True, caption="Uploaded Item")
        else:
            st.markdown(
                """
                <div style="background:linear-gradient(135deg, rgba(0,210,160,0.1), rgba(78,205,196,0.1));
                border-radius:14px; padding:3rem; text-align:center; border:1px solid rgba(255,255,255,0.08);">
                    <span style="font-size:3rem;">🥬</span>
                    <p style="color:#94A3B8; margin-top:0.5rem;">Demo Mode</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with col_result:
        st.markdown(
            f"""
            <div class="{css_class}">
                <div style="display:flex; align-items:center; gap:0.8rem; margin-bottom:0.8rem;">
                    <span style="font-size:2rem;">{emoji}</span>
                    <div>
                        <h3 style="font-family:'Outfit',sans-serif; margin:0; font-weight:700;">
                            {data.get('item_name', 'Unknown Item')}
                        </h3>
                        <span class="badge badge-blue">{data.get('category', 'N/A')}</span>
                    </div>
                </div>
                <div style="display:flex; gap:1rem; flex-wrap:wrap; align-items:center;">
                    <div>
                        <span style="color:#94A3B8; font-size:0.8rem; text-transform:uppercase; letter-spacing:0.08em;">
                            Freshness Stage
                        </span><br>
                        <span style="font-family:'Outfit',sans-serif; font-size:1.4rem; font-weight:700; color:#FAFAFA;">
                            {stage}
                        </span>
                    </div>
                    <div>
                        <span style="color:#94A3B8; font-size:0.8rem; text-transform:uppercase; letter-spacing:0.08em;">
                            Safety Advice
                        </span><br>
                        <span class="badge {badge_class}" style="font-size:0.9rem;">
                            {safety_icon} {safety}
                        </span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Confidence & Indicators ──
    col_gauge, col_indicators = st.columns([1, 1.5])

    with col_gauge:
        confidence = data.get("confidence", 0.0)
        fig = _render_confidence_gauge(confidence)
        st.plotly_chart(fig, use_container_width=True)

    with col_indicators:
        st.markdown("##### 🔎 Visual Indicators Detected")
        raw_ind = data.get("visual_indicators", [])
        indicators = [raw_ind] if isinstance(raw_ind, str) else (raw_ind if isinstance(raw_ind, list) else [])
        for indicator in indicators:
            st.markdown(
                f"""
                <div style="padding:0.35rem 0; color:#FAFAFA; font-size:0.9rem;">
                    <span style="color:#FBBF24; margin-right:0.5rem;">▸</span> {indicator}
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Recommendation ──
    recommendation = data.get("detailed_recommendation", "")
    if recommendation:
        st.markdown(
            f"""
            <div class="glass-card" style="border-left:4px solid #FBBF24;">
                <span style="font-weight:600; color:#FBBF24;">📋 Detailed Recommendation</span>
                <p style="color:#FAFAFA; margin-top:0.5rem; font-size:0.95rem; line-height:1.6;">
                    {recommendation}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Storage Tips ──
    raw_tips = data.get("storage_tips", [])
    tips = [raw_tips] if isinstance(raw_tips, str) else (raw_tips if isinstance(raw_tips, list) else [])
    if tips:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("##### 📦 Proper Storage & Preservation Tips")
        for i, tip in enumerate(tips, 1):
            st.markdown(
                f"""
                <div class="step-item">
                    <div class="step-number">{i}</div>
                    <div class="step-text">{tip}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
