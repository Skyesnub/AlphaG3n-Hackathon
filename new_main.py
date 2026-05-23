import streamlit as st

st.title("My First Streamlit Website 🚀")

st.write("Hello! This is my first Python-powered website.")

name = st.text_input("What's your name?")

if name:
    st.write(f"Hi {name}! Welcome to my app 😎")

mood = st.slider("How productive are you feeling today?", 1, 10, 5)

st.write(f"Productivity level: {mood}/10")
