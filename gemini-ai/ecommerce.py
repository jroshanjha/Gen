import streamlit as st 
import os 
from dotenv import load_dotenv
import requests 
from bs4 import BeautifulSoup
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import plotly.express as px
import google.generativeai as genai

load_dotenv()
## configure the api key:-
genai.configure(api_key=os.getenv("GOOGLE_API_SERVICE"))

#model = genai.GenerativeModel("learnlm-1.5-pro-experimental")
model = genai.GenerativeModel("gemini-pro")
#gemini-1.5-pro-001

# Download required NLTK data
nltk.download('vader_lexicon')
class ProductAnalyzer:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
    
    def scrape_products(self, url):
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        products = []
        for item in soup.find_all('div', class_='product-item'):
            product = {
                'name': item.find('h2', class_='product-name').text.strip(),
                'price': item.find('span', class_='price').text.strip(),
                'description': item.find('div', class_='description').text.strip(),
                'rating': item.find('div', class_='rating').text.strip()
            }
            products.append(product)
        
        return pd.DataFrame(products)
    
    def analyze_sentiment(self, text):
        scores = self.sia.polarity_scores(text)
        return scores['compound']
    
    def analyze_products(self, df):
        df['sentiment'] = df['description'].apply(self.analyze_sentiment)
        df['price_numeric'] = df['price'].str.replace('$', '').astype(float)
        return df

def main():
    st.title("E-commerce Product Analyzer")
    
    url = st.text_input("Enter E-commerce URL")
    
    if st.button("Analyze Products"):
        if url:
            with st.spinner("Scraping and analyzing products..."):
                analyzer = ProductAnalyzer()
                
                # Get and analyze data
                df = analyzer.scrape_products(url)
                
                df = analyzer.analyze_products(df)
                
                # Display results
                st.subheader("Product Analysis Results")
                st.dataframe(df)
                
                # Visualizations
                fig1 = px.scatter(df, x='price_numeric', y='sentiment',
                                hover_data=['name'], 
                                title='Price vs Sentiment Analysis')
                st.plotly_chart(fig1)
                
                fig2 = px.box(df, y='sentiment', 
                             title='Sentiment Distribution')
                st.plotly_chart(fig2)
                
                # Summary statistics
                st.subheader("Summary Statistics")
                st.write(f"Average Product Price: ${df['price_numeric'].mean():.2f}")
                st.write(f"Average Sentiment Score: {df['sentiment'].mean():.2f}")
        
        else:
            st.warning("Please enter a valid URL")

if __name__ == "__main__":
    main()