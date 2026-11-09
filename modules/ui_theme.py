"""
SkillPath AI – Modern Bright Pastel Theme & Visual Components Module.
Provides custom CSS styling, Lottie animation loaders, hero banners,
colorful cards, and rich visual components.
"""
from typing import Dict, Any, Optional
import json
import os
from pathlib import Path
import streamlit as st

try:
    from streamlit_lottie import st_lottie
    HAS_LOTTIE = True
except ImportError:
    HAS_LOTTIE = False

# Path to local Lottie JSON assets
ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
LOTTIE_DIR = ASSETS_DIR / "lottie"


@st.cache_data(show_spinner=False)
def load_lottie_file(filename: str) -> Optional[Dict[str, Any]]:
    """
    Safely loads and caches a local Lottie JSON animation file.
    """
    filepath = LOTTIE_DIR / filename
    if not filepath.exists():
        return None
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def render_lottie(lottie_data: Optional[Dict[str, Any]], height: int = 180, key: Optional[str] = None):
    """
    Renders a Lottie animation cleanly. Falls back gracefully if unavailable.
    """
    if HAS_LOTTIE and lottie_data:
        st_lottie(
            lottie_data,
            speed=1,
            reverse=False,
            loop=True,
            quality="high",
            height=height,
            key=key
        )


def polish_fig(fig):
    """
    Polishes Plotly charts to match the pastel light theme:
    transparent background, modern typography, clean margins.
    """
    if fig:
        fig.update_layout(
            paper_bgcolor="rgba(255, 255, 255, 0)",
            plot_bgcolor="rgba(255, 255, 255, 0)",
            font=dict(family="Plus Jakarta Sans, sans-serif", color="#1E293B"),
            margin=dict(l=25, r=25, t=45, b=35)
        )
    return fig


