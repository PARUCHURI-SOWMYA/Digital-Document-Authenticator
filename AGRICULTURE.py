import os
import streamlit as st
import requests
from PIL import Image

# Function to classify leaf (simplified, hardcoded)
def classify_leaf(image):
    # For now, we will just check for common leaf types based on simple image attributes.
    # This is a placeholder for the actual classification model.
    # In real-life use, you would load your machine learning model here.
    
    image = image.convert('RGB')  # Ensure the image is in RGB format
    width, height = image.size
    
    # Simple check based on dimensions (as an example)
    if width < 200 and height < 200:
        return "Small Leaf (Could be a herb)"
    elif width > 400 and height > 400:
        return "Large Leaf (Could be a tree)"
    else:
        return "Unknown Leaf Type (Could be a fruit or vegetable)"

# Function to get weather forecast (Open-Meteo API)
def get_weather(location):
    lat, lon = location  # Convert location to lat and lon (you can improve this step)
    url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true'
    response = requests.get(url)
    weather_data = response.json()

    # Extract relevant information
    temperature = weather_data['current_weather']['temperature']
    description = weather_data['current_weather']['weathercode']
    
    # Return a text response
    return f"The current temperature is {temperature}°C. Weather description: {description}"

# Streamlit UI
st.title("Agriculture Helper Chatbot")

# Leaf classification part
st.header("Leaf Classification")
uploaded_image = st.file_uploader("Upload an image of a leaf", type=["jpg", "jpeg", "png"])
if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Leaf Image", use_column_width=True)
    leaf_type = classify_leaf(image)
    st.write(f"The leaf is classified as: {leaf_type}")

# Weather forecasting part
st.header("Weather Forecasting")
location = st.text_input("Enter location (e.g., 'Hyderabad, India')", "Hyderabad")
if st.button("Get Weather Forecast"):
    # Here you can use a geocoding service to convert location to lat/lon, for simplicity, using fixed lat/lon
    location_coords = {
        "Hyderabad": (17.385044, 78.486671),  # Latitude, Longitude for Hyderabad
        "Bangalore": (12.971598, 77.594566),  # Latitude, Longitude for Bangalore
    }
    if location in location_coords:
        weather_info = get_weather(location_coords[location])
        st.write(weather_info)
    else:
        st.write("Location not found.")
