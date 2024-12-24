import streamlit as st 
import os
import google.generativeai as genai
import PIL.Image
from PIL import Image
from dotenv import load_dotenv
# load_dotenv()

# -- #from langchain.llms import OpenAI
# -- #from langchain.chains import QuestionAnsweringChain
# Option 1: Set API key directly

# Option 2: Set environment variable
# In terminal/command prompt:
# export GOOGLE_API_KEY='YOUR_API_KEY'

#genai.configure(api_key='AIzaSyCWsS5zmsstSDipuLUHyfVLFP-1LkcVlxs')
os.getenv("GOOGLE_API_SERVICE")
genai.configure(api_key=os.getenv("GOOGLE_API_SERVICE"))

### functions to load Gemini Pro Model and get response:- 

#model = genai.GenerativeModel("gemini-1.5-flash")
#model = genai.GenerativeModel("gemini-pro-vision")
model = genai.GenerativeModel("gemini-1.5-pro-001")
def get_gemini_response(text,image):
    if text!="":
        response = model.generate_content([text, image])
    else:
        response = model.generate_content(image)
    return response.text 

## Initialize the streamlet applications:- 

# Initialize tab title  
st.set_page_config(page_title="Text and Image Generation:-")
st.header("Content-Type Application/")
# Title
st.title("Personal Finance Advisor 💰")

#input = st.file_uploader("Upload an image", type=["jpg","png"])

# Image upload
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png","pdf","webp","JFIF"])
image =""
if uploaded_file is not None:
        # Display image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_container_width =True) # use_column_width
        
        # Save image (optional)
        with open(f"uploads/{uploaded_file.name}", "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Saved file: {uploaded_file.name}")

# Input Text:-
input = st.text_input("Input: ",key="input")        
        
submit = st.button("Tell me What about this image file!!!")
## if submit is clicked

if submit:
    response = get_gemini_response(input,image)
    st.subheader('The response Output:-')
    st.write(response)

