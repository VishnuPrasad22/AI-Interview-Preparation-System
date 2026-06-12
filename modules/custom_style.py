"""
custom_style.py
Place inside `modules/`. Import into app.py and call inject_custom_css() once
right after st.set_page_config().

Design direction:
- Palette: deep navy (#0F172A), slate (#1E293B), accent teal (#14B8A6),
  warm amber highlight (#F59E0B), off-white background (#F8FAFC)
- Display font: 'Sora' (headings) + 'Inter' (body) via Google Fonts
- Card-based sections, pill badges, gradient hero, styled tabs
- Tightened vertical spacing to remove dead whitespace
"""

import streamlit as st


def inject_custom_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Sora:wght@600;700;800&family=Inter:wght@400;500;600&display=swap');

        :root {
            --navy: #0F172A;
            --slate: #1E293B;
            --teal: #14B8A6;
            --amber: #F59E0B;
            --bg: #F8FAFC;
            --card-bg: #FFFFFF;
            --border: #E2E8F0;
            --text-muted: #64748B;
        }

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            color: var(--navy);
        }

        h1, h2, h3, h4 {
            font-family: 'Sora', sans-serif !important;
            font-weight: 700 !important;
            color: var(--navy) !important;
        }

        .stApp {
            background-color: var(--bg);
        }

        /* ---------- Reduce default block spacing ---------- */
        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 2rem !important;
            max-width: 1200px;
        }
        div[data-testid="stVerticalBlock"] > div {
            margin-bottom: 0 !important;
        }
        .element-container {
            margin-bottom: 0.4rem !important;
        }
        h2, h3 {
            margin-top: 0.2rem !important;
            margin-bottom: 0.6rem !important;
        }
        hr {
            border: none;
            border-top: 1px solid var(--border);
            margin: 1rem 0 !important;
        }

        /* ---------- Hero header ---------- */
        .hero-banner {
            background: linear-gradient(135deg, var(--navy) 0%, #1E3A5F 60%, var(--teal) 130%);
            padding: 2rem 2rem;
            border-radius: 16px;
            margin-bottom: 1.25rem;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.25);
        }
        .hero-banner h1 {
            color: #FFFFFF !important;
            font-size: 2.2rem !important;
            margin: 0 0 0.35rem 0 !important;
        }
        .hero-banner p {
            color: #CBD5E1;
            font-size: 1rem;
            margin: 0;
        }

        /* ---------- Card sections ---------- */
        .section-card {
            background-color: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 1.25rem 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
        }
        .section-card h2, .section-card h3, .section-card h4 {
            margin-top: 0 !important;
        }

        /* ---------- Skill badges ---------- */
        .badge {
            display: inline-block;
            padding: 0.3rem 0.85rem;
            border-radius: 999px;
            font-size: 0.85rem;
            font-weight: 600;
            margin: 0.15rem 0.3rem 0.15rem 0;
        }
        .badge-match {
            background-color: rgba(20, 184, 166, 0.12);
            color: #0F766E;
            border: 1px solid rgba(20, 184, 166, 0.3);
        }
        .badge-missing {
            background-color: rgba(239, 68, 68, 0.1);
            color: #B91C1C;
            border: 1px solid rgba(239, 68, 68, 0.25);
        }

        /* ---------- Buttons ---------- */
        .stButton > button, .stDownloadButton > button {
            background-color: var(--navy);
            color: #FFFFFF;
            border: none;
            border-radius: 8px;
            padding: 0.55rem 1.4rem;
            font-weight: 600;
            font-family: 'Inter', sans-serif;
            transition: all 0.2s ease;
        }
        .stButton > button:hover, .stDownloadButton > button:hover {
            background-color: var(--teal);
            color: var(--navy);
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(20, 184, 166, 0.35);
        }

        /* ---------- Metrics ---------- */
        [data-testid="stMetric"] {
            background-color: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 0.8rem 1.1rem;
            box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04);
        }
        [data-testid="stMetricLabel"] {
            color: var(--text-muted) !important;
        }
        [data-testid="stMetricValue"] {
            color: var(--navy) !important;
            font-family: 'Sora', sans-serif;
        }

        /* ---------- Progress bar ---------- */
        .stProgress > div > div > div > div {
            background-color: var(--teal);
        }

        /* ---------- Text areas / inputs ---------- */
        .stTextArea textarea, .stTextInput input {
            border-radius: 10px !important;
            border: 1px solid var(--border) !important;
        }
        .stTextArea textarea:focus, .stTextInput input:focus {
            border-color: var(--teal) !important;
            box-shadow: 0 0 0 2px rgba(20, 184, 166, 0.15) !important;
        }

        /* ---------- Expander ---------- */
        .streamlit-expanderHeader {
            font-weight: 600;
            border-radius: 10px;
        }

        /* ---------- Tabs ---------- */
        .stTabs [data-baseweb="tab-list"] {
            gap: 4px;
            border-bottom: 1px solid var(--border);
        }
        .stTabs [data-baseweb="tab"] {
            height: 42px;
            border-radius: 8px 8px 0 0;
            padding: 0 1.1rem;
            font-weight: 600;
            color: var(--text-muted);
        }
        .stTabs [aria-selected="true"] {
            background-color: var(--card-bg);
            color: var(--navy) !important;
            border-bottom: 2px solid var(--teal);
        }

        /* ---------- Chat bubbles ---------- */
        .chat-user, .chat-coach {
            padding: 0.8rem 1.1rem;
            border-radius: 12px;
            margin-bottom: 0.5rem;
            font-size: 0.95rem;
            line-height: 1.5;
        }
        .chat-user {
            background-color: #EEF2FF;
            border: 1px solid #C7D2FE;
        }
        .chat-coach {
            background-color: #ECFDF5;
            border: 1px solid #A7F3D0;
        }

        /* ---------- Empty state ---------- */
        .empty-state {
            text-align: center;
            padding: 2.5rem 1.5rem;
            color: var(--text-muted);
            border: 1px dashed var(--border);
            border-radius: 14px;
            background-color: var(--card-bg);
        }
        .empty-state h3 {
            color: var(--navy) !important;
            margin-bottom: 0.4rem !important;
        }

        /* ---------- Footer ---------- */
        .app-footer {
            text-align: center;
            color: var(--text-muted);
            font-size: 0.8rem;
            padding: 1.25rem 0 0.5rem 0;
            border-top: 1px solid var(--border);
            margin-top: 1.5rem;
        }

        /* ---------- Sidebar ---------- */
        section[data-testid="stSidebar"] {
            background-color: var(--slate);
        }
        section[data-testid="stSidebar"] * {
            color: #E2E8F0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero():
    st.markdown(
        """
        <div class="hero-banner">
            <h1>🎯 AI Interview Preparation Coach</h1>
            <p>Upload your resume, paste a job description, and get an instant ATS score,
            tailored interview questions, a live mock interview, and a personalized study plan.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_skill_badges(skills, kind="match"):
    """kind: 'match' or 'missing'"""
    css_class = "badge-match" if kind == "match" else "badge-missing"
    icon = "✅" if kind == "match" else "❌"
    if not skills:
        st.write("None found.")
        return
    html = "".join(
        f'<span class="badge {css_class}">{icon} {s}</span>' for s in skills
    )
    st.markdown(html, unsafe_allow_html=True)


def render_empty_state(title, message):
    st.markdown(
        f"""
        <div class="empty-state">
            <h3>{title}</h3>
            <p>{message}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer():
    st.markdown(
        """
        <div class="app-footer">
            AI Interview Preparation Coach &middot; Feedback is AI-generated &mdash;
            use it as guidance, not a guarantee.
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_card_start():
    st.markdown('<div class="section-card">', unsafe_allow_html=True)


def section_card_end():
    st.markdown('</div>', unsafe_allow_html=True)
