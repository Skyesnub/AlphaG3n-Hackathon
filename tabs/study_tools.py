import streamlit as st
import re
import random

'''
Study Tools:



'''




from tabs.settings import apply_settings

def run_study_tools():
    apply_settings()

    st.title("🧠 Study Tools")
    st.write("Paste notes, generate flashcards or quizzes, and review your accuracy.")

    # -----------------------------
    # Safety: make sure state exists
    # -----------------------------
    if "flashcards" not in st.session_state:
        st.session_state.flashcards = []

    if "quizzes" not in st.session_state:
        st.session_state.quizzes = []

    if "quiz_scores" not in st.session_state:
        st.session_state.quiz_scores = []

    if "card_accuracy" not in st.session_state:
        st.session_state.card_accuracy = {}

    if "current_card_index" not in st.session_state:
        st.session_state.current_card_index = 0

    if "show_card_answer" not in st.session_state:
        st.session_state.show_card_answer = False

    if "current_quiz_index" not in st.session_state:
        st.session_state.current_quiz_index = 0

    if "current_quiz_score" not in st.session_state:
        st.session_state.current_quiz_score = 0

    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False

    if "quiz_answered" not in st.session_state:
        st.session_state.quiz_answered = False

    if "last_quiz_result" not in st.session_state:
        st.session_state.last_quiz_result = None

    # -----------------------------
    # Helper functions
    # -----------------------------
    def clean_text(text):
        text = text.strip()
        text = re.sub(r"\s+", " ", text)
        return text

    def split_notes(notes):
        """
        Splits notes by line breaks or sentence endings.
        Allows formats like:
        Photosynthesis: process plants use sunlight...
        Mitochondria is the powerhouse of the cell.
        Hypothesis = a testable explanation.
        """
        chunks = re.split(r"\n+|(?<=[.!?])\s+", notes)
        cleaned = []

        for chunk in chunks:
            chunk = clean_text(chunk)
            if len(chunk) > 5:
                cleaned.append(chunk)

        return cleaned

    def make_hint(answer):
        """
        Gives a small hint without fully revealing the answer.
        """
        answer = answer.strip()

        if len(answer) <= 3:
            return f"It starts with '{answer[0]}'." if answer else "No hint available."

        words = answer.split()

        if len(words) == 1:
            return f"It starts with '{answer[0]}' and has {len(answer)} letters."

        return f"It starts with '{words[0][0]}' and has {len(words)} words."

    def generate_flashcards_from_notes(notes, amount):
        flashcards = []
        chunks = split_notes(notes)

        patterns = [
            r"^(.+?)\s*:\s*(.+)$",
            r"^(.+?)\s*-\s*(.+)$",
            r"^(.+?)\s*=\s*(.+)$",
            r"^(.+?) is defined as (.+)$",
            r"^(.+?) is (.+)$",
            r"^(.+?) are (.+)$",
            r"^(.+?) means (.+)$",
            r"^(.+?) refers to (.+)$",
            r"^(.+?) consists of (.+)$",
            r"^(.+?) contains (.+)$",
            r"^(.+?) causes (.+)$",
            r"^(.+?) leads to (.+)$",
        ]

        for chunk in chunks:
            chunk = chunk.rstrip(".!?")

            for pattern in patterns:
                match = re.match(pattern, chunk, re.IGNORECASE)

                if match:
                    term = match.group(1).strip()
                    definition = match.group(2).strip()

                    if (
                        len(term) > 1
                        and len(definition) > 3
                        and len(term.split()) <= 10
                    ):
                        flashcards.append({
                            "front": f"What is {term}?",
                            "back": definition
                        })

                    break

        random.shuffle(flashcards)
        return flashcards[:amount]

    def generate_quiz_from_notes(notes, amount, quiz_type):
        quizzes = []
        chunks = split_notes(notes)

        banned_words = {
            "because", "therefore", "however", "between", "through",
            "during", "should", "would", "could", "where", "which",
            "their", "there", "about", "after", "before", "these",
            "those", "being", "using", "while", "since", "until"
        }

        possible_answers_pool = []

        for chunk in chunks:
            words = re.findall(r"\b[A-Za-z][A-Za-z\-]+\b", chunk)
            for word in words:
                if len(word) > 4 and word.lower() not in banned_words:
                    possible_answers_pool.append(word)

        for chunk in chunks:
            words = re.findall(r"\b[A-Za-z][A-Za-z\-]+\b", chunk)

            possible_answers = [
                word for word in words
                if len(word) > 4 and word.lower() not in banned_words
            ]

            if not possible_answers:
                continue

            answer = random.choice(possible_answers)
            question_text = chunk.replace(answer, "______", 1)

            quiz_item = {
                "question": question_text,
                "answer": answer,
                "type": quiz_type,
                "hint": make_hint(answer),
                "times_correct": 0,
                "times_attempted": 0
            }

            if quiz_type == "Multiple Choice":
                wrong_choices = []

                shuffled_pool = possible_answers_pool[:]
                random.shuffle(shuffled_pool)

                for choice in shuffled_pool:
                    if choice.lower() != answer.lower() and choice not in wrong_choices:
                        wrong_choices.append(choice)

                    if len(wrong_choices) == 3:
                        break

                while len(wrong_choices) < 3:
                    wrong_choices.append("None of these")

                options = wrong_choices + [answer]
                random.shuffle(options)

                quiz_item["options"] = options

            quizzes.append(quiz_item)

        random.shuffle(quizzes)
        return quizzes[:amount]

    def reset_quiz_state():
        st.session_state.current_quiz_index = 0
        st.session_state.current_quiz_score = 0
        st.session_state.quiz_started = True
        st.session_state.quiz_answered = False
        st.session_state.last_quiz_result = None

    # -----------------------------
    # Notes input
    # -----------------------------
    st.subheader("📥 Paste Your Notes")

    notes = st.text_area(
        "Paste notes here",
        height=230,
        placeholder=(
            "Example:\n"
            "Photosynthesis: the process plants use to convert sunlight into energy.\n"
            "Mitochondria is the powerhouse of the cell.\n"
            "Osmosis = movement of water across a membrane."
        )
    )

    st.divider()

    # -----------------------------
    # Generate flashcards
    # -----------------------------
    st.subheader("🃏 Generate Flashcards")

    flashcard_amount = st.slider(
        "How many flashcards do you want?",
        min_value=1,
        max_value=50,
        value=10
    )

    if st.button("✨ Generate Flashcards", use_container_width=True):
        if notes.strip() == "":
            st.warning("Paste notes first.")
        else:
            new_cards = generate_flashcards_from_notes(notes, flashcard_amount)

            if len(new_cards) == 0:
                st.warning("I couldn't find enough definition-style notes. Try formats like `Term: definition`, `Term = definition`, or `Term is definition`.")
            else:
                st.session_state.flashcards = new_cards
                st.session_state.current_card_index = 0
                st.session_state.show_card_answer = False
                st.success(f"Generated {len(new_cards)} flashcards!")

    # -----------------------------
    # Flashcard review
    # -----------------------------
    st.subheader("🔁 Review Flashcards")

    if len(st.session_state.flashcards) == 0:
        st.info("No flashcards yet.")
    else:
        index = st.session_state.current_card_index
        total_cards = len(st.session_state.flashcards)

        if index >= total_cards:
            st.session_state.current_card_index = total_cards - 1
            index = st.session_state.current_card_index

        card = st.session_state.flashcards[index]
        card_key = card["front"]

        if card_key not in st.session_state.card_accuracy:
            st.session_state.card_accuracy[card_key] = {
                "correct": 0,
                "attempts": 0
            }

        st.write(f"Card **{index + 1}** of **{total_cards}**")
        st.info(card["front"])

        if st.button("👀 Show Answer"):
            st.session_state.show_card_answer = True

        if st.session_state.show_card_answer:
            st.success(card["back"])

            col1, col2 = st.columns(2)

            with col1:
                if st.button("✅ I got it correct"):
                    st.session_state.card_accuracy[card_key]["correct"] += 1
                    st.session_state.card_accuracy[card_key]["attempts"] += 1
                    st.session_state.show_card_answer = False

                    if st.session_state.current_card_index < total_cards - 1:
                        st.session_state.current_card_index += 1

                    st.rerun()

            with col2:
                if st.button("❌ I missed it"):
                    st.session_state.card_accuracy[card_key]["attempts"] += 1
                    st.session_state.show_card_answer = False

                    if st.session_state.current_card_index < total_cards - 1:
                        st.session_state.current_card_index += 1

                    st.rerun()

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("⬅️ Previous Card"):
                if st.session_state.current_card_index > 0:
                    st.session_state.current_card_index -= 1
                    st.session_state.show_card_answer = False
                    st.rerun()

        with col2:
            if st.button("➡️ Next Card"):
                if st.session_state.current_card_index < total_cards - 1:
                    st.session_state.current_card_index += 1
                    st.session_state.show_card_answer = False
                    st.rerun()

        with col3:
            if st.button("🔀 Shuffle Cards"):
                random.shuffle(st.session_state.flashcards)
                st.session_state.current_card_index = 0
                st.session_state.show_card_answer = False
                st.rerun()

        accuracy_data = st.session_state.card_accuracy[card_key]
        attempts = accuracy_data["attempts"]
        correct = accuracy_data["correct"]

        if attempts > 0:
            accuracy = round((correct / attempts) * 100, 1)
            st.write(f"Current card accuracy: **{accuracy}%**")
        else:
            st.write("Current card accuracy: **No attempts yet**")

    st.divider()

    # -----------------------------
    # Generate quiz
    # -----------------------------
    st.subheader("📝 Generate Quiz")

    quiz_amount = st.slider(
        "How many quiz questions do you want?",
        min_value=1,
        max_value=50,
        value=10
    )

    quiz_type = st.radio(
        "Quiz type",
        ["Multiple Choice", "Free Response"],
        horizontal=True
    )

    if st.button("🧪 Generate Quiz", use_container_width=True):
        if notes.strip() == "":
            st.warning("Paste notes first.")
        else:
            new_quiz = generate_quiz_from_notes(notes, quiz_amount, quiz_type)

            if len(new_quiz) == 0:
                st.warning("I couldn't generate quiz questions from these notes.")
            else:
                st.session_state.quizzes = new_quiz
                reset_quiz_state()
                st.success(f"Generated {len(new_quiz)} {quiz_type.lower()} questions!")

    # -----------------------------
    # Quiz mode
    # -----------------------------
    st.subheader("🎯 Take Quiz")

    if len(st.session_state.quizzes) == 0:
        st.info("No quiz generated yet.")
    else:
        if not st.session_state.quiz_started:
            if st.button("▶️ Start Quiz"):
                reset_quiz_state()
                st.rerun()

        else:
            quiz_index = st.session_state.current_quiz_index
            total_questions = len(st.session_state.quizzes)

            if quiz_index >= total_questions:
                score = st.session_state.current_quiz_score
                percent = round((score / total_questions) * 100, 1)

                st.success(f"Quiz finished! Score: {score}/{total_questions} = {percent}%")

                st.session_state.quiz_scores.append(percent)

                if st.button("🔁 Retake Quiz"):
                    reset_quiz_state()
                    st.rerun()

            else:
                question = st.session_state.quizzes[quiz_index]

                st.write(f"Question **{quiz_index + 1}** of **{total_questions}**")
                st.write(question["question"])

                if st.button("💡 Show Hint"):
                    st.info(question["hint"])

                user_answer = None

                if question["type"] == "Multiple Choice":
                    user_answer = st.radio(
                        "Choose an answer:",
                        question["options"],
                        key=f"mc_{quiz_index}"
                    )

                else:
                    user_answer = st.text_input(
                        "Type your answer:",
                        key=f"fr_{quiz_index}"
                    )

                if not st.session_state.quiz_answered:
                    if st.button("✅ Submit Answer"):
                        correct_answer = question["answer"]

                        question["times_attempted"] += 1

                        if user_answer.strip().lower() == correct_answer.strip().lower():
                            question["times_correct"] += 1
                            st.session_state.current_quiz_score += 1
                            st.session_state.last_quiz_result = "correct"
                        else:
                            st.session_state.last_quiz_result = "incorrect"

                        st.session_state.quiz_answered = True
                        st.rerun()

                else:
                    correct_answer = question["answer"]

                    if st.session_state.last_quiz_result == "correct":
                        st.success("Correct!")
                    else:
                        st.error(f"Not quite. Correct answer: {correct_answer}")

                    if question["times_attempted"] > 0:
                        q_accuracy = round(
                            (question["times_correct"] / question["times_attempted"]) * 100,
                            1
                        )
                        st.write(f"Question accuracy: **{q_accuracy}%**")

                    if st.button("➡️ Next Question"):
                        st.session_state.current_quiz_index += 1
                        st.session_state.quiz_answered = False
                        st.session_state.last_quiz_result = None
                        st.rerun()

    st.divider()

    # -----------------------------
    # Overall stats
    # -----------------------------
    st.subheader("📊 Study Tools Stats")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Flashcards", len(st.session_state.flashcards))

    with col2:
        st.metric("Quiz Questions", len(st.session_state.quizzes))

    with col3:
        if len(st.session_state.quiz_scores) > 0:
            avg_score = round(sum(st.session_state.quiz_scores) / len(st.session_state.quiz_scores), 1)
            st.metric("Avg Quiz Score", f"{avg_score}%")
        else:
            st.metric("Avg Quiz Score", "N/A")