import streamlit as st

def render():
    st.markdown(
        """
        <style>
        .header {
            background-color: #f8f9fa;
            padding: 10px;
            text-align: center;
            font-size: 24px;
        }
        </style>
        <div class="header">
            <b>My Streamlit App</b>
        </div>
        """,
        unsafe_allow_html=True
    )
