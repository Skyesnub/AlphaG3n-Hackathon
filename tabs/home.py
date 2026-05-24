import streamlit as st
from datetime import date

'''
Home page:
-welcome back sign
-shows quick summary (total tasks, total study min, and average quiz scores)
-if there's no stats yet, don't show any
'''

from tabs.settings import apply_settings


def inject_home_styles():
    st.markdown(
        """
        <style>
            /*
            This Home page stays pretty, but now it follows the colors
            from settings.py's apply_settings().

            Needed variables from settings.py:
            --app-bg
            --hero-bg
            --accent-color
            --card-bg
            --border-color
            --text-color
            --muted-color
            */

            .stApp {
                background: var(--app-bg) !important;
                color: var(--text-color) !important;
            }

            .block-container {
                padding-top: 2rem;
                padding-bottom: 3rem;
                max-width: 1100px;
            }

            .home-hero {
                padding: 2rem 2.2rem;
                border-radius: 28px;
                background: var(--hero-bg);
                color: white;
                box-shadow: 0 18px 45px rgba(15, 23, 42, 0.18);
                margin-bottom: 1.4rem;
            }

            .home-hero h1 {
                font-size: 2.6rem;
                margin-bottom: 0.35rem;
                line-height: 1.1;
                color: white !important;
            }

            .home-hero p {
                font-size: 1.05rem;
                opacity: 0.95;
                margin-bottom: 0;
                color: rgba(255, 255, 255, 0.92) !important;
            }

            .soft-card {
                padding: 1.2rem 1.3rem;
                border-radius: 22px;
                background: var(--card-bg);
                border: 1px solid var(--border-color);
                box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
                margin-bottom: 1rem;
            }

            .motivation-card {
                padding: 1.1rem 1.3rem;
                border-radius: 22px;
                background: var(--card-bg);
                border: 1px solid var(--border-color);
                border-left: 6px solid var(--accent-color);
                box-shadow: 0 10px 26px rgba(15, 23, 42, 0.07);
                margin: 1rem 0 1.2rem 0;
            }

            .motivation-card h3 {
                margin-top: 0;
                margin-bottom: 0.35rem;
                color: var(--accent-color) !important;
            }

            .motivation-card p {
                margin-bottom: 0;
                color: var(--text-color) !important;
            }

            .empty-state {
                padding: 1.6rem;
                border-radius: 24px;
                background: var(--card-bg);
                border: 1px dashed var(--accent-color);
                text-align: center;
                box-shadow: 0 12px 28px rgba(15, 23, 42, 0.08);
            }

            .empty-state h3 {
                margin-bottom: 0.35rem;
                color: var(--accent-color) !important;
            }

            .empty-state p {
                margin-bottom: 0;
                color: var(--muted-color) !important;
            }

            div[data-testid="stMetric"] {
                background: var(--card-bg);
                border: 1px solid var(--border-color);
                padding: 1rem;
                border-radius: 20px;
                box-shadow: 0 10px 26px rgba(15, 23, 42, 0.07);
            }

            div[data-testid="stMetricLabel"] p {
                font-size: 0.95rem;
                color: var(--muted-color) !important;
            }

            div[data-testid="stMetricValue"] {
                color: var(--text-color) !important;
            }

            .stProgress > div > div > div > div {
                background-color: var(--accent-color) !important;
            }

            .stCaptionContainer,
            .stCaptionContainer p {
                color: var(--muted-color) !important;
            }

            .stButton > button {
                border-radius: 14px;
                border: 0;
                background: var(--hero-bg);
                color: white !important;
                font-weight: 700;
                box-shadow: 0 10px 20px rgba(15, 23, 42, 0.15);
            }

            .stButton > button:hover {
                transform: translateY(-1px);
                box-shadow: 0 14px 26px rgba(15, 23, 42, 0.20);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def format_quiz_score(score):
    if score == "N/A":
        return "N/A"

    return f"{round(score*100, 1)}%"


def run_home_page():
    apply_settings()
    inject_home_styles()

    st.markdown(
        """
        <div class="home-hero">
            <h1>🏠 Welcome back!</h1>
            <p>Let’s get organized, study smarter, and make future-you a little less stressed 📚✨</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="motivation-card">
            <h3>🌟 Today’s tiny mission</h3>
            <p>Pick one task, study one small chunk, or review one quiz question. Tiny progress still counts.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Make sure these exist, just in case init_state was not called
    if "tasks" not in st.session_state:
        st.session_state.tasks = []

    if "study_sessions" not in st.session_state:
        st.session_state.study_sessions = []

    if "total_quiz_scores" not in st.session_state:
        st.session_state.total_quiz_scores = []

    '''
    QUICK SUMMARY:
    '''
    st.subheader("📊 Quick Summary")

    # compute total tasks
    total_tasks = len(st.session_state.tasks)
    completed_tasks = 0
    for task in st.session_state.tasks:
        if task.get("status") == "Done":
            completed_tasks += 1

    # compute total study minutes
    total_study_minutes = 0
    for session in st.session_state.study_sessions:
        total_study_minutes += session.get("minutes", 0)

    # compute average quiz score
    average_quiz_score = 0
    if len(st.session_state.total_quiz_scores) > 0:
        average_quiz_score = sum(st.session_state.total_quiz_scores) / len(st.session_state.total_quiz_scores)
    else:
        average_quiz_score = "N/A"

    # check if you're new or not
    if total_tasks == 0 and total_study_minutes == 0 and average_quiz_score == "N/A":
        st.markdown(
            """
            <div class="empty-state">
                <h3>🚀 No stats yet — fresh start energy!</h3>
                <p>Add a task, log a study session, or take a quiz to start building your dashboard.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:
        # display score
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Tasks", total_tasks)
        with col2:
            st.metric("Completed Tasks", completed_tasks)
        with col3:
            st.metric("Study Minutes", total_study_minutes)
        with col4:
            st.metric("Average Quiz Score", format_quiz_score(average_quiz_score))

        if total_tasks > 0:
            completed_percent = round((completed_tasks / total_tasks) * 100, 1)
            st.progress(completed_tasks / total_tasks)
            st.caption(f"✅ You’ve completed {completed_percent}% of your tasks. Keep stacking those small wins.")

        if total_study_minutes > 0:
            st.caption(f"⏱️ Total study time logged: {total_study_minutes} minutes. Future academic weapon loading...")

        if average_quiz_score != "N/A":
            st.caption(f"🧠 Average quiz score: {format_quiz_score(average_quiz_score)}. Review mode stays undefeated.")
