import os
import streamlit as st
import numpy as np
import tensorflow as tf
import requests
import speech_recognition as sr
import pyttsx3
from PIL import Image
from io import BytesIO

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Load pre-trained leaf classification model (update model path as needed)
model_path = 'leaf_classifier_model.h5'  # Adjust this path
try:
    model = tf.keras.models.load_model(model_path)
except FileNotFoundError:
    st.write(f"Error: Model file not found at {model_path}. Please ensure the model file is present.")
    raise

# Set up text-to-speech engine
engine = pyttsx3.init()

# Function to classify leaf
def classify_leaf(image):
    # Preprocess image for model input (resize, normalization, etc.)
    image = image.resize((224, 224))  # Resize to model input size
    image_array = np.array(image) / 255.0  # Normalize
    image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension

    # Predict class
    prediction = model.predict(image_array)
    class_index = np.argmax(prediction)
    
    # You can add labels for the classes here
    classes = ['Vegetable', 'Fruit', 'Other']
    return classes[class_index]

# Function to get weather forecast from Open-Meteo API
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

# Function to handle voice input
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening for your voice...")
        audio = recognizer.listen(source)
        try:
            speech_text = recognizer.recognize_google(audio)
            st.write(f"You said: {speech_text}")
            return speech_text
        except Exception as e:
            st.write("Sorry, I could not understand your speech. Please try again.")
            return ""

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

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
    speak(f"The leaf is classified as: {leaf_type}")

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
        speak(weather_info)
    else:
        st.write("Location not found.")
        speak("Sorry, I could not find weather information for that location.")

# Voice command section
st.header("Voice Interaction")
if st.button("Ask a Question"):
    speech_text = recognize_speech()
    if "weather" in speech_text.lower():
        location = "Hyderabad"  # For simplicity, we can set a default location
        weather_info = get_weather(location_coords.get(location, (17.385044, 78.486671)))
        speak(weather_info)
    else:
        speak("I'm sorry, I can only help with weather queries right now.")
