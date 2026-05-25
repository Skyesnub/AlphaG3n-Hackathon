import streamlit as st
from supabase import create_client


SAVE_KEYS = [
    "tasks",
    "study_sessions",
    "flashcards",
    "know_flashcards",
    "review_flashcards",
    "quizzes",
    "total_quiz_scores",
    "cur_quiz_scores",
    "card_accuracy",
    "availability",
    "background",
    "flashcard_idx",
    "quiz_idx",
]

TUPLE_LIST_KEYS = {
    "flashcards",
    "know_flashcards",
    "review_flashcards",
    "quizzes",
}


def get_supabase():
    if "supabase_client" not in st.session_state:
        st.session_state.supabase_client = create_client(
            st.secrets["SUPABASE_URL"],
            st.secrets["SUPABASE_ANON_KEY"],
        )
    return st.session_state.supabase_client


def normalize_loaded_value(key, value):
    if key in TUPLE_LIST_KEYS:
        return [tuple(item) for item in value]
    return value


def current_user():
    return st.session_state.get("user")


def load_progress():
    user = current_user()
    if not user:
        return

    result = (
        get_supabase()
        .table("app_state")
        .select("data")
        .eq("user_id", user.id)
        .execute()
    )

    if not result.data:
        return

    saved_data = result.data[0].get("data") or {}
    for key, value in saved_data.items():
        st.session_state[key] = normalize_loaded_value(key, value)

    st.session_state.progress_loaded = True


def save_progress():
    user = current_user()
    if not user:
        return

    data = {
        key: st.session_state.get(key)
        for key in SAVE_KEYS
        if key in st.session_state
    }

    get_supabase().table("app_state").upsert(
        {
            "user_id": user.id,
            "data": data,
        }
    ).execute()


def show_auth_sidebar():
    supabase = get_supabase()

    if "user" not in st.session_state:
        st.session_state.user = None

    st.sidebar.divider()

    if st.session_state.user:
        st.sidebar.caption(f"Signed in as {st.session_state.user.email}")
        if st.sidebar.button("Log out"):
            supabase.auth.sign_out()
            st.session_state.user = None
            st.session_state.progress_loaded = False
            st.rerun()
        return True

    st.sidebar.subheader("Account")
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")

    login_col, signup_col = st.sidebar.columns(2)

    with login_col:
        if st.button("Log in"):
            if not email or not password:
                st.sidebar.error("Enter your email and password.")
            else:
                try:
                    response = supabase.auth.sign_in_with_password(
                        {"email": email, "password": password}
                    )
                    st.session_state.user = response.user
                    load_progress()
                    st.rerun()
                except Exception as exc:
                    st.sidebar.error(f"Login failed: {exc}")

    with signup_col:
        if st.button("Sign up"):
            if not email or not password:
                st.sidebar.error("Enter your email and password.")
            else:
                try:
                    response = supabase.auth.sign_up(
                        {"email": email, "password": password}
                    )
                    if response.session:
                        st.session_state.user = response.user
                        save_progress()
                        st.rerun()
                    else:
                        st.sidebar.success("Check your email to confirm your account.")
                except Exception as exc:
                    st.sidebar.error(f"Signup failed: {exc}")

    return False
