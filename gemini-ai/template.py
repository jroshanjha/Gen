# app.py
import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# Configure the default settings
st.set_page_config(
    page_title="My Streamlit App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton button {
        width: 100%;
    }
    .stSelectbox label {
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Session state initialization
if 'counter' not in st.session_state:
    st.session_state.counter = 0

def increment_counter():
    st.session_state.counter += 1

# Sidebar
with st.sidebar:
    st.title("Navigation")
    page = st.radio(
        "Choose a page",
        ["Dashboard", "Data Analysis", "Settings"]
    )
    
    st.divider()
    
    # Filters section
    st.subheader("Filters")
    date_range = st.date_input(
        "Select Date Range",
        [datetime.now(), datetime.now()]
    )
    
    category = st.multiselect(
        "Select Categories",
        ["Category A", "Category B", "Category C"]
    )

# Main content area
st.title("My Streamlit Application")

# Tabs
tab1, tab2, tab3 = st.tabs(["Overview", "Details", "Settings"])

with tab1:
    # Overview tab content
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Total Sales",
            value="$12,345",
            delta="15%"
        )
    
    with col2:
        st.metric(
            label="Customers",
            value="1,234",
            delta="-2%"
        )
    
    with col3:
        st.metric(
            label="Conversion Rate",
            value="23%",
            delta="7%"
        )

    # Sample chart
    chart_data = pd.DataFrame({
        'Date': pd.date_range('2024-01-01', periods=30),
        'Value': range(30)
    })
    
    st.plotly_chart(
        px.line(chart_data, x='Date', y='Value', title='Trend Analysis'),
        use_container_width=True
    )

with tab2:
    # Details tab content
    st.header("Detailed Analysis")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload your data",
        type=['csv', 'xlsx']
    )
    
    # Data table
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)
    else:
        st.info("Please upload a file to view the data.")
    
    # Download button
    st.download_button(
        label="Download Report",
        data="sample,data\n1,2\n3,4",
        file_name="report.csv",
        mime="text/csv"
    )

with tab3:
    # Settings tab content
    st.header("Settings")
    
    # Form example
    with st.form("settings_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        notifications = st.toggle("Enable Notifications")
        theme = st.select_slider(
            "Choose Theme",
            options=["Light", "Dark", "System"]
        )
        
        submitted = st.form_submit_button("Save Settings")
        if submitted:
            st.success("Settings saved successfully!")

# Footer
st.divider()
with st.container():
    st.markdown("""
        <div style='text-align: center'>
            <p>Made with ❤️ using Streamlit</p>
        </div>
    """, unsafe_allow_html=True)

# Error handling example
try:
    # Your code that might raise an error
    pass
except Exception as e:
    st.error(f"An error occurred: {str(e)}")