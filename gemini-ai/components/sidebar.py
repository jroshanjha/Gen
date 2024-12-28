import streamlit as st

def render():
    with st.sidebar:
        st.title("Navigation")
        st.radio("Go to:", ["Home", "About", "Contact"])
