import streamlit as st

# ---------------------------------------------------------------------------
# BACKGROUND OPTIONS
# Maps display names to CSS gradient strings.
# "Default" means no custom background (empty string = no CSS injected).
# ---------------------------------------------------------------------------
BACKGROUND_OPTIONS = {
    "Default": "",
    "Soft Blue": "linear-gradient(135deg, #e8f4f8 0%, #d6eaf8 100%)",
    "Warm Peach": "linear-gradient(135deg, #fef9f0 0%, #fde8d8 100%)",
    "Mint Green": "linear-gradient(135deg, #f0faf4 0%, #d5f5e3 100%)",
    "Lavender": "linear-gradient(135deg, #f5f0ff 0%, #e8daff 100%)",
}


# ---------------------------------------------------------------------------
# APPLY SETTINGS
# Injects CSS into the page based on the current session_state values.
# Call this AFTER all widgets have run so it reads the latest values.
# Import and call this at the bottom of every other page too, so the
# theme persists when the user navigates away from Settings.
# ---------------------------------------------------------------------------
def apply_settings():
    css_parts = []

    # --- Dark mode ---
    if st.session_state.get("dark_mode", False):
        css_parts.append("""
            .stApp { background: #1e1e1e !important; color: #e8e8e8 !important; }
            .stSidebar { background-color: #2a2a2a !important; }
            .stMarkdown, .stText, h1, h2, h3, h4, p, label { color: #e8e8e8 !important; }
            .stMetric label, .stMetric div { color: #cccccc !important; }
            .stTextInput input, .stSelectbox select, .stTextArea textarea {
                background-color: #2e2e2e !important;
                color: #e8e8e8 !important;
                border-color: #555 !important;
            }
        """)

    # --- Background gradient ---
    bg = st.session_state.get("background", "Default")
    if bg != "Default" and not st.session_state.get("dark_mode", False):
        css_parts.append(f".stApp, .stSidebar {{ background: {BACKGROUND_OPTIONS[bg]} !important; }}")

    # --- Hide Streamlit toolbar/footer --- always applies
    css_parts.append("""
        #MainMenu { visibility: hidden; }
        header { visibility: hidden; }
        footer { visibility: hidden; }
    """)

    # Inject all CSS at once
    st.markdown(f"<style>{''.join(css_parts)}</style>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# SETTINGS PAGE
# ---------------------------------------------------------------------------
def run_settings():
    st.title("⚙️ Settings")
    st.write("Customize your experience.")

    st.subheader("🎨 Appearance")

    # Read current values from session_state as the starting point
    dark_mode = st.toggle(
        "Dark Mode",
        value=st.session_state.dark_mode,  # no key=, just value=
    )
    st.session_state.dark_mode = dark_mode  # manually save it back

    background = st.selectbox(
        "Background",
        options=list(BACKGROUND_OPTIONS.keys()),
        index=list(BACKGROUND_OPTIONS.keys()).index(st.session_state.background),
        disabled=dark_mode,  # no key=, just value= and index=
    )
    st.session_state.background = background  # manually save it back

    if dark_mode:
        st.caption("Background is disabled while Dark Mode is on.")

    st.divider()

    st.subheader("🔄 Reset")
    if st.button("Reset to Defaults"):
        st.session_state.dark_mode = False
        st.session_state.background = "Default"
        st.rerun()

    apply_settings()