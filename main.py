import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Productivity Hub",
    page_icon="🚀",
    layout="wide"
)

# ---------------- SIDEBAR ----------------
st.sidebar.title("📂 Navigation")

mode = st.sidebar.radio(
    "Choose a mode:",
    [
        "Home",
        "Schedule Maker",
        "Music Chooser",
        "Study Tracker",
        "Settings"
    ]
)

st.sidebar.markdown("---")
st.sidebar.write("Built with Streamlit 😎")

# ---------------- HOME PAGE ----------------
if mode == "Home":

    st.title("My First Streamlit Website 🚀")

    st.write("Hello! This is my first Python-powered website.")

    name = st.text_input("What's your name?")

    if name:
        st.write(f"Hi {name}! Welcome to my app 😎")

    mood = st.slider(
        "How productive are you feeling today?",
        1,
        10,
        5
    )

    st.write(f"Productivity level: {mood}/10")

    if st.button("Generate study advice"):
        if mood <= 3:
            st.write(
                "Start with a tiny 10-minute task. Momentum first, perfection later."
            )
        elif mood <= 7:
            st.write(
                "Do a 25-minute focus session, then take a 5-minute break."
            )
        else:
            st.write(
                "You're locked in. Do your hardest task first while your brain is cracked."
            )

# ---------------- SCHEDULE MAKER ----------------
elif mode == "Schedule Maker":

    st.title("📅 Schedule Maker")

    st.subheader("Create Your Daily Plan")

    task_name = st.text_input("Task Name")

    col1, col2 = st.columns(2)

    with col1:
        start_time = st.time_input("Start Time")

    with col2:
        end_time = st.time_input("End Time")

    priority = st.selectbox(
        "Priority",
        ["Low", "Medium", "High"]
    )

    if st.button("Add Task"):
        st.success(
            f"Added task: {task_name} ({priority} priority)"
        )

    st.markdown("---")

    st.subheader("Today's Schedule")

    st.info("📝 Placeholder schedule list")

    st.write("""
    - 8:00 AM → Math Homework  
    - 10:00 AM → Coding Practice  
    - 1:00 PM → Gym  
    - 4:00 PM → Study Session  
    """)

# ---------------- MUSIC CHOOSER ----------------
elif mode == "Music Chooser":

    st.title("🎵 Music Chooser")

    st.subheader("Pick a Study Vibe")

    genre = st.selectbox(
        "Select Genre",
        [
            "Lo-fi",
            "Classical",
            "Synthwave",
            "Jazz",
            "Game Soundtracks"
        ]
    )

    energy = st.slider(
        "Energy Level",
        1,
        10,
        5
    )

    if st.button("Generate Playlist"):
        st.success(
            f"Generating a {genre} playlist with energy level {energy} 🔥"
        )

    st.markdown("---")

    st.subheader("Suggested Songs")

    st.write("""
    🎧 Placeholder Song 1  
    🎧 Placeholder Song 2  
    🎧 Placeholder Song 3  
    """)

# ---------------- STUDY TRACKER ----------------
elif mode == "Study Tracker":

    st.title("📚 Study Tracker")

    st.subheader("Track Your Progress")

    subject = st.selectbox(
        "Subject",
        [
            "Math",
            "Science",
            "History",
            "Programming",
            "English"
        ]
    )

    hours = st.slider(
        "Hours Studied",
        0,
        12,
        2
    )

    if st.button("Save Progress"):
        st.success(
            f"Logged {hours} hours for {subject}"
        )

    st.progress(hours / 12)

# ---------------- SETTINGS ----------------
elif mode == "Settings":

    st.title("⚙️ Settings")

    dark_mode = st.toggle("Enable Dark Mode")

    notifications = st.checkbox(
        "Enable Notifications"
    )

    username = st.text_input("Change Username")

    if st.button("Save Settings"):
        st.success("Settings saved successfully!")