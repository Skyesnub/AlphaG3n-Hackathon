import streamlit as st
import re
import random
from tabs.settings import apply_settings
from tabs.extract import extract_pairs_from_notes
import math
'''
Study Tools

Input:
-takes in user copy-pasted prompt
-looks for patterns such as __ is __ or __ : __, stopping section at '.', '\n'

Flashcards:
-states
    -flashcards -> list of tuples, tuple = (question, answer), dtype = string for both
    -know_flashcards -> same data structure as flashcards, cumulative
    -review_flashcards -> same data structure as flashcards, cumulative
    -flashcard_idx -> which index flashcard you are on, int
-functions
    -toggle show or not show answer
    -left/right buttons on which flashcard you're on
    -generate 1-50 flashcards based on user input
    -if not enough info, repeat flashcards to user specified requirement
    -show current flashcard accuracy (can be toggled to be cleared)
    -can mark as 'know' or 'review'

Quizzes:
-states
    -quizzes -> list of tuples, tuple = (question, answer), dtype = string for both
        -can create free response or multiple choice from these depending on user input
    -total_quiz_scores -> list of 0/1, wrong/right (can also be cleared using separate button)
    -cur_quiz_scores -> list of 0/1, can be cleared by user after each quiz session
-function
    -user can either generate multiple choice or free response, 1-50 quiz questions
    -if not enough info, repeat questions to user specified requirement
    -each question has submit option, right/wrong, add accuracy to current quiz + total quiz score
    -show current quiz accuracy
    
    
Review:
-display every single quiz question generated (remove repeats this time)
-can also display flashcards, which ones are reviewing/know
-can delete + add quiz/flashcard questions

'''


