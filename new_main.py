import streamlit as st

st.title("My First Streamlit Website 🚀")

st.write("Hello! This is my first Python-powered website.")

name = st.text_input("What's your name?")

if name:
    st.write(f"Hi {name}! Welcome to my app 😎")

mood = st.slider("How productive are you feeling today?", 1, 10, 5)

st.write(f"Productivity level: {mood}/10")

if st.button("Generate study advice"):
    if mood <= 3:
        st.write("Start with a tiny 10-minute task. Momentum first, perfection later.")
    elif mood <= 7:
        st.write("Do a 25-minute focus session, then take a 5-minute break.")
    else:
        st.write("You're locked in. Do your hardest task first while your brain is cracked.")
        
        
