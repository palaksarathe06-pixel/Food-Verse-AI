"""
utils/styles.py
All custom CSS injected into the Streamlit app for premium dark-mode styling,
glassmorphism cards, animated gradients, and micro-interactions.
"""


def get_custom_css() -> str:
    """Return the full custom CSS string for the app."""
    return """
<style>
    /* ── Google Font Import ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Outfit:wght@300;400;500;600;700;800&display=swap');

    /* ── Root Variables ── */
    :root {
        --bg-primary: #0E1117;
        --bg-secondary: #1A1F2E;
        --bg-card: rgba(26, 31, 46, 0.7);
        --accent-coral: #FF6B6B;
        --accent-orange: #FF8E53;
        --accent-green: #00D2A0;
        --accent-blue: #4ECDC4;
        --accent-purple: #A855F7;
        --accent-yellow: #FBBF24;
        --text-primary: #FAFAFA;
        --text-secondary: #94A3B8;
        --text-muted: #64748B;
        --border-glass: rgba(255, 255, 255, 0.08);
        --shadow-glow: 0 0 40px rgba(255, 107, 107, 0.15);
        --gradient-main: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 50%, #FBBF24 100%);
        --gradient-cool: linear-gradient(135deg, #4ECDC4 0%, #A855F7 100%);
        --gradient-fresh: linear-gradient(135deg, #00D2A0 0%, #4ECDC4 100%);
    }

    /* ── Global Overrides ── */
    .stApp {
        font-family: 'Inter', sans-serif;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        letter-spacing: -0.02em;
    }

    /* ── Hero Header ── */
    .hero-header {
        background: linear-gradient(135deg, rgba(255,107,107,0.12) 0%, rgba(255,142,83,0.08) 50%, rgba(78,205,196,0.1) 100%);
        border: 1px solid var(--border-glass);
        border-radius: 20px;
        padding: 2.5rem 2rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(20px);
        position: relative;
        overflow: hidden;
    }
    .hero-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(from 0deg, transparent, rgba(255,107,107,0.05), transparent 30%);
        animation: hero-rotate 15s linear infinite;
    }
    @keyframes hero-rotate {
        100% { transform: rotate(360deg); }
    }
    .hero-header h1 {
        font-size: 2.4rem;
        font-weight: 800;
        background: var(--gradient-main);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.3rem;
        position: relative;
    }
    .hero-header p {
        color: var(--text-secondary);
        font-size: 1.05rem;
        position: relative;
    }

    /* ── Glass Card ── */
    .glass-card {
        background: var(--bg-card);
        border: 1px solid var(--border-glass);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(12px);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }
    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-glow);
    }

    /* ── Metric Cards ── */
    .metric-card {
        background: var(--bg-card);
        border: 1px solid var(--border-glass);
        border-radius: 14px;
        padding: 1.2rem 1rem;
        text-align: center;
        backdrop-filter: blur(12px);
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        border-color: var(--accent-coral);
        box-shadow: 0 0 20px rgba(255,107,107,0.1);
    }
    .metric-value {
        font-family: 'Outfit', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        background: var(--gradient-main);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .metric-label {
        color: var(--text-secondary);
        font-size: 0.85rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-top: 0.3rem;
    }

    /* ── Health Score Ring ── */
    .score-ring {
        width: 140px;
        height: 140px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1rem;
        position: relative;
    }
    .score-ring-inner {
        width: 110px;
        height: 110px;
        border-radius: 50%;
        background: var(--bg-primary);
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
    }
    .score-value {
        font-family: 'Outfit', sans-serif;
        font-size: 2.2rem;
        font-weight: 800;
    }
    .score-label {
        font-size: 0.7rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    /* ── Badge / Tag ── */
    .badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
        margin: 0.2rem 0.3rem 0.2rem 0;
        letter-spacing: 0.02em;
    }
    .badge-green {
        background: rgba(0,210,160,0.15);
        color: #00D2A0;
        border: 1px solid rgba(0,210,160,0.3);
    }
    .badge-coral {
        background: rgba(255,107,107,0.15);
        color: #FF6B6B;
        border: 1px solid rgba(255,107,107,0.3);
    }
    .badge-blue {
        background: rgba(78,205,196,0.15);
        color: #4ECDC4;
        border: 1px solid rgba(78,205,196,0.3);
    }
    .badge-purple {
        background: rgba(168,85,247,0.15);
        color: #A855F7;
        border: 1px solid rgba(168,85,247,0.3);
    }
    .badge-yellow {
        background: rgba(251,191,36,0.15);
        color: #FBBF24;
        border: 1px solid rgba(251,191,36,0.3);
    }
    .badge-orange {
        background: rgba(255,142,83,0.15);
        color: #FF8E53;
        border: 1px solid rgba(255,142,83,0.3);
    }

    /* ── Freshness Stages ── */
    .freshness-fresh {
        background: linear-gradient(135deg, rgba(0,210,160,0.15), rgba(78,205,196,0.1));
        border-left: 4px solid #00D2A0;
        border-radius: 12px;
        padding: 1.2rem;
    }
    .freshness-moderate {
        background: linear-gradient(135deg, rgba(251,191,36,0.15), rgba(255,142,83,0.1));
        border-left: 4px solid #FBBF24;
        border-radius: 12px;
        padding: 1.2rem;
    }
    .freshness-spoiled {
        background: linear-gradient(135deg, rgba(255,107,107,0.15), rgba(239,68,68,0.1));
        border-left: 4px solid #FF6B6B;
        border-radius: 12px;
        padding: 1.2rem;
    }

    /* ── Violation Card ── */
    .violation-card {
        background: var(--bg-card);
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 0.8rem;
        border-left: 4px solid;
        transition: all 0.2s ease;
    }
    .violation-card:hover {
        transform: translateX(4px);
    }
    .violation-high { border-left-color: #FF6B6B; }
    .violation-medium { border-left-color: #FBBF24; }
    .violation-low { border-left-color: #4ECDC4; }

    /* ── Recipe Card ── */
    .recipe-card {
        background: linear-gradient(145deg, rgba(26,31,46,0.9), rgba(26,31,46,0.6));
        border: 1px solid var(--border-glass);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    .recipe-card:hover {
        border-color: rgba(255,142,83,0.4);
        box-shadow: 0 8px 32px rgba(255,142,83,0.1);
    }
    .recipe-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }

    /* ── Meal Planner Day Card ── */
    .day-card {
        background: var(--bg-card);
        border: 1px solid var(--border-glass);
        border-radius: 14px;
        padding: 1.2rem;
        margin-bottom: 0.6rem;
        transition: all 0.2s ease;
    }
    .day-card:hover {
        border-color: rgba(168,85,247,0.4);
    }
    .day-name {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 1.1rem;
        background: var(--gradient-cool);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .meal-type {
        font-weight: 600;
        color: var(--accent-coral);
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .meal-name {
        color: var(--text-primary);
        font-size: 0.95rem;
    }
    .meal-macros {
        color: var(--text-muted);
        font-size: 0.8rem;
    }

    /* ── Step/Instruction list ── */
    .step-item {
        display: flex;
        align-items: flex-start;
        gap: 0.8rem;
        padding: 0.6rem 0;
    }
    .step-number {
        min-width: 28px;
        height: 28px;
        border-radius: 50%;
        background: var(--gradient-main);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.8rem;
        color: white;
        flex-shrink: 0;
    }
    .step-text {
        color: var(--text-primary);
        font-size: 0.95rem;
        line-height: 1.5;
    }

    /* ── Sidebar Styling ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0E1117 0%, #151B28 100%);
        border-right: 1px solid var(--border-glass);
    }

    /* ── Tab Styling ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: var(--bg-secondary);
        border-radius: 14px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 0.6rem 1rem;
        font-weight: 500;
        font-size: 0.9rem;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(255,107,107,0.2), rgba(255,142,83,0.15));
        border: 1px solid rgba(255,107,107,0.3);
    }

    /* ── Animated Pulse for Live Indicators ── */
    @keyframes pulse-green {
        0%, 100% { box-shadow: 0 0 0 0 rgba(0,210,160,0.4); }
        50% { box-shadow: 0 0 0 8px rgba(0,210,160,0); }
    }
    .live-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #00D2A0;
        display: inline-block;
        animation: pulse-green 2s infinite;
        margin-right: 6px;
    }

    /* ── Grocery Category ── */
    .grocery-category {
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        padding: 0.4rem 0;
        border-bottom: 2px solid;
        margin-bottom: 0.5rem;
    }
    .grocery-item {
        color: var(--text-secondary);
        padding: 0.15rem 0;
        font-size: 0.9rem;
    }

    /* ── Buttons ── */
    .stButton > button {
        border-radius: 12px;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        letter-spacing: 0.02em;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 20px rgba(255,107,107,0.3);
    }

    /* ── Progress bar override ── */
    .stProgress > div > div > div {
        background: var(--gradient-main);
    }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-primary); }
    ::-webkit-scrollbar-thumb { background: var(--text-muted); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--text-secondary); }

    /* ── Footer ── */
    .app-footer {
        text-align: center;
        padding: 2rem 0 1rem;
        color: var(--text-muted);
        font-size: 0.8rem;
        border-top: 1px solid var(--border-glass);
        margin-top: 3rem;
    }
</style>
"""
