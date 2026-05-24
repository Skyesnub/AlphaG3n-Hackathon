import streamlit as st
from datetime import date, datetime
from tabs.settings import apply_settings
import pandas as pd
import matplotlib.pyplot as plt

if "flashcards" not in st.session_state:
    st.session_state.flashcards = []

if "know_flashcards" not in st.session_state:
    st.session_state.know_flashcards = []

if "review_flashcards" not in st.session_state:
    st.session_state.review_flashcards = []

if "quizzes" not in st.session_state:
    st.session_state.quizzes = []

if "total_quiz_scores" not in st.session_state:
    st.session_state.total_quiz_scores = []

if "cur_quiz_scores" not in st.session_state:
    st.session_state.cur_quiz_scores = []


def apply_progress_styles():
    st.markdown(
        """
        <style>
            /*
            Progress keeps the same Study Tools-style layout,
            but now follows colors from settings.py's apply_settings().

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
                max-width: 1050px;
            }

            .study-hero {
                padding: 1.4rem 1.6rem;
                border-radius: 28px;
                background: var(--hero-bg);
                color: white;
                box-shadow: 0 18px 45px rgba(15, 23, 42, 0.18);
                margin-bottom: 1.2rem;
            }

            .study-hero h1 {
                margin: 0;
                font-size: 2.25rem;
                letter-spacing: -0.04em;
                color: white !important;
            }

            .study-hero p {
                margin: 0.45rem 0 0 0;
                font-size: 1.05rem;
                opacity: 0.95;
                color: rgba(255, 255, 255, 0.92) !important;
            }

            .section-title {
                padding: 0.75rem 1rem;
                border-radius: 18px;
                background: var(--card-bg);
                border: 1px solid var(--border-color);
                box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
                margin-top: 1rem;
                margin-bottom: 0.75rem;
                font-weight: 800;
                font-size: 1.35rem;
                color: var(--accent-color);
            }

            .stat-card {
                padding: 1rem;
                border-radius: 22px;
                background: var(--card-bg);
                border: 1px solid var(--border-color);
                box-shadow: 0 10px 28px rgba(15, 23, 42, 0.06);
                min-height: 108px;
            }

            .stat-card .label {
                color: var(--muted-color);
                font-size: 0.82rem;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: 0.04em;
            }

            .stat-card .value {
                color: var(--text-color);
                font-size: 1.55rem;
                font-weight: 900;
                margin-top: 0.3rem;
            }

            .mini-card {
                padding: 0.9rem 1rem;
                border-radius: 18px;
                background: var(--card-bg);
                border: 1px solid var(--border-color);
                box-shadow: 0 8px 22px rgba(15, 23, 42, 0.04);
                margin-bottom: 0.45rem;
                color: var(--text-color);
            }

            .mini-card b {
                color: var(--text-color);
            }

            .subtle-text {
                color: var(--muted-color);
                font-size: 0.95rem;
            }

            div.stButton > button {
                border-radius: 999px;
                border: 0;
                background: var(--hero-bg);
                color: white !important;
                font-weight: 700;
                box-shadow: 0 9px 18px rgba(15, 23, 42, 0.14);
                transition: transform 0.12s ease, box-shadow 0.12s ease;
            }

            div.stButton > button:hover {
                transform: translateY(-1px);
                box-shadow: 0 12px 24px rgba(15, 23, 42, 0.20);
            }

            div[data-testid="stAlert"] {
                border-radius: 18px;
                border: 1px solid var(--border-color);
                box-shadow: 0 8px 22px rgba(15, 23, 42, 0.05);
            }

            details {
                border-radius: 18px !important;
                background: var(--card-bg) !important;
                border: 1px solid var(--border-color) !important;
                box-shadow: 0 8px 22px rgba(15, 23, 42, 0.04);
            }

            hr {
                margin: 1.4rem 0;
                border-color: var(--border-color);
            }

            div[data-testid="stMetric"] {
                background: var(--card-bg);
                border: 1px solid var(--border-color);
                border-radius: 20px;
                padding: 0.75rem 0.9rem;
                box-shadow: 0 8px 22px rgba(15, 23, 42, 0.04);
            }

            div[data-testid="stMetricLabel"] p {
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

            h1, h2, h3, h4, p, label {
                color: var(--text-color);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def section_header(text):
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)


def stat_card(label, value):
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="label">{label}</div>
            <div class="value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def mini_card(content):
    st.markdown(f'<div class="mini-card">{content}</div>', unsafe_allow_html=True)


def run_progress():
    apply_settings()
    apply_progress_styles()

    st.markdown(
        """
        <div class="study-hero">
            <h1>📊 Progress</h1>
            <p>Track your workload and study habits.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Make sure all needed keys exist
    if "tasks" not in st.session_state:
        st.session_state.tasks = []
    if "study_sessions" not in st.session_state:
        st.session_state.study_sessions = []

    today = date.today()

    # -----------------------------------------------------------------------
    # SECTION 1 — HOMEWORK REMAINING
    # Adds up minutes for all tasks that aren't marked Done.
    # -----------------------------------------------------------------------
    section_header("📚 Homework Remaining")

    incomplete_tasks = [t for t in st.session_state.tasks if t.get("status") != "Done"]

    if not incomplete_tasks:
        st.success("🎉 No homework left! You're all caught up.")
    else:
        total_mins = 0
        for t in incomplete_tasks:
            # Support old tasks stored with "hours"
            if "minutes" in t:
                total_mins += t["minutes"]
            elif "hours" in t:
                total_mins += int(t["hours"] * 60)

        hours, mins = divmod(total_mins, 60)
        done_count = len([t for t in st.session_state.tasks if t.get("status") == "Done"])
        total_count = len(st.session_state.tasks)
        pct = int((done_count / total_count) * 100) if total_count > 0 else 0

        col1, col2, col3 = st.columns(3)
        with col1:
            stat_card("Incomplete Assignments", len(incomplete_tasks))
        with col2:
            stat_card("Total Time Remaining", f"{hours}h {mins}m" if hours > 0 else f"{mins}m")
        with col3:
            stat_card("Completion Rate", f"{pct}%")

        # Progress bar showing how much is done
        if total_count > 0:
            st.progress(pct / 100, text=f"{done_count} of {total_count} assignments complete")

    # -----------------------------------------------------------------------
    # SECTION 2 — UPCOMING DUE DATES
    # Finds the next day that has assignments due and shows them.
    # -----------------------------------------------------------------------
    section_header("📅 Upcoming Due Dates")

    if not st.session_state.tasks:
        st.info("No assignments added yet.")
    else:
        # Group all incomplete tasks by due date
        upcoming = {}
        overdue = []
        for task in st.session_state.tasks:
            if task.get("status") == "Done":
                continue
            due = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
            if due < today:
                overdue.append(task)
            else:
                upcoming.setdefault(due, []).append(task)

        # Show overdue tasks first
        if overdue:
            st.error(f"⚠️ {len(overdue)} overdue assignment(s):")
            for task in overdue:
                color = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}.get(task["priority"], "⚪")
                days_ago = (today - datetime.strptime(task["due_date"], "%Y-%m-%d").date()).days
                mini_card(f"{color} <b>{task['name']}</b> — was due {days_ago} day(s) ago")

        # Show the next upcoming due date and all tasks on that day
        if upcoming:
            next_due_date = min(upcoming.keys())
            days_until = (next_due_date - today).days
            tasks_due = upcoming[next_due_date]

            if days_until == 0:
                label = "today"
            elif days_until == 1:
                label = "tomorrow"
            else:
                label = f"in {days_until} days"

            st.info(f"📌 Next due date: **{next_due_date.strftime('%A, %B %d')}** ({label})")

            for task in tasks_due:
                color = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}.get(task["priority"], "⚪")
                if "minutes" in task:
                    mins = task["minutes"]
                elif "hours" in task:
                    mins = int(task["hours"] * 60)
                else:
                    mins = 0
                h, m = divmod(mins, 60)
                time_str = f"{h}h {m}m" if h > 0 else f"{m}m"
                mini_card(f"{color} <b>{task['name']}</b> — {time_str} remaining · {task['priority']} priority")

            # Also show any other upcoming due dates after that
            future_dates = sorted([d for d in upcoming if d > next_due_date])
            if future_dates:
                with st.expander(f"View {len(future_dates)} more upcoming due date(s)"):
                    for d in future_dates:
                        st.markdown(f"**{d.strftime('%A, %B %d')}**")
                        for task in upcoming[d]:
                            color = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}.get(task["priority"], "⚪")
                            mini_card(f"{color} {task['name']} · {task['priority']} priority")
        else:
            if not overdue:
                st.success("No upcoming assignments!")

    # -----------------------------------------------------------------------
    # SECTION 3 — TIME STUDIED PER SUBJECT
    # Reads from st.session_state.study_sessions, which will be populated
    # by the study timer you'll add to the planner.
    # Each session is expected to be:
    #   {"subject": str, "minutes": int, "date": "YYYY-MM-DD"}
    # -----------------------------------------------------------------------
    section_header("⏱ Time Studied Per Subject")

    if not st.session_state.study_sessions:
        st.info("No study sessions recorded yet. Start a study session from the Planner to track time here.")
    else:
        # Aggregate total minutes per subject
        subject_totals = {}
        for session in st.session_state.study_sessions:
            subject = session.get("subject", "Unknown")
            mins = session.get("minutes", 0)
            subject_totals[subject] = subject_totals.get(subject, 0) + mins

        # Sort by most studied
        sorted_subjects = sorted(subject_totals.items(), key=lambda x: x[1], reverse=True)
        total_studied = sum(subject_totals.values())

        # -------------------------------------------------------------------
        # WORKLOAD COMPLETION PIE CHART
        # -------------------------------------------------------------------

        # Calculate remaining homework minutes
        remaining_minutes = 0

        for task in st.session_state.tasks:
            if task.get("status") != "Done":
                if "minutes" in task:
                    remaining_minutes += task["minutes"]
                elif "hours" in task:
                    remaining_minutes += int(task["hours"] * 60)

        # Total overall workload
        overall_total = total_studied + remaining_minutes

        # Only show chart if there is data
        if overall_total > 0:
            st.write("### 🥧 Study Progress")

            labels = ["Studied", "Remaining"]
            sizes = [total_studied, remaining_minutes]

            fig, ax = plt.subplots(figsize=(2, 2))
            fig.patch.set_alpha(0)
            ax.set_facecolor("none")

            ax.pie(
                sizes,
                labels=labels,
                autopct="%1.1f%%",
                startangle=90,
            )

            ax.axis("equal")

            st.pyplot(fig, use_container_width=False)

            studied_pct = int((total_studied / overall_total) * 100)

            st.caption(
                f"You've completed approximately {studied_pct}% of your total estimated workload."
            )

        total_h, total_m = divmod(total_studied, 60)
        stat_card("Total Study Time", f"{total_h}h {total_m}m" if total_h > 0 else f"{total_m}m")

        st.write("**By subject:**")
        for subject, mins in sorted_subjects:
            h, m = divmod(mins, 60)
            time_str = f"{h}h {m}m" if h > 0 else f"{m}m"
            pct = int((mins / total_studied) * 100) if total_studied > 0 else 0
            mini_card(f"<b>{subject}</b> — {time_str}")
            st.progress(pct / 100, text=f"{pct}% of total study time")

    section_header("🧠 Study Tools Performance")

    # -----------------------------
    # QUIZ ACCURACY
    # -----------------------------
    total_scores = st.session_state.total_quiz_scores
    cur_scores = st.session_state.cur_quiz_scores

    total_acc = (sum(total_scores) / len(total_scores) * 100) if total_scores else None
    cur_acc = (sum(cur_scores) / len(cur_scores) * 100) if cur_scores else None

    col1, col2 = st.columns(2)

    with col1:
        stat_card("Quiz Accuracy (Current)", f"{cur_acc:.1f}%" if cur_acc is not None else "N/A")

    with col2:
        stat_card("Quiz Accuracy (Total)", f"{total_acc:.1f}%" if total_acc is not None else "N/A")

    know = len(st.session_state.know_flashcards)
    review = len(st.session_state.review_flashcards)
    total_cards = len(st.session_state.flashcards)

    if total_cards > 0:
        st.write("### Flashcard Mastery")

        mastery_pct = (know / total_cards) * 100

        stat_card("Mastery Rate", f"{mastery_pct:.1f}%")
        st.progress(mastery_pct / 100)

        col1, col2, col3 = st.columns(3)
        with col1:
            stat_card("Known", know)
        with col2:
            stat_card("Review", review)
        with col3:
            stat_card("Total Cards", total_cards)
    else:
        st.info("No flashcards generated yet.")

    apply_settings()