def apply_custom_theme():
    """
    Injects custom CSS for a bright, colorful, catchy light theme with:
    - Pastel gradient background
    - Gradient headline
    - Rounded white cards with soft shadows
    - Gradient buttons
    - Colorful tabs, metric cards, and progress bars
    """
    st.markdown("""
    <style>
        /* Import clean modern Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Outfit:wght@500;600;700;800&display=swap');

        /* Root Bright & Pastel Palette */
        :root {
            --font-main: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            --font-display: 'Outfit', 'Plus Jakarta Sans', sans-serif;
            --primary-gradient: linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #EC4899 100%);
            --secondary-gradient: linear-gradient(135deg, #3B82F6 0%, #06B6D4 50%, #10B981 100%);
            --accent-warm: linear-gradient(135deg, #F59E0B 0%, #EF4444 100%);
            --bg-card: #FFFFFF;
            --border-soft: rgba(226, 232, 240, 0.85);
            --shadow-soft: 0 10px 25px -5px rgba(99, 102, 241, 0.08), 0 8px 10px -6px rgba(0, 0, 0, 0.02);
            --shadow-hover: 0 16px 32px -4px rgba(99, 102, 241, 0.14), 0 10px 12px -5px rgba(0, 0, 0, 0.04);
        }

        /* Top-level App Background: Dreamy Bright Pastel Gradient */
        .stApp {
            background: linear-gradient(135deg, #F8FAFC 0%, #EEF2FF 20%, #FDF2F8 45%, #F0FDF4 75%, #FFFBEB 100%) fixed !important;
            font-family: var(--font-main) !important;
            color: #1E293B !important;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 55%, #EFF6FF 100%) !important;
            border-right: 1px solid var(--border-soft) !important;
            box-shadow: 4px 0 20px rgba(99, 102, 241, 0.04) !important;
        }

        section[data-testid="stSidebar"] h1, 
        section[data-testid="stSidebar"] h2, 
        section[data-testid="stSidebar"] h3 {
            font-family: var(--font-display) !important;
            color: #1E293B !important;
        }

        /* Typography & Gradient Headlines */
        .gradient-headline {
            font-family: var(--font-display);
            font-size: 2.35rem;
            font-weight: 800;
            background: linear-gradient(135deg, #4338CA 0%, #6366F1 30%, #9333EA 60%, #EC4899 90%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
            line-height: 1.2;
            letter-spacing: -0.02em;
        }

        .section-headline {
            font-family: var(--font-display);
            font-size: 1.85rem;
            font-weight: 700;
            background: linear-gradient(135deg, #3730A3 0%, #6366F1 45%, #DB2777 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0 0 0.25rem 0;
            line-height: 1.25;
            letter-spacing: -0.01em;
        }

        .sub-headline {
            font-size: 1.02rem;
            color: #64748B;
            font-weight: 500;
            margin-bottom: 0.8rem;
            line-height: 1.5;
        }

        /* Hero Banner Card */
        .hero-banner-container {
            background: linear-gradient(135deg, #FFFFFF 0%, #F5F3FF 50%, #FDF2F8 100%);
            border-radius: 24px;
            padding: 1.75rem 2rem;
            margin-bottom: 1.5rem;
            border: 1px solid rgba(199, 210, 254, 0.6);
            box-shadow: 0 14px 34px -8px rgba(99, 102, 241, 0.12), 0 6px 12px -4px rgba(0, 0, 0, 0.03);
            position: relative;
            overflow: hidden;
        }

        .hero-banner-container::after {
            content: "";
            position: absolute;
            top: -60px;
            right: -60px;
            width: 180px;
            height: 180px;
            background: radial-gradient(circle, rgba(236, 72, 153, 0.15) 0%, rgba(99, 102, 241, 0) 70%);
            border-radius: 50%;
            pointer-events: none;
        }

        .hero-badge {
            display: inline-block;
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.12), rgba(236, 72, 153, 0.12));
            color: #4F46E5;
            font-weight: 700;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            padding: 4px 12px;
            border-radius: 20px;
            border: 1px solid rgba(99, 102, 241, 0.2);
            margin-bottom: 0.65rem;
        }

        .hero-chip-row {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 1rem;
        }

        .hero-chip {
            background: #FFFFFF;
            color: #475569;
            font-size: 0.82rem;
            font-weight: 600;
            padding: 4px 12px;
            border-radius: 12px;
            border: 1px solid #E2E8F0;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02);
            display: inline-flex;
            align-items: center;
            gap: 5px;
        }

        /* Section Banner Card */
        .section-banner-card {
            background: #FFFFFF;
            border-radius: 20px;
            padding: 1.4rem 1.75rem;
            margin-bottom: 1.5rem;
            border: 1px solid var(--border-soft);
            box-shadow: var(--shadow-soft);
        }

        /* Rounded White Cards with Soft Shadows */
        .white-card {
            background: #FFFFFF !important;
            border-radius: 18px !important;
            padding: 1.4rem 1.6rem !important;
            border: 1px solid var(--border-soft) !important;
            box-shadow: var(--shadow-soft) !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
            margin-bottom: 1.25rem !important;
        }

        .white-card:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-hover) !important;
        }

        /* Streamlit Native Metric Cards Styled as Rounded White Cards */
        div[data-testid="stMetric"] {
            background: #FFFFFF !important;
            border-radius: 18px !important;
            padding: 1.15rem 1.35rem !important;
            border: 1px solid var(--border-soft) !important;
            box-shadow: var(--shadow-soft) !important;
            position: relative !important;
            overflow: hidden !important;
            border-top: 4px solid #6366F1 !important;
            transition: all 0.25s ease !important;
        }

        div[data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-hover) !important;
        }

        div[data-testid="stMetric"] [data-testid="stMetricLabel"] {
            font-weight: 600 !important;
            color: #64748B !important;
            font-size: 0.88rem !important;
            letter-spacing: 0.01em;
        }

        div[data-testid="stMetric"] [data-testid="stMetricValue"] {
            font-family: var(--font-display) !important;
            color: #1E293B !important;
            font-weight: 800 !important;
            font-size: 1.95rem !important;
        }

        div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
            font-weight: 600 !important;
            font-size: 0.85rem !important;
        }

        /* Gradient Action Buttons */
        div.stButton > button, 
        div.stFormSubmitButton > button, 
        div.stLinkButton > a {
            background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #EC4899 100%) !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.55rem 1.35rem !important;
            box-shadow: 0 4px 14px 0 rgba(139, 92, 246, 0.35) !important;
            transition: all 0.22s ease-in-out !important;
            letter-spacing: 0.015em;
            text-decoration: none !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
        }

        div.stButton > button:hover, 
        div.stFormSubmitButton > button:hover, 
        div.stLinkButton > a:hover {
            background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #DB2777 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 22px 0 rgba(139, 92, 246, 0.5) !important;
            color: #FFFFFF !important;
        }

        div.stButton > button:active, 
        div.stFormSubmitButton > button:active, 
        div.stLinkButton > a:active {
            transform: translateY(0px) !important;
        }

        /* Streamlit Tabs: Bright, Colorful & Smooth */
        div[data-baseweb="tab-list"] {
            gap: 8px !important;
            background-color: transparent !important;
            border-bottom: 2px solid #E2E8F0 !important;
            padding-bottom: 2px !important;
            margin-bottom: 1.25rem !important;
        }

        button[data-baseweb="tab"] {
            font-family: var(--font-display) !important;
            font-weight: 700 !important;
            font-size: 0.98rem !important;
            border-radius: 12px 12px 0 0 !important;
            padding: 0.65rem 1.35rem !important;
            color: #64748B !important;
            background: transparent !important;
            border: none !important;
            transition: all 0.2s ease !important;
        }

        button[data-baseweb="tab"]:hover {
            color: #4F46E5 !important;
            background: rgba(99, 102, 241, 0.05) !important;
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            color: #4338CA !important;
            background: #FFFFFF !important;
            border-bottom: 3px solid #6366F1 !important;
            box-shadow: 0 -2px 10px rgba(99, 102, 241, 0.06) !important;
        }

        /* Streamlit Progress Bars */
        div[data-testid="stProgress"] > div > div > div > div {
            background: linear-gradient(90deg, #10B981 0%, #3B82F6 50%, #8B5CF6 100%) !important;
            border-radius: 10px !important;
        }

        div[data-testid="stProgress"] > div > div > div {
            background: #E2E8F0 !important;
            border-radius: 10px !important;
            height: 10px !important;
        }

        /* Course Recommendation Cards */
        .course-card {
            background: #FFFFFF;
            border-radius: 18px;
            padding: 1.5rem;
            margin-bottom: 1.25rem;
            border: 1px solid var(--border-soft);
            box-shadow: var(--shadow-soft);
            transition: all 0.25s ease;
            position: relative;
        }

        .course-card:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-hover);
            border-color: #C7D2FE;
        }

        .course-card-top {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 12px;
            margin-bottom: 0.6rem;
        }

        .course-title {
            font-family: var(--font-display);
            font-size: 1.25rem;
            font-weight: 700;
            color: #1E293B;
            margin: 0;
            line-height: 1.3;
        }

        .fit-badge {
            background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%);
            color: #4338CA;
            font-weight: 700;
            font-size: 0.85rem;
            padding: 4px 12px;
            border-radius: 20px;
            border: 1px solid #C7D2FE;
            white-space: nowrap;
        }

        .course-chips {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-bottom: 0.75rem;
        }

        .course-chip {
            background: #F8FAFC;
            color: #475569;
            font-size: 0.8rem;
            font-weight: 600;
            padding: 3px 10px;
            border-radius: 8px;
            border: 1px solid #E2E8F0;
        }

        .why-box {
            background: linear-gradient(135deg, #ECFDF5 0%, #F0FDF4 100%);
            border-left: 4px solid #10B981;
            padding: 0.75rem 1rem;
            border-radius: 6px 10px 10px 6px;
            color: #065F46;
            font-size: 0.9rem;
            margin: 0.75rem 0;
        }

        /* Colorful Roadmap Step Cards */
        .roadmap-card {
            background: #FFFFFF;
            border-radius: 18px;
            padding: 1.5rem;
            margin-bottom: 1.25rem;
            border: 1px solid var(--border-soft);
            box-shadow: var(--shadow-soft);
            transition: all 0.25s ease;
            position: relative;
        }

        .roadmap-card:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-hover);
        }

        .roadmap-card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 0.75rem;
        }

        .step-pill {
            color: #FFFFFF;
            font-weight: 800;
            font-size: 0.85rem;
            padding: 4px 14px;
            border-radius: 20px;
            box-shadow: 0 2px 8px rgba(99, 102, 241, 0.25);
        }

        .phase-pill {
            font-weight: 700;
            font-size: 0.82rem;
            padding: 4px 12px;
            border-radius: 20px;
        }

        .schedule-pill {
            background: #F8FAFC;
            color: #64748B;
            font-size: 0.8rem;
            font-weight: 600;
            padding: 4px 10px;
            border-radius: 8px;
            border: 1px solid #E2E8F0;
        }

        /* Achievement Badge Card */
        .badge-pill-card {
            background: linear-gradient(135deg, #FFFFFF 0%, #FDF4FF 100%);
            border: 1px solid #FBCFE8;
            border-radius: 16px;
            padding: 1.1rem;
            text-align: center;
            box-shadow: 0 4px 12px rgba(236, 72, 153, 0.06);
            transition: transform 0.2s ease;
        }

        .badge-pill-card:hover {
            transform: scale(1.02);
            box-shadow: 0 8px 18px rgba(236, 72, 153, 0.12);
        }

        /* Skill Level Bar Card */
        .skill-progress-card {
            background: #FFFFFF;
            border-radius: 14px;
            padding: 1rem 1.25rem;
            border: 1px solid var(--border-soft);
            margin-bottom: 0.65rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
        }
    </style>
    """, unsafe_allow_html=True)


