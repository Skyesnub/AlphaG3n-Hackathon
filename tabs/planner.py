import streamlit as st
from datetime import date, datetime, timedelta
from tabs.settings import apply_settings
import calendar
import time
import uuid


def inject_planner_styles():
    st.markdown(
        """
        <style>
            /*
            This Planner page keeps the same pretty layout,
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
                max-width: 1180px;
            }

            .planner-hero {
                padding: 2rem 2.2rem;
                border-radius: 28px;
                background: var(--hero-bg);
                color: white;
                box-shadow: 0 18px 45px rgba(15, 23, 42, 0.18);
                margin-bottom: 1.35rem;
            }

            .planner-hero h1 {
                font-size: 2.55rem;
                line-height: 1.08;
                margin-bottom: 0.35rem;
                color: white !important;
            }

            .planner-hero p {
                font-size: 1.05rem;
                opacity: 0.95;
                margin-bottom: 0;
                color: rgba(255, 255, 255, 0.92) !important;
            }

            .planner-tip {
                padding: 1.05rem 1.25rem;
                border-radius: 22px;
                background: var(--card-bg);
                border: 1px solid var(--border-color);
                border-left: 6px solid var(--accent-color);
                box-shadow: 0 10px 26px rgba(15, 23, 42, 0.07);
                margin: 1rem 0 1.25rem 0;
            }

            .planner-tip h3 {
                margin-top: 0;
                margin-bottom: 0.35rem;
                color: var(--accent-color) !important;
            }

            .planner-tip p {
                margin-bottom: 0;
                color: var(--text-color) !important;
            }

            .section-card {
                padding: 1.15rem 1.25rem;
                border-radius: 24px;
                background: var(--card-bg);
                border: 1px solid var(--border-color);
                box-shadow: 0 12px 30px rgba(15, 23, 42, 0.07);
                margin: 0.8rem 0 1rem 0;
            }

            .section-card h3 {
                color: var(--accent-color) !important;
            }

            .section-card p {
                color: var(--muted-color) !important;
            }

            .task-done {
                text-decoration: line-through;
                opacity: 0.58;
            }

            .task-box {
                padding: 0.9rem 1rem;
                border-radius: 18px;
                background: var(--card-bg);
                border: 1px solid var(--border-color);
                box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
                margin: 0.35rem 0 0.25rem 0;
                color: var(--text-color);
            }

            .calendar-day {
                min-height: 4.3rem;
                padding: 0.5rem 0.45rem;
                border-radius: 16px;
                background: var(--card-bg);
                border: 1px solid var(--border-color);
                box-shadow: 0 6px 16px rgba(15, 23, 42, 0.045);
                margin-bottom: 0.35rem;
                color: var(--text-color);
            }

            .calendar-day-active {
                background: var(--card-bg);
                border: 1px solid var(--accent-color);
                box-shadow: 0 10px 22px rgba(15, 23, 42, 0.10);
            }

            .calendar-day-muted {
                min-height: 4.3rem;
                padding: 0.5rem;
                border-radius: 16px;
                background: rgba(255, 255, 255, 0.18);
                border: 1px dashed var(--border-color);
                margin-bottom: 0.35rem;
            }

            .daily-block {
                padding: 0.85rem 1rem;
                border-radius: 18px;
                background: var(--card-bg);
                border: 1px solid var(--border-color);
                border-left: 5px solid var(--accent-color);
                box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
                margin: 0.45rem 0;
                color: var(--text-color);
            }

            .daily-block-break {
                padding: 0.75rem 1rem;
                border-radius: 18px;
                background: var(--card-bg);
                border: 1px solid var(--border-color);
                border-left: 5px solid var(--muted-color);
                box-shadow: 0 8px 20px rgba(15, 23, 42, 0.045);
                margin: 0.45rem 0;
                color: var(--text-color);
            }

            .empty-state {
                padding: 1.35rem;
                border-radius: 22px;
                background: var(--card-bg);
                border: 1px dashed var(--accent-color);
                text-align: center;
                box-shadow: 0 12px 28px rgba(15, 23, 42, 0.08);
                color: var(--muted-color);
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

            .stButton > button {
                border-radius: 14px;
                border: 0;
                background: var(--hero-bg);
                color: white !important;
                font-weight: 700;
                box-shadow: 0 10px 20px rgba(15, 23, 42, 0.15);
                transition: 0.16s ease-in-out;
            }

            .stButton > button:hover {
                transform: translateY(-1px);
                box-shadow: 0 14px 26px rgba(15, 23, 42, 0.20);
            }

            .stTextInput input, .stNumberInput input, textarea {
                border-radius: 14px;
            }

            div[data-baseweb="select"] > div {
                border-radius: 14px;
            }

            div[data-testid="stExpander"] {
                border-radius: 18px;
                border: 1px solid var(--border-color);
                box-shadow: 0 8px 20px rgba(15, 23, 42, 0.045);
                background: var(--card-bg);
            }

            .stProgress > div > div > div > div {
                background-color: var(--accent-color) !important;
            }

            .stCaptionContainer,
            .stCaptionContainer p {
                color: var(--muted-color) !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def section_card(title, body):
    st.markdown(
        f"""
        <div class="section-card">
            <h3 style="margin-top:0; margin-bottom:0.25rem;">{title}</h3>
            <p style="margin-bottom:0;">{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def fmt_time(minutes):
    """Convert minutes to a readable string like '1h 30m' or '45m'."""
    minutes = round(minutes)
    if minutes >= 60:
        h, m = divmod(minutes, 60)
        return f"{h}h {m}m" if m > 0 else f"{h}h"
    return f"{minutes}m"


def time_to_minutes(t):
    """Convert a time object to minutes since midnight."""
    return t.hour * 60 + t.minute


def minutes_to_time_str(mins):
    """Convert minutes since midnight to a readable time string like '3:30 PM'."""
    h, m = divmod(int(mins), 60)
    period = "AM" if h < 12 else "PM"
    h12 = h % 12 or 12
    return f"{h12}:{m:02d} {period}"


def prune_completed_tasks(limit=5):
    done_tasks = [task for task in st.session_state.tasks if task.get("status") == "Done"]
    if len(done_tasks) <= limit:
        return 0

    done_tasks.sort(key=lambda task: task.get("due_date", "9999-12-31"))
    ids_to_delete = {task["id"] for task in done_tasks[:-limit]}
    st.session_state.tasks = [
        task for task in st.session_state.tasks if task.get("id") not in ids_to_delete
    ]
    return len(ids_to_delete)


def run_planner():
    apply_settings()
    inject_planner_styles()

    st.markdown(
        """
        <div class="planner-hero">
            <h1>📅 Planner</h1>
            <p>Add assignments, map out due dates, and turn your workload into a study plan that actually feels doable ✨</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="planner-tip">
            <h3>🌟 Tiny planning win</h3>
            <p>Break big assignments into time chunks. Your schedule works better when your brain is not being jump-scared by giant tasks.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------------------------
    # ADD TASK FORM
    # -----------------------------------------------------------------------
    section_card("➕ Add Assignment", "Add the assignment, deadline, estimated time, and priority.")

    task_name = st.text_input("Assignment Name", placeholder="e.g. Math Homework")

    col1, col2 = st.columns(2)
    with col1:
        due_date = st.date_input("Due Date", min_value=date.today())
    with col2:
        st.write("Estimated Time")
        tcol1, tcol2 = st.columns(2)
        with tcol1:
            est_hours = st.number_input("Hours", min_value=0, max_value=23, step=1, value=1, key="add_hours")
        with tcol2:
            est_minutes = st.number_input("Minutes", min_value=0, max_value=59, step=10, value=0, key="add_minutes")

    priority = st.selectbox("Priority", ["Low", "Medium", "High"])

    if st.button("Add Assignment", type="primary"):
        total_minutes = est_hours * 60 + est_minutes
        if task_name.strip() == "":
            st.error("Please enter an assignment name.")
        elif total_minutes < 10:
            st.error("Minimum time is 10 minutes.")
        else:
            st.session_state.tasks.append({
                "id": str(uuid.uuid4()),
                "name": task_name.strip(),
                "due_date": due_date.strftime("%Y-%m-%d"),
                "minutes": total_minutes,
                "priority": priority,
                "status": "To Do",
            })
            st.success(f"Added: {task_name} ({fmt_time(total_minutes)})")
            st.rerun()

    st.divider()

    # -----------------------------------------------------------------------
    # TASK LIST
    # -----------------------------------------------------------------------
    section_card("📋 Assignments", "See what is coming up, what is done, and what needs your attention next.")
    deleted_completed_count = prune_completed_tasks()

    if deleted_completed_count > 0:
        st.caption(
            f"Removed {deleted_completed_count} older completed assignment(s) to keep your recent history tidy."
        )

    if not st.session_state.tasks:
        st.markdown(
            """
            <div class="empty-state">
                <b>📝 No assignments yet.</b><br>
                Add one above and your planner will start building the dashboard.
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        sorted_tasks = sorted(st.session_state.tasks, key=lambda x: x["due_date"])

        incomplete = [t for t in sorted_tasks if t.get("status") != "Done"]
        done = [t for t in sorted_tasks if t.get("status") == "Done"]

        all_to_show = incomplete + done

        for task in all_to_show:

            is_done = task.get("status") == "Done"
            color = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}.get(task["priority"], "⚪")

            due = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
            days_left = (due - date.today()).days

            if is_done:
                urgency = "✅ Done"
            elif days_left < 0:
                urgency = "⚠️ Overdue"
            elif days_left == 0:
                urgency = "⚠️ Due today"
            elif days_left == 1:
                urgency = "Due tomorrow"
            else:
                urgency = f"Due in {days_left} days"

            container = st.container()

            with container:
                css_class = "task-done" if is_done else ""

                st.markdown(
                    f"<div class='task-box {css_class}'>"
                    f"{color} <b>{task['name']}</b> — {task['due_date']} ({urgency})"
                    f"</div>",
                    unsafe_allow_html=True
                )

                with st.expander("Details", expanded=False):

                    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])

                    with col1:
                        st.write(f"⏱ **Time:** {fmt_time(task['minutes'])}")

                    with col2:
                        st.write(f"📌 **Priority:** {task['priority']}")

                    with col3:
                        status_options = ["To Do", "In Progress", "Done"]

                        current_index = status_options.index(task["status"])

                        new_status = st.selectbox(
                            "Status",
                            status_options,
                            index=current_index,
                            key=f"status_{task['id']}",
                        )

                        if new_status != task["status"]:
                            for t in st.session_state.tasks:
                                if t["id"] == task["id"]:
                                    t["status"] = new_status
                            st.rerun()

                    with col4:
                        st.write("")
                        if st.button("🗑", key=f"delete_task_{task['id']}", help="Delete assignment"):
                            st.session_state.tasks = [
                                t for t in st.session_state.tasks if t["id"] != task["id"]
                            ]
                            st.rerun()

    st.divider()

    # -----------------------------------------------------------------------
    # CALENDAR VIEW — due dates
    # -----------------------------------------------------------------------
    section_card("🗓 Due Date Calendar", "A quick month view of deadlines, with priority colors at a glance.")

    today = date.today()
    selected_month = st.selectbox(
        "Month",
        options=[date(today.year, m, 1).strftime("%B %Y") for m in range(1, 13)],
        index=today.month - 1,
        key="due_cal_month",
    )
    month_date = datetime.strptime(selected_month, "%B %Y")
    selected_year = month_date.year
    selected_month_num = month_date.month

    tasks_by_day = {}
    for task in st.session_state.tasks:
        d = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
        if d.year == selected_year and d.month == selected_month_num:
            tasks_by_day.setdefault(d.day, []).append(task)

    cal = calendar.monthcalendar(selected_year, selected_month_num)
    cols = st.columns(7)
    for col, day_name in zip(cols, ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
        col.markdown(f"**{day_name}**")
    for week in cal:
        cols = st.columns(7)
        for col, day in zip(cols, week):
            if day == 0:
                col.markdown("<div class='calendar-day-muted'></div>", unsafe_allow_html=True)
            elif day in tasks_by_day:
                icons = " ".join(
                    {"Low": "🟢", "Medium": "🟡", "High": "🔴"}.get(t["priority"], "⚪")
                    for t in tasks_by_day[day]
                )
                col.markdown(
                    f"<div class='calendar-day calendar-day-active'><b>{day}</b><br>{icons}</div>",
                    unsafe_allow_html=True,
                )
            else:
                col.markdown(f"<div class='calendar-day'><b>{day}</b></div>", unsafe_allow_html=True)

    st.divider()

    # -----------------------------------------------------------------------
    # AVAILABILITY INPUT
    # -----------------------------------------------------------------------
    section_card("⏰ Your Daily Availability", "Set the time window you are free to study each day.")

    if "availability" not in st.session_state:
        st.session_state.availability = {
            "Monday":    {"start": 16 * 60, "end": 20 * 60},
            "Tuesday":   {"start": 16 * 60, "end": 20 * 60},
            "Wednesday": {"start": 16 * 60, "end": 20 * 60},
            "Thursday":  {"start": 16 * 60, "end": 20 * 60},
            "Friday":    {"start": 16 * 60, "end": 20 * 60},
            "Saturday":  {"start": 10 * 60, "end": 18 * 60},
            "Sunday":    {"start": 10 * 60, "end": 18 * 60},
        }

    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    cols = st.columns(7)
    for col, day in zip(cols, days_of_week):
        with col:
            col.markdown(f"**{day[:3]}**")
            current = st.session_state.availability.get(day, {"start": 16 * 60, "end": 20 * 60})
            start_h, start_m = divmod(current["start"], 60)
            end_h, end_m = divmod(current["end"], 60)

            start_time = col.time_input(
                "From", value=datetime(2000, 1, 1, start_h, start_m).time(),
                key=f"avail_start_{day}", step=600
            )
            end_time = col.time_input(
                "To", value=datetime(2000, 1, 1, end_h, end_m).time(),
                key=f"avail_end_{day}", step=600
            )

            start_mins = time_to_minutes(start_time)
            end_mins = time_to_minutes(end_time)

            if end_mins <= start_mins:
                col.caption("⚠️ End must be after start")
                end_mins = start_mins

            st.session_state.availability[day] = {"start": start_mins, "end": end_mins}

    st.divider()

    # -----------------------------------------------------------------------
    # STUDY SCHEDULE GENERATOR
    # -----------------------------------------------------------------------
    section_card("📆 Generated Study Schedule", "Your planner splits assignment time into available study windows before each due date.")

    if len(st.session_state.tasks) == 0:
        st.markdown(
            """
            <div class="empty-state">
                <b>📆 Nothing to schedule yet.</b><br>
                Add assignments first, then your study blocks will show up here.
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        tasks_to_schedule = [
            t for t in st.session_state.tasks if t.get("status") != "Done"
        ]
        for t in tasks_to_schedule:
            if "minutes" not in t and "hours" in t:
                t["minutes"] = int(t["hours"] * 60)

        tasks_to_schedule.sort(key=lambda x: (
            priority_order.get(x["priority"], 1),
            x["due_date"]
        ))

        day_state = {}
        for i in range(60):
            d = today + timedelta(days=i)
            day_name = d.strftime("%A")
            window = st.session_state.availability.get(day_name, {"start": 0, "end": 0})
            day_state[d] = {
                "cursor": window["start"],
                "end": window["end"],
                "last_block_long": False,
            }

        schedule = {}

        for task in tasks_to_schedule:
            due = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
            mins_left = task["minutes"]

            available_days = sorted([
                d for d in day_state
                if d < due and (day_state[d]["end"] - day_state[d]["cursor"]) >= 10
            ])

            for d in available_days:
                if mins_left <= 0:
                    break

                state = day_state[d]
                cursor = state["cursor"]
                window_end = state["end"]
                free_in_window = window_end - cursor

                if free_in_window < 10:
                    continue

                if state["last_block_long"] and free_in_window >= 25:
                    schedule.setdefault(d, []).append({
                        "name": "☕ Break",
                        "start_min": cursor,
                        "end_min": cursor + 15,
                        "priority": None,
                        "is_break": True,
                    })
                    cursor += 15
                    free_in_window -= 15
                    state["last_block_long"] = False

                if free_in_window < 10:
                    state["cursor"] = cursor
                    continue

                assignable = min(free_in_window, mins_left)
                if assignable < 10:
                    state["cursor"] = cursor
                    continue

                schedule.setdefault(d, []).append({
                    "name": task["name"],
                    "start_min": cursor,
                    "end_min": cursor + assignable,
                    "priority": task["priority"],
                    "is_break": False,
                })

                state["last_block_long"] = assignable > 45
                cursor += assignable
                state["cursor"] = cursor
                mins_left -= assignable

            if mins_left > 0:
                st.warning(
                    f"⚠️ Not enough availability to fully schedule **{task['name']}** "
                    f"before its due date. {fmt_time(mins_left)} couldn't be scheduled."
                )

        sched_month = st.selectbox(
            "Month",
            options=[date(today.year, m, 1).strftime("%B %Y") for m in range(1, 13)],
            index=today.month - 1,
            key="sched_cal_month",
        )
        sched_month_date = datetime.strptime(sched_month, "%B %Y")
        sched_year = sched_month_date.year
        sched_month_num = sched_month_date.month

        sched_by_day = {}
        for d, blocks in schedule.items():
            if d.year == sched_year and d.month == sched_month_num:
                sched_by_day[d.day] = blocks

        cal2 = calendar.monthcalendar(sched_year, sched_month_num)
        cols = st.columns(7)
        for col, day_name in zip(cols, ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
            col.markdown(f"**{day_name}**")

        for week in cal2:
            cols = st.columns(7)
            for col, day in zip(cols, week):
                if day == 0:
                    col.markdown("<div class='calendar-day-muted'></div>", unsafe_allow_html=True)
                elif day in sched_by_day:
                    blocks = sched_by_day[day]
                    task_blocks = [b for b in blocks if not b["is_break"]]
                    total_mins = sum(b["end_min"] - b["start_min"] for b in task_blocks)
                    icons = " ".join(
                        {"Low": "🟢", "Medium": "🟡", "High": "🔴"}.get(b["priority"], "⚪")
                        for b in task_blocks
                    )
                    col.markdown(
                        f"<div class='calendar-day calendar-day-active'><b>{day}</b><br>{icons}<br><em>{fmt_time(total_mins)}</em></div>",
                        unsafe_allow_html=True,
                    )
                else:
                    col.markdown(f"<div class='calendar-day'><b>{day}</b></div>", unsafe_allow_html=True)

        st.write("#### 📝 Daily Schedule")
        sorted_days = sorted(sched_by_day.items())
        if not sorted_days:
            st.markdown(
                """
                <div class="empty-state">
                    <b>🌙 No study sessions scheduled this month.</b><br>
                    Try adding more availability or checking assignments due in this month.
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            for day_num, blocks in sorted_days:
                d = date(sched_year, sched_month_num, day_num)
                st.markdown(f"**{d.strftime('%A, %B %d')}**")
                for block in blocks:
                    start_str = minutes_to_time_str(block["start_min"])
                    end_str = minutes_to_time_str(block["end_min"])
                    duration = block["end_min"] - block["start_min"]
                    if block["is_break"]:
                        st.markdown(
                            f"<div class='daily-block-break'>☕ <b>Break</b> — {start_str} to {end_str}</div>",
                            unsafe_allow_html=True,
                        )
                    else:
                        color = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}.get(block["priority"], "⚪")
                        st.markdown(
                            f"<div class='daily-block'>{color} <b>{block['name']}</b> — {start_str} to {end_str} ({fmt_time(duration)})</div>",
                            unsafe_allow_html=True,
                        )

    st.divider()

    # -----------------------------------------------------------------------
    # STUDY TIMER
    # Pick an assignment, hit Start. The start timestamp is saved to
    # session_state so it survives Streamlit reruns. When you hit Stop,
    # elapsed time is calculated and saved to study_sessions for progress.py.
    # -----------------------------------------------------------------------
    section_card("⏱ Study Timer", "Start a focused study session and save the time into your progress log.")

    # Ensure timer state keys exist
    if "timer_running" not in st.session_state:
        st.session_state.timer_running = False
    if "timer_start" not in st.session_state:
        st.session_state.timer_start = None
    if "timer_subject" not in st.session_state:
        st.session_state.timer_subject = None

    # Build subject list from tasks — fall back to a free-text option
    task_names = [t["name"] for t in st.session_state.tasks] if st.session_state.tasks else []
    subject_options = task_names + ["Other (type below)"]

    if not st.session_state.timer_running:
        # ----- TIMER NOT RUNNING — show setup -----
        selected_subject = st.selectbox(
            "What are you studying?",
            options=subject_options,
            key="timer_subject_select",
        )

        # If "Other" is chosen, show a text input for a custom subject name
        if selected_subject == "Other (type below)":
            custom_subject = st.text_input("Subject name", placeholder="e.g. Chemistry")
            subject_to_use = custom_subject.strip() if custom_subject.strip() else "Other"
        else:
            subject_to_use = selected_subject

        if st.button("▶️ Start Timer", type="primary"):
            st.session_state.timer_running = True
            st.session_state.timer_start = datetime.now().timestamp()  # Unix timestamp survives reruns
            st.session_state.timer_subject = subject_to_use
            st.rerun()

    else:
        # ----- TIMER IS RUNNING — show elapsed time and stop button -----
        elapsed_seconds = datetime.now().timestamp() - st.session_state.timer_start
        elapsed_minutes = elapsed_seconds / 60

        elapsed_h = int(elapsed_seconds // 3600)
        elapsed_m = int((elapsed_seconds % 3600) // 60)
        elapsed_s = int(elapsed_seconds % 60)

        st.info(
            f"⏳ Studying **{st.session_state.timer_subject}**  \n"
            f"Elapsed: **{elapsed_h:02d}:{elapsed_m:02d}:{elapsed_s:02d}**"
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("⏹ Stop & Save", type="primary"):
                # Only save if at least 1 minute has passed
                rounded_minutes = max(1, round(elapsed_minutes))

                st.session_state.study_sessions.append({
                    "subject": st.session_state.timer_subject,
                    "minutes": rounded_minutes,
                    "date": date.today().strftime("%Y-%m-%d"),
                })

                saved_subject = st.session_state.timer_subject

                # Clear timer state
                st.session_state.timer_running = False
                st.session_state.timer_start = None
                st.session_state.timer_subject = None

                st.success(f"✅ Saved {fmt_time(rounded_minutes)} of studying **{saved_subject}**!")
                st.rerun()

        with col2:
            if st.button("🗑 Discard"):
                # Stop without saving
                st.session_state.timer_running = False
                st.session_state.timer_start = None
                st.session_state.timer_subject = None
                st.rerun()

        # Auto-refresh every 5 seconds so the elapsed time updates visually
        time.sleep(1)
        st.rerun()

    # -----------------------------------------------------------------------
    # STUDY SESSION LOG
    # Shows all logged sessions so the user can see their history
    # and manually delete any bad entries.
    # -----------------------------------------------------------------------
    if st.session_state.study_sessions:
        st.write("#### 📋 Session Log")
        for i, session in enumerate(reversed(st.session_state.study_sessions)):
            idx = len(st.session_state.study_sessions) - 1 - i  # real index for deletion
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(
                    f"<div class='daily-block'>📖 <b>{session['subject']}</b> — {fmt_time(session['minutes'])} on {session['date']}</div>",
                    unsafe_allow_html=True,
                )
            with col2:
                if st.button("🗑", key=f"del_session_{idx}"):
                    st.session_state.study_sessions.pop(idx)
                    st.rerun()

    apply_settings()
