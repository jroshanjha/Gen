import streamlit as st
from transformers import pipeline
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
import csv

def initialize_analyzer():
    return pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def analyze_batch(analyzer, texts):
    results = []
    for text in texts:
        if text.strip():  # Skip empty texts
            result = analyzer(text)[0]
            results.append({
                'text': text,
                'sentiment': result['label'],
                'confidence': result['score']
            })
    return pd.DataFrame(results)

def create_sentiment_distribution(df):
    sentiment_counts = df['sentiment'].value_counts()
    fig = px.pie(
        values=sentiment_counts.values,
        names=sentiment_counts.index,
        title='Sentiment Distribution',
        color_discrete_map={'POSITIVE': '#2ecc71', 'NEGATIVE': '#e74c3c'}
    )
    return fig

def create_confidence_histogram(df):
    fig = px.histogram(
        df,
        x='confidence',
        color='sentiment',
        nbins=20,
        title='Confidence Score Distribution',
        color_discrete_map={'POSITIVE': '#2ecc71', 'NEGATIVE': '#e74c3c'}
    )
    return fig

def main():
    st.title("Advanced Text Sentiment Analyzer")
    
    # Initialize the analyzer
    analyzer = initialize_analyzer()
    
    # Sidebar for input method selection
    input_method = st.sidebar.radio(
        "Choose Input Method",
        ["Single Text", "Multiple Texts", "CSV Upload"]
    )
    
    if input_method == "Single Text":
        # Single text input
        text_input = st.text_area(
            "Enter text to analyze:",
            "Type or paste your text here..."
        )
        
        if st.button("Analyze Text"):
            if text_input and text_input != "Type or paste your text here...":
                df = analyze_batch(analyzer, [text_input])
                
                # Display single result with large sentiment indicator
                result = df.iloc[0]
                sentiment_color = "#2ecc71" if result['sentiment'] == "POSITIVE" else "#e74c3c"
                st.markdown(
                    f"""
                    <div style="padding: 20px; 
                               background-color: {sentiment_color}; 
                               border-radius: 10px; 
                               color: white;">
                        <h3 style="margin: 0;">
                            {result['sentiment']} 
                            ({result['confidence']:.2%})
                        </h3>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
    elif input_method == "Multiple Texts":
        # Text area for multiple inputs
        text_inputs = st.text_area(
            "Enter multiple texts (one per line):",
            "Text 1\nText 2\nText 3",
            height=200
        )
        
        if st.button("Analyze Texts"):
            texts = text_inputs.split('\n')
            df = analyze_batch(analyzer, texts)
            
            # Display results in expandable section
            with st.expander("Show Detailed Results", expanded=True):
                st.dataframe(df)
                
            # Display visualizations
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(create_sentiment_distribution(df), use_container_width=True)
            with col2:
                st.plotly_chart(create_confidence_histogram(df), use_container_width=True)
                
    else:  # CSV Upload
        uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
        text_column = st.text_input("Enter the name of the text column:", "text")
        
        if uploaded_file and st.button("Analyze CSV"):
            # Read CSV
            df_input = pd.read_csv(uploaded_file)
            
            if text_column in df_input.columns:
                # Analyze texts from CSV
                texts = df_input[text_column].tolist()
                df_results = analyze_batch(analyzer, texts)
                
                # Merge results with original data
                df_final = pd.concat([df_input, df_results.drop('text', axis=1)], axis=1)
                
                # Display results
                with st.expander("Show Detailed Results", expanded=True):
                    st.dataframe(df_final)
                    
                # Download button for results
                csv = df_final.to_csv(index=False)
                st.download_button(
                    "Download Results",
                    csv,
                    "sentiment_analysis_results.csv",
                    "text/csv",
                    key='download-csv'
                )
                
                # Display visualizations
                col1, col2 = st.columns(2)
                with col1:
                    st.plotly_chart(create_sentiment_distribution(df_results), use_container_width=True)
                with col2:
                    st.plotly_chart(create_confidence_histogram(df_results), use_container_width=True)
            else:
                st.error(f"Column '{text_column}' not found in CSV file.")

if __name__ == "__main__":
    main()