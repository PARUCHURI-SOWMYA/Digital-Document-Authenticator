import streamlit as st
import cv2
import numpy as np
import pytesseract
from PyPDF2 import PdfReader
from pdf2image import convert_from_bytes
import difflib

def preprocess_image(image, mode):
    if mode == "Grayscale":
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif mode == "Edge Detection":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.Canny(gray, 100, 200)
    elif mode == "Color Inversion":
        return cv2.bitwise_not(image)
    return image

def extract_text(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text

def highlight_changes(original_text, modified_text):
    diff = difflib.ndiff(original_text.split(), modified_text.split())
    highlighted = " ".join([f'**{word}**' if word.startswith('+') else word for word in diff])
    return highlighted

def main():
    st.title("Digital Document Authenticator and Verification Tool")
    uploaded_file = st.file_uploader("Upload a PDF Document", type=["pdf"])
    
    if uploaded_file:
        pages = convert_from_bytes(uploaded_file.read())
        selected_page = st.selectbox("Select a page to verify", list(range(1, len(pages) + 1)))
        
        if selected_page:
            image_np = np.array(pages[selected_page - 1])
            st.image(image_np, caption="Original Page", use_column_width=True)
            
            mode = st.radio("Select Processing Mode", ["Grayscale", "Edge Detection", "Color Inversion"])
            processed_image = preprocess_image(image_np, mode)
            st.image(processed_image, caption=f"Processed ({mode})", use_column_width=True, channels="GRAY" if mode == "Grayscale" else "RGB")
            
            # Extract and verify text
            original_text = extract_text(image_np)
            modified_text = extract_text(processed_image)
            highlighted_text = highlight_changes(original_text, modified_text)
            
            st.subheader("Text Verification Result")
            st.write(highlighted_text)
            
            st.subheader("Before & After Document View")
            col1, col2 = st.columns(2)
            with col1:
                st.text("Original Document")
                st.image(image_np, use_column_width=True)
            with col2:
                st.text("Processed Document")
                st.image(processed_image, use_column_width=True)

if __name__ == "__main__":
    main()
