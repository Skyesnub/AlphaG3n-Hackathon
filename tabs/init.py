import streamlit as st

def init_state():
    defaults = {
        # Planner
        "tasks": [],

        # Study tracker
        "study_sessions": [],

        # Study tools
        "flashcards": [],
        "quizzes": [],
        "quiz_scores": [],

        # Progress
        "card_accuracy": {},

        # Settings
        "dark_mode": False,
        "background": "Default",
    }

    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value