import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
import random
import re

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(
    page_title="Student Productivity App",
    page_icon="📚",
    layout="wide"
)

# -----------------------------
# Session state defaults
# -----------------------------
def init_state():
    defaults = {
        "dark_mode": False,
        "background": "Default",
        "tasks": [],
        "study_sessions": [],
        "flashcards": [],
        "quiz_history": [],
        "current_quiz": [],
        "quiz_submitted": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_state()

# -----------------------------
# Styling
# -----------------------------
def apply_theme():
    if st.session_state.dark_mode:
        bg_color = "#0f172a"
        text_color = "#e2e8f0"
        card_color = "#1e293b"
        border_color = "#334155"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        card_color = "#ffffff"
        border_color = "#e2e8f0"

    background_choice = st.session_state.background
    if background_choice == "Soft Blue":
        bg_color = "#eff6ff" if not st.session_state.dark_mode else "#0f172a"
    elif background_choice == "Soft Purple":
        bg_color = "#f5f3ff" if not st.session_state.dark_mode else "#1e1b4b"
    elif background_choice == "Soft Green":
        bg_color = "#f0fdf4" if not st.session_state.dark_mode else "#052e16"

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {bg_color};
            color: {text_color};
        }}
        .card {{
            background-color: {card_color};
            padding: 1.2rem;
            border-radius: 18px;
            border: 1px solid {border_color};
            box-shadow: 0 4px 12px rgba(0,0,0,0.06);
            margin-bottom: 1rem;
        }}
        .big-number {{
            font-size: 2rem;
            font-weight: 800;
        }}
        .muted {{
            color: #64748b;
            font-size: 0.95rem;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

apply_theme()

# -----------------------------
# Helper functions
# -----------------------------
def task_dataframe():
    if not st.session_state.tasks:
        return pd.DataFrame(columns=["Task", "Subject", "Due Date", "Priority", "Estimated Minutes", "Status"])
    return pd.DataFrame(st.session_state.tasks)


def sessions_dataframe():
    if not st.session_state.study_sessions:
        return pd.DataFrame(columns=["Date", "Subject", "Topic", "Minutes", "Focus Rating"])
    return pd.DataFrame(st.session_state.study_sessions)


def quiz_history_dataframe():
    if not st.session_state.quiz_history:
        return pd.DataFrame(columns=["Date", "Score", "Total", "Accuracy"])
    return pd.DataFrame(st.session_state.quiz_history)


def make_simple_flashcards(notes):
    """Create simple flashcards from notes.

    This is a rule-based starter version. Later, you can connect this to an AI API.
    """
    sentences = re.split(r"(?<=[.!?])\s+|\n+", notes.strip())
    cards = []

    for sentence in sentences:
        sentence = sentence.strip(" -•\t")
        if len(sentence.split()) < 5:
            continue

        words = re.findall(r"\b[A-Za-z][A-Za-z0-9-]*\b", sentence)
        important_words = [w for w in words if len(w) >= 6]

        if important_words:
            answer = important_words[0]
            question = sentence.replace(answer, "____", 1)
            cards.append({"Front": question, "Back": answer, "Accuracy": None})

    return cards[:10]


def make_quiz_from_flashcards(cards):
    quiz = []
    answers = [card["Back"] for card in cards]

    for card in cards:
        correct = card["Back"]
        wrong_choices = [answer for answer in answers if answer != correct]
        wrong_choices = random.sample(wrong_choices, min(3, len(wrong_choices)))

        while len(wrong_choices) < 3:
            wrong_choices.append(random.choice(["None of these", "Not enough information", "A different topic"]))

        choices = wrong_choices + [correct]
        random.shuffle(choices)

        quiz.append({
            "question": card["Front"],
            "choices": choices,
            "answer": correct,
        })

    return quiz


def generate_schedule(tasks, available_minutes, session_length, break_length):
    incomplete_tasks = [task for task in tasks if task["Status"] != "Done"]
    priority_order = {"High": 0, "Medium": 1, "Low": 2}

    incomplete_tasks.sort(
        key=lambda x: (priority_order.get(x["Priority"], 3), x["Due Date"])
    )

    schedule = []
    remaining = available_minutes
    current_time = datetime.now().replace(second=0, microsecond=0)

    for task in incomplete_tasks:
        if remaining <= 0:
            break

        minutes_needed = int(task["Estimated Minutes"])
        while minutes_needed > 0 and remaining > 0:
            study_block = min(session_length, minutes_needed, remaining)
            start = current_time
            end = start + timedelta(minutes=study_block)

            schedule.append({
                "Time": f"{start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')}",
                "Activity": f"Study: {task['Task']}",
                "Subject": task["Subject"],
            })

            current_time = end
            remaining -= study_block
            minutes_needed -= study_block

            if remaining > break_length and minutes_needed > 0:
                break_start = current_time
                break_end = break_start + timedelta(minutes=break_length)
                schedule.append({
                    "Time": f"{break_start.strftime('%I:%M %p')} - {break_end.strftime('%I:%M %p')}",
                    "Activity": "Break 🌿",
                    "Subject": "Rest",
                })
                current_time = break_end
                remaining -= break_length

    return schedule


# -----------------------------
# Sidebar navigation
# -----------------------------
st.sidebar.title("📚 Productivity App")
page = st.sidebar.radio(
    "Go to",
    ["Home Page", "Planner", "Study Tools", "Progress", "Settings"]
)

# -----------------------------
# Home Page
# -----------------------------
if page == "Home Page":
    st.title("📚 Student Productivity App")
    st.caption("Plan your work, study smarter, and track your progress.")

    tasks_df = task_dataframe()
    sessions_df = sessions_dataframe()
    quiz_df = quiz_history_dataframe()

    today = date.today().isoformat()
    incomplete_tasks = tasks_df[tasks_df["Status"] != "Done"] if not tasks_df.empty else pd.DataFrame()
    due_today = incomplete_tasks[incomplete_tasks["Due Date"] == today] if not incomplete_tasks.empty else pd.DataFrame()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("<div class='card'><div class='muted'>Incomplete Tasks</div><div class='big-number'>" + str(len(incomplete_tasks)) + "</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='card'><div class='muted'>Due Today</div><div class='big-number'>" + str(len(due_today)) + "</div></div>", unsafe_allow_html=True)
    with col3:
        total_minutes = int(sessions_df["Minutes"].sum()) if not sessions_df.empty else 0
        st.markdown("<div class='card'><div class='muted'>Study Minutes</div><div class='big-number'>" + str(total_minutes) + "</div></div>", unsafe_allow_html=True)
    with col4:
        avg_accuracy = round(quiz_df["Accuracy"].mean(), 1) if not quiz_df.empty else 0
        st.markdown("<div class='card'><div class='muted'>Quiz Accuracy</div><div class='big-number'>" + str(avg_accuracy) + "%</div></div>", unsafe_allow_html=True)

    st.subheader("⚡ Quick Actions")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("Go to **Planner** to add assignments and create a schedule.")
    with col2:
        st.info("Go to **Study Tools** to make flashcards and quizzes from notes.")
    with col3:
        st.info("Go to **Progress** to check your study stats and accuracy.")

    st.subheader("🎯 Today's Focus")
    if due_today.empty:
        st.success("No tasks due today. Tiny academic W 😎")
    else:
        st.dataframe(due_today, use_container_width=True)

    if not incomplete_tasks.empty:
        st.subheader("📌 Upcoming Tasks")
        st.dataframe(incomplete_tasks.sort_values("Due Date").head(5), use_container_width=True)

# -----------------------------
# Planner
# -----------------------------
elif page == "Planner":
    st.title("🗓️ Planner")
    st.caption("Add tasks, track study sessions, and generate a study schedule.")

    tab1, tab2, tab3 = st.tabs(["Task Planner", "Study Tracker", "Schedule Generator"])

    with tab1:
        st.subheader("➕ Add a Task")
        with st.form("add_task_form", clear_on_submit=True):
            task_name = st.text_input("Task name")
            subject = st.text_input("Subject")
            due_date = st.date_input("Due date")
            priority = st.selectbox("Priority", ["High", "Medium", "Low"])
            estimated_minutes = st.number_input("Estimated minutes", min_value=5, max_value=600, value=30, step=5)
            submitted = st.form_submit_button("Add Task")

            if submitted:
                if task_name.strip() and subject.strip():
                    st.session_state.tasks.append({
                        "Task": task_name.strip(),
                        "Subject": subject.strip(),
                        "Due Date": due_date.isoformat(),
                        "Priority": priority,
                        "Estimated Minutes": int(estimated_minutes),
                        "Status": "Not Done",
                    })
                    st.success("Task added!")
                else:
                    st.warning("Please enter both a task name and subject.")

        st.subheader("📋 Your Tasks")
        tasks_df = task_dataframe()
        if tasks_df.empty:
            st.info("No tasks yet. Add one above!")
        else:
            edited_tasks = st.data_editor(
                tasks_df,
                use_container_width=True,
                num_rows="dynamic",
                column_config={
                    "Status": st.column_config.SelectboxColumn(
                        "Status",
                        options=["Not Done", "In Progress", "Done"],
                    ),
                    "Priority": st.column_config.SelectboxColumn(
                        "Priority",
                        options=["High", "Medium", "Low"],
                    ),
                }
            )
            st.session_state.tasks = edited_tasks.to_dict("records")

    with tab2:
        st.subheader("⏱️ Log a Study Session")
        with st.form("study_session_form", clear_on_submit=True):
            session_subject = st.text_input("Subject studied")
            topic = st.text_input("Topic")
            minutes = st.number_input("Minutes studied", min_value=1, max_value=300, value=25)
            focus_rating = st.slider("Focus rating", 1, 5, 3)
            session_submit = st.form_submit_button("Log Session")

            if session_submit:
                if session_subject.strip():
                    st.session_state.study_sessions.append({
                        "Date": date.today().isoformat(),
                        "Subject": session_subject.strip(),
                        "Topic": topic.strip(),
                        "Minutes": int(minutes),
                        "Focus Rating": int(focus_rating),
                    })
                    st.success("Study session logged!")
                else:
                    st.warning("Please enter a subject.")

        st.subheader("📖 Study History")
        sessions_df = sessions_dataframe()
        if sessions_df.empty:
            st.info("No study sessions logged yet.")
        else:
            st.dataframe(sessions_df, use_container_width=True)

    with tab3:
        st.subheader("✨ Generate a Study Schedule")
        col1, col2, col3 = st.columns(3)
        with col1:
            available_minutes = st.number_input("Available minutes today", min_value=10, max_value=600, value=120, step=10)
        with col2:
            session_length = st.number_input("Study block length", min_value=5, max_value=120, value=25, step=5)
        with col3:
            break_length = st.number_input("Break length", min_value=0, max_value=60, value=5, step=5)

        if st.button("Generate Schedule"):
            schedule = generate_schedule(st.session_state.tasks, int(available_minutes), int(session_length), int(break_length))
            if not schedule:
                st.warning("No incomplete tasks found, or not enough available time.")
            else:
                st.dataframe(pd.DataFrame(schedule), use_container_width=True)

# -----------------------------
# Study Tools
# -----------------------------
elif page == "Study Tools":
    st.title("🧠 Study Tools")
    st.caption("Turn notes into flashcards and quizzes.")

    notes = st.text_area("Paste your notes here", height=220, placeholder="Example: The gizzard grinds food mechanically. The crop stores food temporarily...")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generate Flashcards"):
            cards = make_simple_flashcards(notes)
            if cards:
                st.session_state.flashcards = cards
                st.success(f"Generated {len(cards)} flashcards!")
            else:
                st.warning("Add more detailed notes so the app can create cards.")

    with col2:
        if st.button("Generate Quiz"):
            if not st.session_state.flashcards:
                cards = make_simple_flashcards(notes)
                st.session_state.flashcards = cards
            if len(st.session_state.flashcards) >= 2:
                st.session_state.current_quiz = make_quiz_from_flashcards(st.session_state.flashcards)
                st.session_state.quiz_submitted = False
                st.success("Quiz generated!")
            else:
                st.warning("Need at least 2 flashcards to make a quiz.")

    st.subheader("🃏 Flashcards")
    if not st.session_state.flashcards:
        st.info("No flashcards yet. Paste notes and click Generate Flashcards.")
    else:
        for i, card in enumerate(st.session_state.flashcards):
            with st.expander(f"Card {i + 1}: {card['Front'][:60]}..."):
                st.write("**Front:**", card["Front"])
                st.write("**Back:**", card["Back"])
                accuracy = st.selectbox(
                    "How well did you know this card?",
                    ["Not rated", "Incorrect", "Almost", "Correct"],
                    key=f"card_accuracy_{i}"
                )
                st.session_state.flashcards[i]["Accuracy"] = accuracy

    st.subheader("📝 Quiz")
    if st.session_state.current_quiz:
        with st.form("quiz_form"):
            user_answers = []
            for i, question in enumerate(st.session_state.current_quiz):
                st.write(f"**{i + 1}. {question['question']}**")
                answer = st.radio(
                    "Choose one:",
                    question["choices"],
                    key=f"quiz_question_{i}"
                )
                user_answers.append(answer)

            submit_quiz = st.form_submit_button("Submit Quiz")

        if submit_quiz:
            score = 0
            total = len(st.session_state.current_quiz)
            for user_answer, question in zip(user_answers, st.session_state.current_quiz):
                if user_answer == question["answer"]:
                    score += 1

            accuracy = round(score / total * 100, 1)
            st.session_state.quiz_history.append({
                "Date": date.today().isoformat(),
                "Score": score,
                "Total": total,
                "Accuracy": accuracy,
            })
            st.session_state.quiz_submitted = True

            st.success(f"You scored {score}/{total} — {accuracy}%")

            if accuracy >= 80:
                st.balloons()
                st.write("Academic weapon behavior detected 🫡")
            elif accuracy >= 50:
                st.write("Solid start. Review the missed cards and rerun it.")
            else:
                st.write("This topic needs a refresh. Happens to the best of us.")

# -----------------------------
# Progress
# -----------------------------
elif page == "Progress":
    st.title("📈 Progress")
    st.caption("Track study time, task completion, card accuracy, and quiz accuracy.")

    tasks_df = task_dataframe()
    sessions_df = sessions_dataframe()
    quiz_df = quiz_history_dataframe()

    col1, col2, col3 = st.columns(3)
    with col1:
        completed = len(tasks_df[tasks_df["Status"] == "Done"]) if not tasks_df.empty else 0
        st.metric("Completed Tasks", completed)
    with col2:
        total_minutes = int(sessions_df["Minutes"].sum()) if not sessions_df.empty else 0
        st.metric("Total Study Minutes", total_minutes)
    with col3:
        avg_quiz = round(quiz_df["Accuracy"].mean(), 1) if not quiz_df.empty else 0
        st.metric("Average Quiz Accuracy", f"{avg_quiz}%")

    st.subheader("⏱️ Study Minutes by Subject")
    if sessions_df.empty:
        st.info("No study data yet.")
    else:
        subject_minutes = sessions_df.groupby("Subject", as_index=False)["Minutes"].sum()
        st.bar_chart(subject_minutes, x="Subject", y="Minutes")

    st.subheader("✅ Task Status")
    if tasks_df.empty:
        st.info("No task data yet.")
    else:
        status_counts = tasks_df["Status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        st.bar_chart(status_counts, x="Status", y="Count")

    st.subheader("🎯 Quiz Accuracy Over Time")
    if quiz_df.empty:
        st.info("No quiz history yet.")
    else:
        st.line_chart(quiz_df, x="Date", y="Accuracy")
        st.dataframe(quiz_df, use_container_width=True)

    st.subheader("🃏 Flashcard Accuracy")
    if not st.session_state.flashcards:
        st.info("No flashcards rated yet.")
    else:
        accuracy_counts = {}
        for card in st.session_state.flashcards:
            rating = card.get("Accuracy", "Not rated")
            accuracy_counts[rating] = accuracy_counts.get(rating, 0) + 1

        accuracy_df = pd.DataFrame({
            "Rating": list(accuracy_counts.keys()),
            "Count": list(accuracy_counts.values())
        })
        st.bar_chart(accuracy_df, x="Rating", y="Count")

# -----------------------------
# Settings
# -----------------------------
elif page == "Settings":
    st.title("⚙️ Settings")
    st.caption("Customize the app appearance.")

    st.subheader("🎨 Appearance")
    dark_mode = st.toggle("Dark mode", value=st.session_state.dark_mode)
    background = st.selectbox(
        "Background",
        ["Default", "Soft Blue", "Soft Purple", "Soft Green"],
        index=["Default", "Soft Blue", "Soft Purple", "Soft Green"].index(st.session_state.background)
    )

    if dark_mode != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_mode
        st.rerun()

    if background != st.session_state.background:
        st.session_state.background = background
        st.rerun()

    st.subheader("🧹 Reset Data")
    st.warning("This clears your current session data. Use carefully.")
    if st.button("Clear All Data"):
        st.session_state.tasks = []
        st.session_state.study_sessions = []
        st.session_state.flashcards = []
        st.session_state.quiz_history = []
        st.session_state.current_quiz = []
        st.success("Data cleared!")
        st.rerun()
