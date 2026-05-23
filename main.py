import streamlit as st

from tabs.home import run_home_page
from tabs.planner import run_planner
from tabs.study_tools import run_study_tools
from tabs.progress import run_progress
from tabs.settings import run_settings
from tabs.init import init_state

init_state()

st.set_page_config(
    page_title="Productivity App",
    page_icon="📚",
    layout="wide"
)


st.sidebar.title("📚 Productivity App")

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