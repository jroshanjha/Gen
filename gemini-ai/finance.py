import streamlit as st
import requests
import openai  # Replace with Gemini's SDK if using Gemini
import pandas as pd
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
## configure the api key:-
genai.configure(api_key=os.getenv("GOOGLE_API_SERVICE"))

# Set up API keys
#OPENAI_API_KEY = "your_openai_api_key"  # Replace with Gemini API key if applicable
#openai.api_key = OPENAI_API_KEY


#model = genai.GenerativeModel("learnlm-1.5-pro-experimental")
model = genai.GenerativeModel("gemini-pro")
#gemini-1.5-pro-001

#titale for title bar:- 
st.set_page_config("Personal Finance Advisor 💰")    
# Title
st.title("Personal Finance Advisor 💰")
#st.header("Personal Finance Advisor:-💁")

# Sidebar Menu
menu = st.sidebar.radio("Menu", ["Budget Planning", "Investment Guidance", "Debt Management", "Chat with Advisor"])

def get_gemini_response(text):
    response = model.generate_content(text)
    return response.text

prompt = "tell me about my self?"
if menu == "Budget Planning":
    st.header("Budget Planning 💁")
    income = st.number_input("Enter your monthly income", min_value=0)
    expenses = st.number_input("Enter your monthly expenses", min_value=0)
    savings_goal = st.number_input("Enter your savings goal", min_value=0)

    if st.button("Get Suggestions"):
        prompt = f"My monthly income is {income}, expenses are {expenses}, and my savings goal is {savings_goal}. Suggest ways to optimize my budget."
        # response = openai.Completion.create(
        #     engine="text-davinci-003", prompt=prompt, max_tokens=150
        # )
        #st.write(response['choices'][0]['text'])
        
elif menu == "Investment Guidance":
    st.header("Investment Guidance😃")
    risk = st.selectbox("Risk Tolerance", ["Low", "Medium", "High"])
    time_frame = st.slider("Investment Time Frame (Years)", 1, 30, 5)
    goal = st.text_input("Investment Goal")

    if st.button("Get Investment Advice"):
        prompt = f"I have a {risk}-risk tolerance, a {time_frame}-year investment horizon, and my goal is {goal}. Suggest investment strategies."

elif menu == "Debt Management":
    st.header("Debt Management💡")
    debt = st.number_input("Total Debt Amount", min_value=0)
    interest_rate = st.number_input("Interest Rate (%)", min_value=0.0)
    monthly_payment = st.number_input("Monthly Payment", min_value=0)

    if st.button("Get Repayment Plan"):
        prompt = f"My total debt is {debt} with an interest rate of {interest_rate}%, and I can pay {monthly_payment} monthly. Suggest a repayment plan."
        
elif menu == "Chat with Advisor":
    st.header("Chat with Your Financial Advisor🧑")
    user_query = st.text_input("Ask a question")
    if st.button("Submit"):
        response = user_query
        # response = openai.Completion.create(
        #     engine="text-davinci-003", prompt=user_query, max_tokens=150
        # )
        # st.write(response['choices'][0]['text'])
        
response = get_gemini_response(prompt)
st.subheader('The response Output:-')
st.write(response)