import streamlit as st 
import os 
from google import generativeai as genai
from google.cloud import aiplatform,storage
from PIL import Image
import io
from dotenv import load_dotenv

load_dotenv()
## configure the api key:-
genai.configure(api_key=os.getenv("GOOGLE_API_SERVICE"))

#model = genai.GenerativeModel("learnlm-1.5-pro-experimental")
#model = genai.GenerativeModel("gemini-pro")
text_model = genai.GenerativeModel('gemini-pro')
vision_model = genai.GenerativeModel('gemini-1.5-pro-001') # gemini-pro-vision1


def get_gemini_response(request):
    try:
        response = text_model.generate_content(request)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        print("Analysis complete")

# Analyze Show functions which return a prompt message indicating the results.

# def analyze_show(show_name, show_description):
#     prompt = f"""
#     Analyze the Netflix show:
#     Name: {show_name}
#     Description: {show_description}
    
#     Provide:
#     1. Target audience
#     2. Similar show recommendations
#     3. Key themes
#     4. Content rating justification
#     """
#     return get_gemini_response(prompt)
    
#     # response = model.generate_content(prompt)
#     # return response.text

def analyze_show(show_name, show_description, image=None):
    base_prompt = f"""
    Analyze the Netflix show:
    Name: {show_name}
    Description: {show_description}
    
    Provide:
    1. Target audience
    2. Similar show recommendations
    3. Key themes
    4. Content rating justification
    """
    
    if image:
        image_prompt = "Analyze this show poster and describe key visual elements that indicate the show's genre, tone, and target audience."
        vision_response = vision_model.generate_content([image_prompt, image])
        
        combined_prompt = f"""
        {base_prompt}
        
        Poster Analysis:
        {vision_response.text}
        
        Provide a comprehensive analysis incorporating both the show details and poster visuals.
        """
        response = text_model.generate_content(combined_prompt)
    else:
        response = text_model.generate_content(base_prompt)
    
    return response.text

def process_image(uploaded_file):
    if uploaded_file is not None:
        # Read the image file
        image = Image.open(uploaded_file)
        
        # Convert image if not in RGB
        if image.mode != "RGB":
            img = image.convert("RGB")
        
        return image, img  # Return both display image and Gemini-compatible image
    return None, None

# def main():
#     st.set_page_config(page_title='Netflix Show Analyzer')
#     #st.header('Netflix Show Analyzer')
#     st.title("Netflix Show Analyzer")
    
#     # Input fields
#     show_name = st.text_input("Enter Netflix Show Name")
#     show_description = st.text_area("Enter Show Description")
    
#     # Optional image upload
#     uploaded_file = st.file_uploader("Upload Show Poster (optional)", type=['png', 'jpg', 'jpeg'])
#     if uploaded_file:
#         image = Image.open(uploaded_file)
#         st.image(image, caption=show_name, width=300)
    
#     # Analyze button
#     if st.button("Analyze Show"):
#         if show_name and show_description:
#             with st.spinner("Analyzing..."):
#                 analysis = analyze_show(show_name, show_description)
#                 st.markdown("### Analysis Results")
#                 st.write(analysis)
#         else:
#             st.warning("Please enter both show name and description")
       
def main():
    st.title("Netflix Show Analyzer")
    
    show_name = st.text_input("Enter Netflix Show Name")
    show_description = st.text_area("Enter Show Description")
    
    uploaded_file = st.file_uploader("Upload Show Poster (optional)", type=['png', 'jpg', 'jpeg'])
    
    display_image = None
    gemini_image = None
    
    if uploaded_file:
        display_image, gemini_image = process_image(uploaded_file)
        if display_image:
            st.image(display_image, caption=show_name, width=300)
    
    if st.button("Analyze Show"):
        if show_name and show_description:
            with st.spinner("Analyzing show and poster..."):
                try:
                    analysis = analyze_show(show_name, show_description, gemini_image)
                    st.markdown("### Analysis Results")
                    st.write(analysis)
                except Exception as e:
                    st.error(f"Error during analysis: {str(e)}")
        else:
            st.warning("Please enter both show name and description")
            
if __name__ == '__main__':
    main()
    