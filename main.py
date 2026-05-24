import streamlit as st
from PIL import Image
from tabs.home import run_home_page
from tabs.planner import run_planner
from tabs.study_tools import run_study_tools
from tabs.progress import run_progress
from tabs.settings import run_settings
from tabs.init import init_state

init_state()

# logo = Image.open("assets/test.png")

st.set_page_config(
    page_title="Productivity App",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide sidebar collapse button
st.markdown("""
<style>

/* Hide collapse button */
[data-testid="stSidebarCollapseButton"] {
    display: none;
}

/* Optional: cleaner top spacing */
[data-testid="stSidebarContent"] {
    padding-top: 1rem;
}

</style>
""", unsafe_allow_html=True)

st.sidebar.image("assets/actual_logo.png", use_container_width=True)

page = st.sidebar.radio(
    "Go to",
    [
        "Home Page",
        "Planner",
        "Study Tools",
        "Progress",
        "Settings",
    ]
)

if page == "Home Page":
    run_home_page()

elif page == "Planner":
    run_planner()

elif page == "Study Tools":
    run_study_tools()

elif page == "Progress":
    run_progress()

elif page == "Settings":
    run_settings()