# This is a list of functionalities that can be implemented using coding, particularly in Python.
# These functionalities include autocomplete location search, displaying a map based on a location,
# retrieving coordinates from a location name (Geocoding), and showing nearby places using the Places
# API.
# ✅ What You Can Do:
# Autocomplete location search 🔍

# Show map based on location 🗺️

# Get coordinates from location name (Geocoding)

# Show places nearby (using Places API)

# -- 🐍 2. Install Required Python Libraries
# pip install streamlit geopy requests python-dotenv

# -- 🚀 3. Sample Streamlit Code: Location Search + Coordinates + Map

# Google Cloud Console
# Enable the following APIs:

# Maps JavaScript API

# Places API

# Geocoding API


import streamlit as st
import requests
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import st_folium

# 🔐 Add your API key here
GOOGLE_API_KEY = "AIzaSyCsTA8jx9211m1sHiV-E9mpTQfK_spOSPA"

st.title("📍 Google Location Search App")

location = st.text_input("Enter a location (e.g., Delhi, Eiffel Tower, etc.):")

# if location:
#     geolocator = Nominatim(user_agent="geoapiExercises")
#     try:
#         loc = geolocator.geocode(location)
        
#         print('📍Coordinates: Latitude: %s, Longitude: %s' % (loc.latitude, loc.longitude))
    
#         if loc:
#             st.success(f"📌 Coordinates: Latitude: {loc.latitude}, Longitude: {loc.longitude}")

#             # Map
#             map_ = folium.Map(location=[loc.latitude, loc.longitude], zoom_start=13)
#             folium.Marker([loc.latitude, loc.longitude], popup=location).add_to(map_)
#             st_folium(map_, width=700)
#         else:
#             st.error("Location not found.")
#     except Exception as e:
#         st.error(f"Error (Location not found.) :- {e}")


# 🌍 Optional: Use Google Places Autocomplete API

import streamlit as st
import streamlit.components.v1 as components

# html_code = f"""
# <!DOCTYPE html>
# <html>
#   <head>
#     <script src="https://maps.googleapis.com/maps/api/js?key={GOOGLE_API_KEY}&libraries=places"></script>
#     <script>
#       function initAutocomplete() {{
#         var input = document.getElementById('autocomplete');
#         new google.maps.places.Autocomplete(input);
#       }}
#     </script>
#   </head>
#   <body onload="initAutocomplete()">
#     <input id="autocomplete" type="text" style="width: 100%; padding: 10px;" placeholder="Search location"/>
#   </body>
# </html>
# """

#components.html(html_code, height=100)


# 🧠 Bonus: Use Google Places API via Python 

# def get_place_details(place_name):
#     url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
#     params = {
#         'input': place_name,
#         'inputtype': 'textquery',
#         'fields': 'formatted_address,name,geometry',
#         'key': GOOGLE_API_KEY
#     }
#     response = requests.get(url, params=params).json()
#     return response

# if location:
#     result = get_place_details(location)
#     st.json(result)


# 📦 Save Your API Key Securely
# from dotenv import load_dotenv
# import os
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# .streamlit/secrets.toml
# [google]
# api_key = "your_key"


# Setup Your API Key
# Get a Google Maps API key

# Enable the following APIs:

# Maps JavaScript API

# Places API

# Directions API

# Geocoding API


# 1️⃣ Autocomplete Input (Frontend with JavaScript + Streamlit)

import streamlit as st
import streamlit.components.v1 as components

GOOGLE_API_KEY = "YOUR_API_KEY"

html_code = f"""
<input id="autocomplete" placeholder="Search for a location" type="text" style="width: 90%; padding: 10px;" />
<script src="https://maps.googleapis.com/maps/api/js?key={GOOGLE_API_KEY}&libraries=places"></script>
<script>
  function initAutocomplete() {{
    var input = document.getElementById('autocomplete');
    new google.maps.places.Autocomplete(input);
  }}
  window.onload = initAutocomplete;
</script>
"""

st.components.v1.html(html_code, height=100)

# 2️⃣ Nearby Search Using Places API 
import requests

def nearby_places(lat, lon, radius, type_):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lon}",
        "radius": radius,
        "type": type_,
        "key": GOOGLE_API_KEY
    }
    response = requests.get(url, params=params)
    return response.json()

# Example usage
places = nearby_places(28.6139, 77.2090, 2000, "restaurant")
for place in places["results"]:
    st.write(place["name"], "-", place["vicinity"])

# 3️⃣ Directions API: Draw Route on Map
def get_directions(origin, destination):
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "mode": "driving",
        "key": GOOGLE_API_KEY
    }
    response = requests.get(url, params=params)
    return response.json()

directions = get_directions("India Gate, Delhi", "Red Fort, Delhi")

# Decode polyline to draw route on map
import polyline
route = directions["routes"][0]["overview_polyline"]["points"]
coords = polyline.decode(route)

import folium
from streamlit_folium import st_folium

m = folium.Map(location=coords[0], zoom_start=13)
folium.PolyLine(coords, color="blue", weight=5).add_to(m)
st_folium(m, width=725)
