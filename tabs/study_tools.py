import streamlit as st
import re
import random

def run_study_tools():
    st.title("🧠 Study Tools")
    st.write("Paste your notes, then generate flashcards or quiz questions.")

    # -----------------------------
    # Initialize state
    # -----------------------------
    if "flashcards" not in st.session_state:
        st.session_state.flashcards = []

    if "quizzes" not in st.session_state:
        st.session_state.quizzes = []

    # -----------------------------
    # Helper functions
    # -----------------------------
    def clean_sentence(sentence):
        sentence = sentence.strip()
        sentence = re.sub(r"\s+", " ", sentence)
        return sentence

    def split_into_sentences(text):
        # Splits by periods, question marks, exclamation points, OR line breaks
        chunks = re.split(r"(?<=[.!?])\s+|\n+", text)

        cleaned_chunks = []
        for chunk in chunks:
            chunk = clean_sentence(chunk)
            if len(chunk) > 5:
                cleaned_chunks.append(chunk)

        return cleaned_chunks

    def generate_flashcards_from_notes(notes):
        flashcards = []
        chunks = split_into_sentences(notes)

        patterns = [
            # Colon style: Photosynthesis: process plants use...
            r"^(.+?)\s*:\s*(.+)$",

            # Dash style: Photosynthesis - process plants use...
            r"^(.+?)\s*-\s*(.+)$",

            # Equals style: Photosynthesis = process plants use...
            r"^(.+?)\s*=\s*(.+)$",

            # Definition sentence styles
            r"^(.+?) is defined as (.+)$",
            r"^(.+?) is (.+)$",
            r"^(.+?) are (.+)$",
            r"^(.+?) means (.+)$",
            r"^(.+?) refers to (.+)$",
            r"^(.+?) consists of (.+)$",
            r"^(.+?) contains (.+)$"
        ]

        for chunk in chunks:
            chunk_no_period = chunk.rstrip(".!?")

            for pattern in patterns:
                match = re.match(pattern, chunk_no_period, re.IGNORECASE)

                if match:
                    term = match.group(1).strip()
                    definition = match.group(2).strip()

                    # Avoid weird bad flashcards
                    if (
                        len(term.split()) <= 8
                        and len(definition.split()) >= 2
                        and len(term) > 1
                        and len(definition) > 3
                    ):
                        flashcards.append({
                            "front": f"What is {term}?",
                            "back": definition
                        })

                    break

        return flashcards

    def generate_quiz_from_notes(notes):
        quizzes = []
        chunks = split_into_sentences(notes)

        banned_words = {
            "because", "therefore", "however", "between",
            "through", "during", "should", "would", "could",
            "where", "which", "their", "there", "about",
            "after", "before", "these", "those", "being"
        }

        for chunk in chunks:
            words = re.findall(r"\b[A-Za-z][A-Za-z\-]+\b", chunk)

            possible_answers = [
                word for word in words
                if len(word) > 5 and word.lower() not in banned_words
            ]

            if possible_answers:
                answer = random.choice(possible_answers)
                question = chunk.replace(answer, "______", 1)

                quizzes.append({
                    "question": question,
                    "answer": answer
                })

        return quizzes

    # -----------------------------
    # Input area
    # -----------------------------
    st.subheader("📥 Add Your Notes")

    notes = st.text_area(
        "Paste your notes here",
        height=250,
        placeholder=(
            "Example:\n"
            "Photosynthesis: the process plants use to convert sunlight into chemical energy.\n"
            "Mitochondria is the powerhouse of the cell.\n"
            "Hypothesis = a testable explanation."
        )
    )

    # -----------------------------
    # Generate tools
    # -----------------------------
    st.subheader("⚙️ Generate Study Materials")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✨ Generate Flashcards", use_container_width=True):
            if notes.strip():
                new_flashcards = generate_flashcards_from_notes(notes)

                if new_flashcards:
                    st.session_state.flashcards.extend(new_flashcards)
                    st.success(f"Generated {len(new_flashcards)} flashcards!")
                else:
                    st.warning(
                        "I couldn't find clear definition-style notes. "
                        "Try formats like 'Term: definition', 'Term = definition', or 'Term is definition'."
                    )
            else:
                st.warning("Please paste notes first.")

    with col2:
        if st.button("📝 Generate Quiz", use_container_width=True):
            if notes.strip():
                new_quizzes = generate_quiz_from_notes(notes)

                if new_quizzes:
                    st.session_state.quizzes.extend(new_quizzes)
                    st.success(f"Generated {len(new_quizzes)} quiz questions!")
                else:
                    st.warning("I couldn't generate quiz questions from these notes yet.")
            else:
                st.warning("Please paste notes first.")

    # -----------------------------
    # Display flashcards
    # -----------------------------
    st.divider()
    st.subheader("🃏 Flashcards")

    if len(st.session_state.flashcards) == 0:
        st.info("No flashcards yet. Generate some from your notes!")
    else:
        for i, card in enumerate(st.session_state.flashcards):
            with st.expander(f"Flashcard {i + 1}: {card['front']}"):
                new_front = st.text_input(
                    "Front",
                    value=card["front"],
                    key=f"flashcard_front_{i}"
                )

                new_back = st.text_area(
                    "Back",
                    value=card["back"],
                    key=f"flashcard_back_{i}"
                )

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("💾 Save Flashcard", key=f"save_flashcard_{i}"):
                        st.session_state.flashcards[i]["front"] = new_front
                        st.session_state.flashcards[i]["back"] = new_back
                        st.success("Flashcard updated!")

                with col2:
                    if st.button("🗑️ Delete Flashcard", key=f"delete_flashcard_{i}"):
                        st.session_state.flashcards.pop(i)
                        st.rerun()

    # -----------------------------
    # Display quizzes
    # -----------------------------
    st.divider()
    st.subheader("📝 Quiz Questions")

    if len(st.session_state.quizzes) == 0:
        st.info("No quiz questions yet. Generate some from your notes!")
    else:
        for i, quiz in enumerate(st.session_state.quizzes):
            with st.expander(f"Question {i + 1}"):
                st.write("**Question:**")
                st.write(quiz["question"])

                user_answer = st.text_input(
                    "Your answer",
                    key=f"quiz_answer_input_{i}"
                )

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("✅ Check Answer", key=f"check_quiz_{i}"):
                        if user_answer.strip().lower() == quiz["answer"].strip().lower():
                            st.success("Correct!")
                        else:
                            st.error(f"Not quite. Correct answer: {quiz['answer']}")

                with col2:
                    if st.button("🗑️ Delete Question", key=f"delete_quiz_{i}"):
                        st.session_state.quizzes.pop(i)
                        st.rerun()