import streamlit as st

# App title
st.title("👋 Simple Streamlit App")

# Input section
name = st.text_input("Enter your name:")
age = st.number_input("Enter your age:", min_value=0, max_value=120, step=1)

# Button
if st.button("Submit"):
    if name:
        st.success(f"Hello, {name}! Yaaou are {age} years old.")
    else:
        st.warning("Please enter your name before submitting.")
