from datetime import date
import streamlit as st
import requests
import pandas as pd
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
## configure the api key:-
genai.configure(api_key=os.getenv("GOOGLE_API_SERVICE"))

model = genai.GenerativeModel("gemini-pro")

def get_gemini_response(text):
    response = model.generate_content(text)
    return response.text

def t_ravel():
    ##title for title bar:- 
    ##st.set_page_config("Smart Travel Planner 🌍")  
    # Page title
    # Title
    st.title("Welcome to Smart Travel Planner 🌍")

    # Sidebar Menu
    menu = st.sidebar.radio("Menu", ["Plan Itinerary", "Flights & Hotels", "Local Recommendations", "Packing List", "Travel Chat"])

    prompt = "Tell me about Travel Planner"
    if menu == "Plan Itinerary":
        st.header("Plan Your Itinerary")
        destination = st.text_input("Enter Destination")
        start_date = st.date_input("Start Date", min_value=date.today())
        end_date = st.date_input("End Date", min_value=start_date)
        preferences = st.text_area("Enter Your Preferences (e.g., museums, beaches, nightlife)")

        if st.button("Generate Itinerary"):
            prompt = f"Plan a detailed trip itinerary for {destination} from {start_date} to {end_date}. Preferences: {preferences}."


    elif menu == "Flights & Hotels":
        st.header("Find Flights and Hotels")
        origin = st.text_input("Departure City")
        destination = st.text_input("Destination City")
        departure_date = st.date_input("Departure Date", min_value=date.today())
        return_date = st.date_input("Return Date", min_value=departure_date)

        if st.button("Search Deals"):
            prompt = f"Search Flights and Hotels for Departure {origin} , Designation {destination} and departure date {departure_date} , Return Date {return_date} "
            #st.write("Fetching deals... (Integrate with Skyscanner or Expedia API here)")

    elif menu == "Local Recommendations":
        st.header("Discover Local Attractions")
        location = st.text_input("Enter Location")
        if st.button("Get Recommendations"):
            prompt = f"Suggest top attractions, restaurants, and activities in {location}."

    elif menu == "Packing List":
        st.header("Packing List Generator")
        destination = st.text_input("Destination")
        travel_dates = st.date_input("Travel Dates", [])
        activity_type = st.text_area("Activities (e.g., hiking, formal events)")

        if st.button("Generate Packing List"):
            prompt = f"Create a packing list for a trip to {destination}. Dates: {travel_dates}. Activities: {activity_type}."

    elif menu == "Travel Chat":
        st.header("Ask Your Travel Assistant")
        question = st.text_input("Ask a question about your trip")
        if st.button("Get Answer"):
            prompt = question
            # response = openai.Completion.create(
            #     engine="text-davinci-003", prompt=question, max_tokens=150
            # )
            # st.write(response['choices'][0]['text'])

    response = get_gemini_response(prompt)
    st.subheader('The response Output:-')
    st.write(response)
    
# Main
if __name__ == "__main__":
    t_ravel()