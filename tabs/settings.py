import streamlit as st

# ---------------------------------------------------------------------------
# THEME OPTIONS
# Settings-page-only theme preview.
# These colors only affect settings.py unless you copy the system elsewhere.
# ---------------------------------------------------------------------------
THEME_OPTIONS = {
    "Default": {
        "background": "linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%)",
        "header": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "accent": "#667eea",
        "card": "rgba(255, 255, 255, 0.82)",
        "border": "rgba(102, 126, 234, 0.22)",
        "text": "#1f2937",
        "muted": "#6b7280",
    },
    "Warm Peach": {
        "background": "linear-gradient(135deg, #fff7ed 0%, #fed7aa 100%)",
        "header": "linear-gradient(135deg, #fb923c 0%, #f97316 45%, #ea580c 100%)",
        "accent": "#f97316",
        "card": "rgba(255, 247, 237, 0.86)",
        "border": "rgba(249, 115, 22, 0.25)",
        "text": "#431407",
        "muted": "#9a3412",
    },
    "Mint Green": {
        "background": "linear-gradient(135deg, #ecfdf5 0%, #bbf7d0 100%)",
        "header": "linear-gradient(135deg, #34d399 0%, #10b981 50%, #059669 100%)",
        "accent": "#059669",
        "card": "rgba(240, 253, 244, 0.86)",
        "border": "rgba(5, 150, 105, 0.24)",
        "text": "#064e3b",
        "muted": "#047857",
    },
    "Lavender": {
        "background": "linear-gradient(135deg, #faf5ff 0%, #e9d5ff 100%)",
        "header": "linear-gradient(135deg, #a78bfa 0%, #8b5cf6 50%, #7c3aed 100%)",
        "accent": "#7c3aed",
        "card": "rgba(250, 245, 255, 0.86)",
        "border": "rgba(124, 58, 237, 0.24)",
        "text": "#3b0764",
        "muted": "#6b21a8",
    },
    "Rose Pink": {
        "background": "linear-gradient(135deg, #fff1f2 0%, #fecdd3 100%)",
        "header": "linear-gradient(135deg, #fb7185 0%, #f43f5e 50%, #e11d48 100%)",
        "accent": "#e11d48",
        "card": "rgba(255, 241, 242, 0.86)",
        "border": "rgba(225, 29, 72, 0.24)",
        "text": "#4c0519",
        "muted": "#be123c",
    },
    "Deep Red": {
        "background": "linear-gradient(135deg, #fff1f2 0%, #fecaca 48%, #fca5a5 100%)",
        "header": "linear-gradient(135deg, #ef4444 0%, #b91c1c 50%, #7f1d1d 100%)",
        "accent": "#b91c1c",
        "card": "rgba(255, 245, 245, 0.88)",
        "border": "rgba(185, 28, 28, 0.28)",
        "text": "#450a0a",
        "muted": "#991b1b",
    },
    "Midnight": {
        "background": "linear-gradient(135deg, #020617 0%, #111827 45%, #1e1b4b 100%)",
        "header": "linear-gradient(135deg, #312e81 0%, #1e3a8a 45%, #0f172a 100%)",
        "accent": "#93c5fd",
        "card": "rgba(15, 23, 42, 0.72)",
        "border": "rgba(147, 197, 253, 0.22)",
        "text": "#e5e7eb",
        "muted": "#bfdbfe",
    },
}


