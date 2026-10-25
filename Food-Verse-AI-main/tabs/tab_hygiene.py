"""
tabs/tab_hygiene.py
Tab 3 – Kitchen Hygiene & Food Safety Compliance (Epic 4)
Upload a kitchen environment photo → Gemini Vision evaluates hygiene indicators
and generates a compliance score with itemized violations.
"""

import streamlit as st
from PIL import Image
import plotly.graph_objects as go

from utils.gemini_client import generate_with_image, generate_with_video, parse_json_response
from utils.prompts import HYGIENE_PROMPT
from utils.demo_data import DEMO_HYGIENE


def _severity_color(severity: str) -> str:
    s = severity.lower()
    if s == "high":
        return "#FF6B6B"
    elif s == "medium":
        return "#FBBF24"
    return "#4ECDC4"


def _severity_css(severity: str) -> str:
    s = severity.lower()
    if s == "high":
        return "violation-high"
    elif s == "medium":
        return "violation-medium"
    return "violation-low"


def _render_compliance_gauge(score: int):
    """Render a large compliance score gauge."""
    if score >= 80:
        color = "#00D2A0"
        grade = "A – Excellent"
    elif score >= 60:
        color = "#FBBF24"
        grade = "B – Acceptable"
    elif score >= 40:
        color = "#FF8E53"
        grade = "C – Needs Improvement"
    else:
        color = "#FF6B6B"
        grade = "D – Critical"

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number=dict(suffix="/100", font=dict(size=40, color="#FAFAFA", family="Outfit")),
            gauge=dict(
                axis=dict(range=[0, 100], tickfont=dict(color="#64748B", size=11), dtick=20),
                bar=dict(color=color, thickness=0.65),
                bgcolor="rgba(255,255,255,0.05)",
                borderwidth=0,
                steps=[
                    dict(range=[0, 40], color="rgba(255,107,107,0.08)"),
                    dict(range=[40, 60], color="rgba(255,142,83,0.08)"),
                    dict(range=[60, 80], color="rgba(251,191,36,0.08)"),
                    dict(range=[80, 100], color="rgba(0,210,160,0.08)"),
                ],
                threshold=dict(
                    line=dict(color="#FAFAFA", width=2),
                    thickness=0.8,
                    value=score,
                ),
            ),
            title=dict(
                text=f"Kitchen Hygiene Score<br><span style='font-size:14px; color:{color}'>{grade}</span>",
                font=dict(size=16, color="#94A3B8", family="Inter"),
            ),
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=280,
        margin=dict(t=60, b=10, l=40, r=40),
    )
    return fig


