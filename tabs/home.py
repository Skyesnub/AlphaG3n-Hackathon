import streamlit as st
from datetime import date


def run_home_page():
    st.title("🏠 Home Page")
    st.write("Welcome back! Let's get organized and study smarter 📚")

    # Make sure these exist, just in case init_state was not called
    if "tasks" not in st.session_state:
        st.session_state.tasks = []

    if "study_sessions" not in st.session_state:
        st.session_state.study_sessions = []

    if "quiz_scores" not in st.session_state:
        st.session_state.quiz_scores = []

    '''
    QUICK SUMMARY:
    -show total tasks, total study min, and average quiz scores
    -
    
    '''
    st.subheader("📊 Quick Summary")

    total_tasks = len(st.session_state.tasks)
    completed_tasks = 0

    for task in st.session_state.tasks:
        if task.get("status") == "Done":
            completed_tasks += 1

    total_study_minutes = 0

    for session in st.session_state.study_sessions:
        total_study_minutes += session.get("minutes", 0)

    average_quiz_score = 0

    if len(st.session_state.quiz_scores) > 0:
        average_quiz_score = sum(st.session_state.quiz_scores) / len(st.session_state.quiz_scores)
    else:
        average_quiz_score = "N/A"
        
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Tasks", total_tasks)

    with col2:
        st.metric("Completed Tasks", completed_tasks)

    with col3:
        st.metric("Study Minutes", total_study_minutes)

    st.metric("Average Quiz Score", average_quiz_score)