import streamlit as st
from components import header, sidebar, footer

# Initialize app
st.set_page_config(page_title="My Streamlit App", layout="wide")

# Reusable components
header.render()
sidebar.render()

# Main app content
st.title("Welcome to My Streamlit App!")
st.write("Use the sidebar to navigate between pages.")

footer.render()
