from dotenv import load_dotenv
from flask import Flask, request, jsonify,render_template,jsonify
load_dotenv() ## loading all the dependencies variables
import streamlit as st 
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


### functions to load Gemini Pro Model and get response:- 

#model = genai.GenerativeModel("gemini-1.5-flash")
model = genai.GenerativeModel("learnlm-1.5-pro-experimental")
#model = genai.GenerativeModel("gemini-pro")
def get_gemini_response(text):
    response = model.generate_content(text)
    return response.text

## Initialize the streamlet applications:- 

st.set_page_config(page_title='Question & Answers Application')
st.header('Content-Type:- Gemini Application')
#st.write('Gemini is a large language model that can be used for a variety of tasks,')
input = st.text_input("Input: ",key="input")
submit = st.button('Enter Your Input Questions')

if submit:
    response = get_gemini_response(input)
    st.subheader('The response Output:-')
    st.write(response)
    

    