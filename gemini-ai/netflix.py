import streamlit as st 
import os 
from google import generativeai as genai
from google.cloud import aiplatform,storage
from PIL import Image
from dotenv import load_dotenv

load_dotenv()
## configure the api key:-
genai.configure(api_key=os.getenv("GOOGLE_API_SERVICE"))

#model = genai.GenerativeModel("learnlm-1.5-pro-experimental")
model = genai.GenerativeModel("gemini-pro")
#gemini-1.5-pro-001

def get_gemini_response(request):
    try:
        response = model.generate_content(request)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        print("Analysis complete")

# Analyze Show functions which return a prompt message indicating the results.

def analyze_show(show_name, show_description):
    prompt = f"""
    Analyze the Netflix show:
    Name: {show_name}
    Description: {show_description}
    
    Provide:
    1. Target audience
    2. Similar show recommendations
    3. Key themes
    4. Content rating justification
    """
    return get_gemini_response(prompt)
    
    # response = model.generate_content(prompt)
    # return response.text

def main():
    st.set_page_config(page_title='Netflix Show Analyzer')
    #st.header('Netflix Show Analyzer')
    st.title("Netflix Show Analyzer")
    
    # Input fields
    show_name = st.text_input("Enter Netflix Show Name")
    show_description = st.text_area("Enter Show Description")
    
    # Optional image upload
    uploaded_file = st.file_uploader("Upload Show Poster (optional)", type=['png', 'jpg', 'jpeg'])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption=show_name, width=300)
    
    # Analyze button
    if st.button("Analyze Show"):
        if show_name and show_description:
            with st.spinner("Analyzing..."):
                analysis = analyze_show(show_name, show_description)
                st.markdown("### Analysis Results")
                st.write(analysis)
        else:
            st.warning("Please enter both show name and description")
       
if __name__ == '__main__':
    main()
    