def render():
    """Main render function for the Kitchen Hygiene tab."""
    st.markdown(
        """
        <div style="margin-bottom:1rem;">
            <h2 style="font-family:'Outfit',sans-serif; font-weight:700; margin-bottom:0.2rem;">
                🏪 Kitchen Hygiene & Food Safety Compliance
            </h2>
            <p style="color:#94A3B8; font-size:0.95rem;">
                Upload a photo or surveillance video clip of a kitchen — AI audits hygiene practices (gloves, hairnets, cross-contamination, sanitation) and generates a compliance report.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded = st.file_uploader(
        "Upload a kitchen photo or video clip (MP4, MOV, JPG, PNG)",
        type=["jpg", "jpeg", "png", "webp", "mp4", "mov", "avi"],
        key="hygiene_uploader",
    )

    col_upload, col_action = st.columns([3, 1])
    with col_action:
        use_demo = st.button("🎮 Try Demo", key="demo_hygiene", use_container_width=True)

    data = None
    image_to_show = None
    video_to_show = None

    if uploaded is not None:
        file_ext = uploaded.name.split(".")[-1].lower()
        is_video = file_ext in ["mp4", "mov", "avi"]

        if is_video:
            video_bytes = uploaded.getvalue()
            video_to_show = video_bytes
            with st.spinner("📹 Extracting video frames & auditing kitchen hygiene with AI..."):
                if st.session_state.get("api_configured"):
                    raw = generate_with_video(HYGIENE_PROMPT, video_bytes)
                    data = parse_json_response(raw)
                    if not data or not isinstance(data, dict):
                        st.warning("Could not parse AI response. Showing demonstration audit.")
                        data = DEMO_HYGIENE
                else:
                    st.info("💡 No API key — showing demonstration results.")
                    data = DEMO_HYGIENE
        else:
            image = Image.open(uploaded)
            image_to_show = image

            with st.spinner("🧹 Auditing kitchen hygiene compliance with AI..."):
                if st.session_state.get("api_configured"):
                    raw = generate_with_image(HYGIENE_PROMPT, image)
                    data = parse_json_response(raw)
                    if not data or not isinstance(data, dict):
                        st.warning("Could not parse AI response. Showing demonstration audit.")
                        data = DEMO_HYGIENE
                else:
                    st.info("💡 No API key — showing demonstration results.")
                    data = DEMO_HYGIENE

    elif use_demo:
        data = DEMO_HYGIENE

    if data:
        _render_results(data, image=image_to_show, video_bytes=video_to_show)


def _render_results(data: dict, image=None, video_bytes=None):
    """Render hygiene compliance results."""
    score = data.get("overall_score", 0)
    violations = data.get("violations", [])
    positives = data.get("positive_observations", [])

    # ── Score & Summary ──
    col_gauge, col_summary = st.columns([1, 1.5])

    with col_gauge:
        fig = _render_compliance_gauge(score)
        st.plotly_chart(fig, use_container_width=True)

    with col_summary:
        if video_bytes:
            st.video(video_bytes)
        elif image:
            st.image(image, use_container_width=True, caption="Kitchen Under Review")
        st.markdown(
            f"""
            <div class="glass-card">
                <span style="font-weight:600; color:#94A3B8; font-size:0.8rem; text-transform:uppercase; letter-spacing:0.08em;">
                    Summary
                </span>
                <p style="color:#FAFAFA; margin-top:0.4rem; font-size:0.95rem; line-height:1.5;">
                    {data.get('summary', 'N/A')}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Violations ──
    if violations:
        # Count by severity
        high = sum(1 for v in violations if v.get("severity", "").lower() == "high")
        medium = sum(1 for v in violations if v.get("severity", "").lower() == "medium")
        low = sum(1 for v in violations if v.get("severity", "").lower() == "low")

        st.markdown(
            f"""
            <div style="display:flex; gap:1rem; margin-bottom:1rem; flex-wrap:wrap;">
                <span class="badge badge-coral">🔴 {high} High</span>
                <span class="badge badge-yellow">🟡 {medium} Medium</span>
                <span class="badge badge-blue">🟢 {low} Low</span>
                <span class="badge badge-purple">📋 {len(violations)} Total Violations</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("##### 🚨 Violation Details")
        for v in violations:
            severity = v.get("severity", "Low")
            css = _severity_css(severity)
            color = _severity_color(severity)

            st.markdown(
                f"""
                <div class="violation-card {css}">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
                        <span style="font-weight:600; color:#FAFAFA; font-size:1rem;">
                            {v.get('category', 'N/A')}
                        </span>
                        <span class="badge" style="background:rgba({','.join(str(int(color.lstrip('#')[i:i+2], 16)) for i in (0,2,4))},0.15);
                        color:{color}; border:1px solid rgba({','.join(str(int(color.lstrip('#')[i:i+2], 16)) for i in (0,2,4))},0.3);">
                            {severity}
                        </span>
                    </div>
                    <p style="color:#94A3B8; margin:0 0 0.5rem; font-size:0.9rem;">
                        {v.get('description', '')}
                    </p>
                    <div style="background:rgba(78,205,196,0.08); border-radius:8px; padding:0.6rem; margin-top:0.3rem;">
                        <span style="font-weight:500; color:#4ECDC4; font-size:0.8rem;">💡 Recommendation:</span>
                        <span style="color:#FAFAFA; font-size:0.85rem;"> {v.get('recommendation', '')}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── Positive Observations ──
    if positives:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("##### ✅ Positive Observations")
        for p in positives:
            st.markdown(
                f"""
                <div style="padding:0.35rem 0; color:#FAFAFA; font-size:0.9rem;">
                    <span style="color:#00D2A0; margin-right:0.5rem;">✓</span> {p}
                </div>
                """,
                unsafe_allow_html=True,
            )