def render_top_hero_banner():
    """
    Renders an eye-catching, colorful top hero banner with gradient title,
    value proposition, highlight chips, and animated hero illustration.
    """
    col_text, col_anim = st.columns([2.3, 0.9])

    with col_text:
        st.markdown("""
        <div class="hero-banner-container">
            <span class="hero-badge">✨ Next-Gen Corporate Capability Intelligence · AI Engine 🚀</span>
            <h1 class="gradient-headline">🎯 SkillPath AI · Enterprise Career Accelerator</h1>
            <p class="sub-headline" style="margin-top: 0.5rem; font-size: 1.05rem; color: #475569;">
                Bridging corporate capability gaps with deterministic, explainable AI-driven career roadmaps,
                objective skill gap diagnostics, and real-time workforce mobility intelligence.
            </p>
            <div class="hero-chip-row">
                <span class="hero-chip">🏢 <b>Enterprise Ready</b></span>
                <span class="hero-chip">🎯 <b>8 Standard Tracks</b></span>
                <span class="hero-chip">📚 <b>30+ Curated Courses</b></span>
                <span class="hero-chip">🧠 <b>Bias-Free Diagnostics</b></span>
                <span class="hero-chip">📊 <b>Workforce Mobility ROI</b></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_anim:
        hero_lottie = load_lottie_file("hero_rocket.json")
        if hero_lottie:
            render_lottie(hero_lottie, height=210, key="top_hero_lottie")
        else:
            st.image(
                "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=600&q=80",
                caption="🚀 Empowering Workforce Mastery",
                use_container_width=True
            )


def render_section_header(
    title: str,
    subtitle: str,
    badge: str,
    lottie_filename: Optional[str] = None,
    image_url: Optional[str] = None,
    anim_height: int = 150,
    key_prefix: str = "section"
):
    """
    Renders a colorful section header card with an emoji-packed title,
    subtitle, badge, and either a Lottie animation or high-res illustration.
    """
    col_content, col_visual = st.columns([2.4, 0.9])

    with col_content:
        st.markdown(f"""
        <div class="section-banner-card">
            <span class="hero-badge">{badge}</span>
            <h2 class="section-headline">{title}</h2>
            <p class="sub-headline" style="margin-bottom: 0;">{subtitle}</p>
        </div>
        """, unsafe_allow_html=True)

    with col_visual:
        if lottie_filename:
            lottie_data = load_lottie_file(lottie_filename)
            if lottie_data:
                render_lottie(lottie_data, height=anim_height, key=f"{key_prefix}_lottie")
            elif image_url:
                st.image(image_url, use_container_width=True)
        elif image_url:
            st.image(image_url, use_container_width=True)


def render_roadmap_step_card(m: Dict[str, Any]):
    """
    Renders an individual milestone as a colorful step card with icons,
    status badges, duration chips, and target dates.
    """
    phase_color = m.get("phase_color", "#3B82F6")
    phase_bg = f"{phase_color}18"  # 10% tint
    phase_icons = {
        1: "🌱",
        2: "⚡",
        3: "🚀"
    }
    phase_icon = phase_icons.get(m.get("phase_num", 1), "📌")

    st.markdown(f"""
    <div class="roadmap-card" style="border-left: 6px solid {phase_color};">
        <div class="roadmap-card-header">
            <span class="step-pill" style="background: {phase_color};">⚡ Step {m['step']}</span>
            <span class="phase-pill" style="background: {phase_bg}; color: {phase_color}; border: 1px solid {phase_color}40;">
                {phase_icon} <b>{m['phase_name']}</b>
            </span>
            <span class="schedule-pill">📅 Target: <b>{m['start_date']}</b> ➔ <b>{m['end_date']}</b></span>
        </div>
        <h3 style="font-family: var(--font-display); font-size: 1.25rem; margin: 0.4rem 0 0.6rem 0;">
            <a href="{m['platform_url']}" target="_blank" style="color: #1E293B; text-decoration: none;">
                🔗 {m['title']}
            </a>
        </h3>
        <div class="course-chips">
            <span class="course-chip">🎯 <b>Skill:</b> {m['skill_name']} (Lvl {m['level']}/5)</span>
            <span class="course-chip">🏛️ <b>Provider:</b> {m['provider']}</span>
            <span class="course-chip">⏱️ <b>Study:</b> {m['duration_hours']} hrs</span>
            <span class="course-chip">⏳ <b>Pace:</b> ~{m['weeks_duration']} weeks</span>
        </div>
        <div class="why-box">
            💡 <b>AI Strategic Rationale:</b> {m['explanation']}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_course_card(rec: Dict[str, Any]):
    """
    Renders a course recommendation card with fit badge, provider,
    duration, and AI explanation.
    """
    st.markdown(f"""
    <div class="course-card">
        <div class="course-card-top">
            <h3 class="course-title">
                <a href="{rec['platform_url']}" target="_blank" style="color: #1E293B; text-decoration: none;">
                    🎓 {rec['title']}
                </a>
            </h3>
            <span class="fit-badge">⭐ Fit Score: <b>{rec['score']}</b></span>
        </div>
        <div class="course-chips">
            <span class="course-chip">🏛️ <b>Provider:</b> {rec['provider']}</span>
            <span class="course-chip">🎯 <b>Skill:</b> {rec['skill_name']} (Level {rec['level']}/5)</span>
            <span class="course-chip">⏱️ <b>Duration:</b> {rec['duration_hours']} hrs (~{rec['estimated_weeks']} wks)</span>
            <span class="course-chip">⭐ <b>Rating:</b> {rec['rating']}/5.0</span>
        </div>
        <p style="color: #475569; font-size: 0.93rem; margin: 0.5rem 0 0.75rem 0; line-height: 1.5;">
            {rec['description']}
        </p>
        <div class="why-box">
            💡 <b>Why Recommended:</b> {rec['explanation']}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_skill_progress_item(
    skill_name: str,
    category: str,
    current_lvl: int,
    required_lvl: int,
    gap: int,
    status: str,
    is_core: int
):
    """
    Renders a colorful skill progress bar comparing current proficiency
    against target benchmark level.
    """
    status_colors = {
        "Met / Strong": ("#10B981", "#ECFDF5", "✅ Benchmark Met"),
        "Low Gap": ("#F59E0B", "#FEF3C7", f"⚠️ Low Gap (+{gap})"),
        "Critical Gap": ("#EF4444", "#FEE2E2", f"🚨 Critical Gap (+{gap})")
    }
    color, bg, status_text = status_colors.get(status, ("#64748B", "#F1F5F9", status))
    core_badge = "⭐ Core" if is_core == 1 else "🔹 Elective"

    st.markdown(f"""
    <div class="skill-progress-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
            <span style="font-weight: 700; font-size: 1rem; color: #1E293B;">🎯 {skill_name}</span>
            <div>
                <span style="background: #F1F5F9; color: #475569; font-size: 0.75rem; font-weight: 600; padding: 2px 8px; border-radius: 6px; margin-right: 6px;">{core_badge}</span>
                <span style="background: {bg}; color: {color}; font-size: 0.8rem; font-weight: 700; padding: 3px 10px; border-radius: 12px; border: 1px solid {color}30;">{status_text}</span>
            </div>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 0.82rem; color: #64748B; margin-bottom: 6px;">
            <span>Category: <i>{category}</i></span>
            <span>Current: <b>Level {current_lvl}/5</b> ➔ Benchmark: <b>Level {required_lvl}/5</b></span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(max(0.0, min(1.0, current_lvl / 5.0)))
    st.markdown("<div style='margin-bottom: 0.8rem;'></div>", unsafe_allow_html=True)
