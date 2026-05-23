import streamlit as st
from datetime import date, datetime, timedelta
from tabs.settings import apply_settings
import calendar


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


def run_planner():
    st.title("📅 Planner")
    st.write("Add assignments and view them on a calendar.")

    # -----------------------------------------------------------------------
    # ADD TASK FORM
    # -----------------------------------------------------------------------
    st.subheader("➕ Add Assignment")

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
    st.subheader("📋 Assignments")

    if len(st.session_state.tasks) == 0:
        st.info("No assignments yet. Add one above!")
    else:
        sorted_tasks = sorted(st.session_state.tasks, key=lambda x: x["due_date"])

        for i, task in enumerate(sorted_tasks):
            if "minutes" not in task and "hours" in task:
                task["minutes"] = int(task["hours"] * 60)

            color = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}.get(task["priority"], "⚪")
            due = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
            days_left = (due - date.today()).days

            if days_left < 0:
                urgency = "⚠️ Overdue"
            elif days_left == 0:
                urgency = "⚠️ Due today"
            elif days_left == 1:
                urgency = "Due tomorrow"
            else:
                urgency = f"Due in {days_left} days"

            with st.expander(f"{color} {task['name']} — {task['due_date']} ({urgency})"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"⏱ **Time:** {fmt_time(task['minutes'])}")
                with col2:
                    st.write(f"📌 **Priority:** {task['priority']}")
                with col3:
                    new_status = st.selectbox(
                        "Status",
                        ["To Do", "In Progress", "Done"],
                        index=["To Do", "In Progress", "Done"].index(task.get("status", "To Do")),
                        key=f"status_{i}_{task['name']}",
                    )
                    for t in st.session_state.tasks:
                        if t["name"] == task["name"] and t["due_date"] == task["due_date"]:
                            t["status"] = new_status

                if st.button("🗑 Delete", key=f"delete_{i}_{task['name']}"):
                    st.session_state.tasks = [
                        t for t in st.session_state.tasks
                        if not (t["name"] == task["name"] and t["due_date"] == task["due_date"])
                    ]
                    st.rerun()

    st.divider()

    # -----------------------------------------------------------------------
    # CALENDAR VIEW — due dates
    # -----------------------------------------------------------------------
    st.subheader("🗓 Due Date Calendar")

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
                col.write("")
            elif day in tasks_by_day:
                icons = " ".join(
                    {"Low": "🟢", "Medium": "🟡", "High": "🔴"}.get(t["priority"], "⚪")
                    for t in tasks_by_day[day]
                )
                col.markdown(f"**{day}**  \n{icons}")
            else:
                col.write(str(day))

    st.divider()

    # -----------------------------------------------------------------------
    # AVAILABILITY INPUT — free window per day (start time to end time)
    # Stored in session_state as {day: {"start": minutes, "end": minutes}}
    # -----------------------------------------------------------------------
    st.subheader("⏰ Your Daily Availability")
    st.write("Set the time window you're free to study each day.")

    # Default: 4 PM to 8 PM on weekdays, 10 AM to 6 PM on weekends
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

    # Show 7 columns, one per day
    cols = st.columns(7)
    for col, day in zip(cols, days_of_week):
        with col:
            col.markdown(f"**{day[:3]}**")

            current = st.session_state.availability.get(day, {"start": 16 * 60, "end": 20 * 60})

            # Convert stored minutes-since-midnight back to a time object for the widget
            start_h, start_m = divmod(current["start"], 60)
            end_h, end_m = divmod(current["end"], 60)

            start_time = col.time_input(
                "From", value=datetime(2000, 1, 1, start_h, start_m).time(),
                key=f"avail_start_{day}", step=600  # 10 min steps
            )
            end_time = col.time_input(
                "To", value=datetime(2000, 1, 1, end_h, end_m).time(),
                key=f"avail_end_{day}", step=600
            )

            start_mins = time_to_minutes(start_time)
            end_mins = time_to_minutes(end_time)

            # Make sure end is after start
            if end_mins <= start_mins:
                col.caption("⚠️ End must be after start")
                end_mins = start_mins  # treat as 0 free time

            st.session_state.availability[day] = {"start": start_mins, "end": end_mins}

    st.divider()

    # -----------------------------------------------------------------------
    # STUDY SCHEDULE GENERATOR
    # Places tasks into the free window each day, adding 15 min breaks
    # between assignments longer than 45 minutes.
    # Shows exact start/end times for each block.
    # -----------------------------------------------------------------------
    st.subheader("📆 Generated Study Schedule")

    if len(st.session_state.tasks) == 0:
        st.info("Add assignments above to generate a schedule.")
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

        # For each day in the next 60 days, track a "cursor" = next available
        # minute within the free window.
        # day_state[date] = {"cursor": minutes_since_midnight, "end": minutes_since_midnight}
        day_state = {}
        for i in range(60):
            d = today + timedelta(days=i)
            day_name = d.strftime("%A")
            window = st.session_state.availability.get(day_name, {"start": 0, "end": 0})
            day_state[d] = {
                "cursor": window["start"],
                "end": window["end"],
                # track whether the previous block on this day was >45 min
                # so we know to insert a break
                "last_block_long": False,
            }

        # schedule[date] = list of {name, start_min, end_min, priority, is_break}
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

                # Insert a 15 min break if the previous block on this day was >45 min
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

                # How much of this task can we fit today?
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

                # Mark if this block was long (>45 min) so next task gets a break
                state["last_block_long"] = assignable > 45

                cursor += assignable
                state["cursor"] = cursor
                mins_left -= assignable

            if mins_left > 0:
                st.warning(
                    f"⚠️ Not enough availability to fully schedule **{task['name']}** "
                    f"before its due date. {fmt_time(mins_left)} couldn't be scheduled."
                )

        # -----------------------------------------------------------------------
        # DISPLAY SCHEDULE CALENDAR
        # -----------------------------------------------------------------------
        sched_month = st.selectbox(
            "Month",
            options=[date(today.year, m, 1).strftime("%B %Y") for m in range(1, 13)],
            index=today.month - 1,
            key="sched_cal_month",
        )
        sched_month_date = datetime.strptime(sched_month, "%B %Y")
        sched_year = sched_month_date.year
        sched_month_num = sched_month_date.month

        # Filter to selected month, exclude breaks from calendar dots
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
                    col.write("")
                elif day in sched_by_day:
                    blocks = sched_by_day[day]
                    task_blocks = [b for b in blocks if not b["is_break"]]
                    total_mins = sum(b["end_min"] - b["start_min"] for b in task_blocks)
                    icons = " ".join(
                        {"Low": "🟢", "Medium": "🟡", "High": "🔴"}.get(b["priority"], "⚪")
                        for b in task_blocks
                    )
                    col.markdown(f"**{day}**  \n{icons}  \n_{fmt_time(total_mins)}_")
                else:
                    col.write(str(day))

        # -----------------------------------------------------------------------
        # DETAILED DAILY BREAKDOWN WITH TIMES
        # -----------------------------------------------------------------------
        st.write("#### 📝 Daily Schedule")
        sorted_days = sorted(sched_by_day.items())
        if not sorted_days:
            st.info("No study sessions scheduled this month.")
        else:
            for day_num, blocks in sorted_days:
                d = date(sched_year, sched_month_num, day_num)
                st.markdown(f"**{d.strftime('%A, %B %d')}**")
                for block in blocks:
                    start_str = minutes_to_time_str(block["start_min"])
                    end_str = minutes_to_time_str(block["end_min"])
                    duration = block["end_min"] - block["start_min"]
                    if block["is_break"]:
                        st.write(f"  ☕ Break — {start_str} to {end_str}")
                    else:
                        color = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}.get(block["priority"], "⚪")
                        st.write(f"  {color} {block['name']} — {start_str} to {end_str} ({fmt_time(duration)})")

    apply_settings()