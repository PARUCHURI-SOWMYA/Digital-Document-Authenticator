import streamlit as st
import numpy as np
from PIL import Image, ImageOps, ImageFilter
import pytesseract

def process_image(image):
    gray = ImageOps.grayscale(image)
    edges = gray.filter(ImageFilter.FIND_EDGES)
    inverted = ImageOps.invert(gray)
    return gray, edges, inverted

def detect_duplicate_text(image):
    text = pytesseract.image_to_string(image)
    words = text.split()
    duplicates = {word for word in words if words.count(word) > 1}
    return text, duplicates

def main():
    st.title("Digital Document Authenticator")
    st.write("Upload an academic certificate or ID proof (image format) to check for authenticity.")
    
    uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Original Document", use_column_width=True)
        gray, edges, inverted = process_image(image)
        
        st.image(gray, caption="Grayscale Version", use_column_width=True)
        st.image(edges, caption="Edge Detection", use_column_width=True)
        st.image(inverted, caption="Color Inverted", use_column_width=True)
        
        extracted_text, duplicates = detect_duplicate_text(gray)
        st.subheader("Extracted Text")
        st.text_area("Text from Image", extracted_text, height=200)
        
        if duplicates:
            st.subheader("Duplicate Words Found")
            st.write(", ".join(duplicates))
        else:
            st.write("No duplicate words found.")
        
        st.download_button(
            label="Download Grayscale Image",
            data=gray.tobytes(),
            file_name="grayscale.png",
            mime="image/png"
        )
        st.download_button(
            label="Download Edge Detection Image",
            data=edges.tobytes(),
            file_name="edges.png",
            mime="image/png"
        )
        st.download_button(
            label="Download Color Inverted Image",
            data=inverted.tobytes(),
            file_name="inverted.png",
            mime="image/png"
        )
            
if __name__ == "__main__":
    main()