def apply_study_tools_styles():
    st.markdown(
        """
        <style>
            /*
            Study Tools keeps the same pretty layout,
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
                margin-top: 0.8rem;
                margin-bottom: 0.75rem;
                font-weight: 800;
                font-size: 1.35rem;
                color: var(--accent-color);
            }

            div[data-testid="stTextArea"] textarea,
            div[data-testid="stTextInput"] input {
                border-radius: 16px;
                border: 1px solid var(--border-color);
                box-shadow: 0 8px 22px rgba(15, 23, 42, 0.05);
                color: var(--text-color);
            }

            div[data-testid="stSlider"] {
                padding: 0.25rem 0.15rem 0.6rem 0.15rem;
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

            button[data-baseweb="tab"] {
                border-radius: 999px;
                padding: 0.45rem 1rem;
                font-weight: 700;
            }

            details {
                border-radius: 18px !important;
                background: var(--card-bg) !important;
                border: 1px solid var(--border-color) !important;
                box-shadow: 0 8px 22px rgba(15, 23, 42, 0.04);
            }

            hr {
                margin: 1.7rem 0;
                border-color: var(--border-color);
            }

            .stat-card {
                padding: 1rem;
                border-radius: 22px;
                background: var(--card-bg);
                border: 1px solid var(--border-color);
                box-shadow: 0 10px 28px rgba(15, 23, 42, 0.06);
            }

            .stat-card .label {
                color: var(--muted-color);
                font-size: 0.85rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.04em;
            }

            .stat-card .value {
                color: var(--text-color);
                font-size: 1.45rem;
                font-weight: 900;
                margin-top: 0.2rem;
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
        unsafe_allow_html=True
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
        unsafe_allow_html=True
    )


def run_study_tools():
    apply_settings()
    apply_study_tools_styles()

    st.markdown(
        '''
        <div class="study-hero">
            <h1>🧠 Study Tools</h1>
            <p>Paste notes, generate flashcards/quizzes, and track what you know.</p>
        </div>
        ''',
        unsafe_allow_html=True
    )

    #initialization
    defaults = {
        # Flashcards
        "flashcards": [],
        "know_flashcards": [],
        "review_flashcards": [],
        "flashcard_idx": 0,
        "show_flashcard_answer": False,

        # Quizzes
        "quizzes": [],
        "total_quiz_scores": [],
        "cur_quiz_scores": [],
        "quiz_idx": 0,
        "quiz_answer_submitted": False,
        "last_quiz_correct": None,

        # Review add forms
        "new_flashcard_question": "",
        "new_flashcard_answer": "",
        "new_quiz_question": "",
        "new_quiz_answer": "",
    }


    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    ##################################################
    '''*************** HELPER FUNCTIONS ******************'''
    ##################################################

    def repeat_to_amount(items, amount):
        """
        If there are not enough generated items,
        repeat them until reaching the requested amount.
        """
        if len(items) == 0:
            return []

        result = []
        while len(result) < amount:
            for item in items:
                result.append(item)
                if len(result) == amount:
                    break

        return result

    def get_accuracy(scores):
        if len(scores) == 0:
            return "N/A"

        return round((sum(scores) / len(scores)) * 100, 1)

    def remove_duplicates(items):
        seen = set()
        result = []

        for item in items:
            if item not in seen:
                seen.add(item)
                result.append(item)

        return result

    def make_multiple_choice_options(correct_answer):
        all_answers = [answer for question, answer in st.session_state.quizzes]
        wrong_answers = []

        for answer in all_answers:
            if answer != correct_answer and answer not in wrong_answers:
                wrong_answers.append(answer)

        random.shuffle(wrong_answers)

        options = wrong_answers[:3]

        while len(options) < 3:
            options.append("None of these")

        options.append(correct_answer)
        random.shuffle(options)

        return options

    ##################################################
    '''*************** INPUTS ******************'''
    ##################################################
    section_header("📥 Paste Notes")

    notes = st.text_area(
        "Copy-paste your notes here:",
        height=220,
        placeholder=(
            "Example:\n"
            "Photosynthesis: the process plants use to convert sunlight into energy.\n"
            "Mitochondria is the powerhouse of the cell.\n"
            "Osmosis = movement of water across a membrane."
        )
    )

    # print(notes)
    # print(type(notes))

    extracted_pairs = extract_pairs_from_notes(notes)
    
    percent_used = st.slider(
    "How selective should AI be?",
    min_value=10,
    max_value=100,
    value=70,
    step=5,
    help="Lower percentages only use the most important flashcards. Higher percentages include more flashcards."
    )
    num_to_use = math.ceil(len(extracted_pairs) * percent_used / 100)
    extracted_pairs = extracted_pairs[:num_to_use]
    
    if notes.strip():
        st.caption(f"Detected {len(extracted_pairs)} possible study items from your notes.")

    stat_col1, stat_col2, stat_col3 = st.columns(3)
    with stat_col1:
        stat_card("Detected items", len(extracted_pairs))
    with stat_col2:
        stat_card("Flashcards saved", len(st.session_state.flashcards))
    with stat_col3:
        stat_card("Quiz questions saved", len(st.session_state.quizzes))

    st.divider()

    ##################################################
    '''*************** FLASHCARDS ******************'''
    ##################################################
    
    section_header("🃏 Flashcards")

    flashcard_amount = st.slider(
        "How many flashcards do you want?",
        min_value=1,
        max_value=50,
        value=10,
        key="flashcard_amount_slider"
    )

    if st.button("✨ Generate Flashcards", use_container_width=True):
        if not notes.strip():
            st.warning("Paste notes first.")
        elif len(extracted_pairs) == 0:
            st.warning("I couldn't find patterns like `term is definition` or `term: definition`.")
        else:
            generated = repeat_to_amount(extracted_pairs, flashcard_amount)

            for gen in generated:
                st.session_state.flashcards.append(gen)
            st.session_state.flashcard_idx = 0
            st.session_state.show_flashcard_answer = False
            st.session_state.cur_flashcard_scores = []

            st.success(f"Generated {len(generated)} flashcards!")

    if len(st.session_state.flashcards) > 0:
        idx = st.session_state.flashcard_idx

        if idx >= len(st.session_state.flashcards):
            st.session_state.flashcard_idx = 0
            idx = 0

        question, answer = st.session_state.flashcards[idx]

        st.write(f"Flashcard **{idx + 1}** of **{len(st.session_state.flashcards)}**")
        st.info(question)

        if st.button("👀 Show / Hide Answer"):
            st.session_state.show_flashcard_answer = not st.session_state.show_flashcard_answer
            st.rerun()

        if st.session_state.show_flashcard_answer:
            st.success(answer)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("⬅️ Left"):
                if st.session_state.flashcard_idx > 0:
                    st.session_state.flashcard_idx -= 1
                st.session_state.show_flashcard_answer = False
                st.rerun()

        with col2:
            if st.button("➡️ Right"):
                if st.session_state.flashcard_idx < len(st.session_state.flashcards) - 1:
                    st.session_state.flashcard_idx += 1
                st.session_state.show_flashcard_answer = False
                st.rerun()

        with col3:
            if st.button("✅ Know"):
                card = (question, answer)
                if card not in st.session_state.know_flashcards:
                    st.session_state.know_flashcards.append(card)

                if card in st.session_state.review_flashcards:
                    st.session_state.review_flashcards.remove(card)

                if st.session_state.flashcard_idx < len(st.session_state.flashcards) - 1:
                    st.session_state.flashcard_idx += 1

                st.session_state.show_flashcard_answer = False
                st.rerun()

        with col4:
            if st.button("🔁 Review"):
                card = (question, answer)
                if card not in st.session_state.review_flashcards:
                    st.session_state.review_flashcards.append(card)

                if card in st.session_state.know_flashcards:
                    st.session_state.know_flashcards.remove(card)

                if st.session_state.flashcard_idx < len(st.session_state.flashcards) - 1:
                    st.session_state.flashcard_idx += 1

                st.session_state.show_flashcard_answer = False
                st.rerun()

    else:
        st.info("No flashcards generated yet.")

    st.divider()

    ##################################################
    '''*************** QUIZZES ******************'''
    ##################################################
    
    section_header("📝 Quizzes")

    quiz_amount = st.slider(
        "How many quiz questions do you want?",
        min_value=1,
        max_value=50,
        value=10,
        key="quiz_amount_slider"
    )

    quiz_mode = st.radio(
        "Quiz type:",
        ["Free Response", "Multiple Choice"],
        horizontal=True
    )

    if st.button("🧪 Generate Quiz", use_container_width=True):
        if not notes.strip():
            st.warning("Paste notes first.")
        elif len(extracted_pairs) == 0:
            st.warning("I couldn't find patterns like `term is definition` or `term: definition`.")
        else:
            generated = repeat_to_amount(extracted_pairs, quiz_amount)

            for gen in generated:
                st.session_state.quizzes.append(gen)
            st.session_state.quiz_idx = 0
            st.session_state.cur_quiz_scores = []
            st.session_state.quiz_answer_submitted = False
            st.session_state.last_quiz_correct = None

            st.success(f"Generated {len(generated)} quiz questions!")

    if len(st.session_state.quizzes) > 0:
        idx = st.session_state.quiz_idx

        if idx >= len(st.session_state.quizzes):
            st.success("Quiz finished!")

            cur_quiz_acc = get_accuracy(st.session_state.cur_quiz_scores)
            st.write(f"Final current quiz accuracy: **{cur_quiz_acc}%**" if cur_quiz_acc != "N/A" else "Final current quiz accuracy: **N/A**")

            if st.button("🔁 Restart Quiz"):
                st.session_state.quiz_idx = 0
                st.session_state.cur_quiz_scores = []
                st.session_state.quiz_answer_submitted = False
                st.session_state.last_quiz_correct = None
                st.rerun()

        else:
            st.write(f"Question **{idx + 1}** of **{len(st.session_state.quizzes)}**")
            user_answer = ""

            if quiz_mode == "Free Response":
                answer, question = st.session_state.quizzes[idx]
                st.info(question)
                user_answer = st.text_input("Your answer:", key=f"free_response_{idx}")

            else:
                question, answer = st.session_state.quizzes[idx]
                st.info(question)
                option_key = f"multiple_choice_options_{idx}"

                if option_key not in st.session_state:
                    st.session_state[option_key] = make_multiple_choice_options(answer)

                options = st.session_state[option_key]

                user_answer = st.radio(
                    "Choose one:",
                    options,
                    key=f"multiple_choice_{idx}"
                )

            if not st.session_state.quiz_answer_submitted:
                if st.button("✅ Submit Answer"):
                    is_correct = user_answer.strip().lower() == answer.strip().lower()

                    if is_correct:
                        st.session_state.cur_quiz_scores.append(1)
                        st.session_state.total_quiz_scores.append(1)
                        st.session_state.last_quiz_correct = True
                    else:
                        st.session_state.cur_quiz_scores.append(0)
                        st.session_state.total_quiz_scores.append(0)
                        st.session_state.last_quiz_correct = False

                    st.session_state.quiz_answer_submitted = True
                    st.rerun()

            else:
                if st.session_state.last_quiz_correct:
                    st.success("Correct!")
                else:
                    st.error(f"Not quite. Correct answer: {answer}")

                if st.button("➡️ Next Question"):
                    st.session_state.quiz_idx += 1
                    st.session_state.quiz_answer_submitted = False
                    st.session_state.last_quiz_correct = None
                    st.rerun()

        cur_quiz_acc = get_accuracy(st.session_state.cur_quiz_scores)
        total_quiz_acc = get_accuracy(st.session_state.total_quiz_scores)

        st.write(f"Current quiz accuracy: **{cur_quiz_acc}%**" if cur_quiz_acc != "N/A" else "Current quiz accuracy: **N/A**")
        st.write(f"Total quiz accuracy: **{total_quiz_acc}%**" if total_quiz_acc != "N/A" else "Total quiz accuracy: **N/A**")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🧹 Clear Current Quiz Scores"):
                st.session_state.cur_quiz_scores = []
                st.rerun()

        with col2:
            if st.button("🗑️ Clear Total Quiz Scores"):
                st.session_state.total_quiz_scores = []
                st.rerun()

    else:
        st.info("No quiz generated yet.")

    st.divider()

    ##################################################
    '''*************** REVIEW ******************'''
    ##################################################
    section_header("📚 Review All Generated Items")

    tab1, tab2, tab3 = st.tabs(["All Flashcards", "Know / Review", "All Quiz Questions"])

    # -----------------------------
    # All flashcards
    # -----------------------------
    with tab1:
        st.write("Flashcards shown here remove repeated generated items.")

        unique_flashcards = remove_duplicates(st.session_state.flashcards)

        if len(unique_flashcards) == 0:
            st.info("No flashcards to review.")
        else:
            for i, card in enumerate(unique_flashcards):
                question, answer = card

                with st.expander(f"Flashcard {i + 1}: {question}"):
                    st.write(f"**Answer:** {answer}")

                    if st.button("Delete Flashcard", key=f"delete_flashcard_{i}"):
                        st.session_state.flashcards = [
                            item for item in st.session_state.flashcards
                            if item != card
                        ]

                        if card in st.session_state.know_flashcards:
                            st.session_state.know_flashcards.remove(card)

                        if card in st.session_state.review_flashcards:
                            st.session_state.review_flashcards.remove(card)

                        st.rerun()

        st.subheader("➕ Add Flashcard")

        new_q = st.text_input("New flashcard question:", key="add_flashcard_q")
        new_a = st.text_input("New flashcard answer:", key="add_flashcard_a")

        if st.button("Add Flashcard"):
            if new_q.strip() and new_a.strip():
                st.session_state.flashcards.append((new_q.strip(), new_a.strip()))
                st.success("Flashcard added!")
                st.rerun()
            else:
                st.warning("Add both a question and an answer.")



    # -----------------------------
    # Know / Review flashcards
    # -----------------------------
    with tab2:
        st.write("Cards you marked as known or needing review.")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("✅ Know")

            unique_know = remove_duplicates(st.session_state.know_flashcards)

            if len(unique_know) == 0:
                st.info("No known flashcards yet.")
            else:
                for i, card in enumerate(unique_know):
                    q, a = card
                    st.write(f"**{q}**")
                    st.caption(a)

                    if st.button("Move to Review", key=f"know_to_review_{i}"):
                        if card in st.session_state.know_flashcards:
                            st.session_state.know_flashcards.remove(card)

                        if card not in st.session_state.review_flashcards:
                            st.session_state.review_flashcards.append(card)

                        st.rerun()

        with col2:
            st.subheader("⭐ Review")

            unique_review = remove_duplicates(st.session_state.review_flashcards)

            if len(unique_review) == 0:
                st.info("No review flashcards yet.")
            else:
                for i, card in enumerate(unique_review):
                    q, a = card
                    st.write(f"**{q}**")
                    st.caption(a)

                    if st.button("Move to Know", key=f"review_to_know_{i}"):
                        if card in st.session_state.review_flashcards:
                            st.session_state.review_flashcards.remove(card)

                        if card not in st.session_state.know_flashcards:
                            st.session_state.know_flashcards.append(card)

                        st.rerun()

    # -----------------------------
    # All quiz questions
    # -----------------------------
    with tab3:
        st.write("Quiz questions shown here remove repeated generated items.")

        unique_quizzes = remove_duplicates(st.session_state.quizzes)

        if len(unique_quizzes) == 0:
            st.info("No quiz questions to review.")
        else:
            for i, quiz in enumerate(unique_quizzes):
                question, answer = quiz

                with st.expander(f"Quiz Question {i + 1}: {question}"):
                    st.write(f"**Answer:** {answer}")

                    if st.button("Delete Quiz Question", key=f"delete_quiz_{i}"):
                        st.session_state.quizzes = [
                            item for item in st.session_state.quizzes
                            if item != quiz
                        ]
                        st.rerun()

        st.subheader("➕ Add Quiz Question")

        new_q = st.text_input("New quiz question:", key="add_quiz_q")
        new_a = st.text_input("New quiz answer:", key="add_quiz_a")

        if st.button("Add Quiz Question"):
            if new_q.strip() and new_a.strip():
                st.session_state.quizzes.append((new_q.strip(), new_a.strip()))
                st.success("Quiz question added!")
                st.rerun()
            else:
                st.warning("Add both a question and an answer.")