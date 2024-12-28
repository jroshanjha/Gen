import streamlit as st

def render():
    st.markdown(
        """
        <style>
        .footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            background-color: #f8f9fa;
            text-align: center;
            padding: 10px;
        }
        </style>
        <div class="footer">
            <small>© 2024 My Streamlit App</small>
        </div>
        """,
        unsafe_allow_html=True
    )