# ---------------------------------------------------------------------------
# APPLY SETTINGS
# This version only styles Settings itself.
# It does NOT globally carry the custom header/card colors to other tabs.
# ---------------------------------------------------------------------------
def apply_settings():
    theme_name = st.session_state.get("background", "Default")
    theme = THEME_OPTIONS.get(theme_name, THEME_OPTIONS["Default"])

    st.markdown(f"""
        <style>
            :root {{
                --settings-bg: {theme["background"]};
                --settings-header: {theme["header"]};
                --settings-accent: {theme["accent"]};
                --settings-card: {theme["card"]};
                --settings-border: {theme["border"]};
                --settings-text: {theme["text"]};
                --settings-muted: {theme["muted"]};
            }}

            #MainMenu {{ visibility: hidden; }}
            header {{ visibility: hidden; }}
            footer {{ visibility: hidden; }}

            .stApp {{
                background: var(--settings-bg) !important;
                color: var(--settings-text) !important;
            }}

            .stSidebar {{
                background: var(--settings-bg) !important;
            }}

            .settings-hero {{
                background: var(--settings-header);
                padding: 2rem;
                border-radius: 28px;
                color: white;
                box-shadow: 0 16px 40px rgba(0, 0, 0, 0.18);
                margin-bottom: 1.25rem;
            }}

            .settings-hero h1 {{
                color: white !important;
                margin-bottom: 0.3rem;
                font-size: 2.2rem;
            }}

            .settings-hero p {{
                color: rgba(255, 255, 255, 0.9) !important;
                font-size: 1.05rem;
                margin-bottom: 0;
            }}

            .settings-card {{
                background: var(--settings-card);
                border: 1px solid var(--settings-border);
                border-radius: 24px;
                padding: 1.35rem;
                margin: 1rem 0;
                box-shadow: 0 12px 30px rgba(0, 0, 0, 0.08);
                backdrop-filter: blur(10px);
            }}

            .settings-card h3 {{
                color: var(--settings-text) !important;
                margin-top: 0;
            }}

            .settings-muted {{
                color: var(--settings-muted) !important;
                font-size: 0.95rem;
            }}

            .theme-pill {{
                display: inline-block;
                background: var(--settings-header);
                color: white;
                padding: 0.35rem 0.8rem;
                border-radius: 999px;
                font-weight: 700;
                font-size: 0.85rem;
                margin-top: 0.4rem;
                box-shadow: 0 8px 18px rgba(0, 0, 0, 0.12);
            }}

            .preview-strip {{
                height: 78px;
                border-radius: 20px;
                background: var(--settings-header);
                border: 1px solid var(--settings-border);
                box-shadow: inset 0 0 0 1px rgba(255,255,255,0.16);
                margin-top: 0.8rem;
            }}

            div[data-testid="stSelectbox"] label,
            div[data-testid="stButton"] button,
            .stMarkdown, p, label {{
                color: var(--settings-text) !important;
            }}

            div[data-testid="stSelectbox"] > div {{
                border-radius: 16px;
            }}

            .stButton > button {{
                border-radius: 16px !important;
                border: 1px solid var(--settings-border) !important;
                background: rgba(255, 255, 255, 0.72) !important;
                color: var(--settings-text) !important;
                font-weight: 700 !important;
            }}

            .stButton > button:hover {{
                border-color: var(--settings-accent) !important;
                color: var(--settings-accent) !important;
            }}
        </style>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# SETTINGS PAGE
# ---------------------------------------------------------------------------
def run_settings():
    # Make sure default settings exist
    if "background" not in st.session_state:
        st.session_state.background = "Default"

    apply_settings()

    st.markdown("""
        <div class="settings-hero">
            <h1>⚙️ Settings</h1>
            <p>Customize the app's look and preview theme colors.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="settings-card">
            <h3>🎨 Appearance</h3>
            <p class="settings-muted">Choose a theme below. This version previews the matching background and header colors on this page only.</p>
        </div>
    """, unsafe_allow_html=True)

    background = st.selectbox(
        "Theme",
        options=list(THEME_OPTIONS.keys()),
        index=list(THEME_OPTIONS.keys()).index(st.session_state.background),
    )

    if background != st.session_state.background:
        st.session_state.background = background
        st.rerun()

    current_theme = THEME_OPTIONS[st.session_state.background]
    print(st.session_state.background)

    st.markdown(f"""
        <div class="settings-card">
            <h3>Current Theme</h3>
            <span class="theme-pill">{st.session_state.background}</span>
            <div class="preview-strip"></div>
            <p class="settings-muted">
                Accent color: <b>{current_theme["accent"]}</b>
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="settings-card">
            <h3>🔄 Reset</h3>
            <p class="settings-muted">Reset the theme back to Default.</p>
        </div>
    """, unsafe_allow_html=True)

    if st.button("Reset to Defaults"):
        st.session_state.background = "Default"
        st.rerun()
