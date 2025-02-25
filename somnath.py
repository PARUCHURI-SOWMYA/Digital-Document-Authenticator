import streamlit as st
from PIL import Image, ImageOps, ImageFilter
import cv2
import numpy as np

def display_pdf_forensically(file):
    st.error("PDF processing without additional libraries is not supported. Convert PDF to images before uploading.")

def check_text_duplicates(file):
    text = file.read().decode("utf-8")
    lines = text.split("\n")
    unique_lines = set()
    duplicate_lines = set()
    
    for line in lines:
        stripped_line = line.strip()
        if stripped_line in unique_lines:
            duplicate_lines.add(stripped_line)
        else:
            unique_lines.add(stripped_line)
    
    if duplicate_lines:
        st.error("Duplicate lines found:")
        for line in duplicate_lines:
            st.write(f"- {line}")
    else:
        st.success("No duplicate lines found!")

def process_image(image):
    gray = ImageOps.grayscale(image)
    st.image(gray, caption="Grayscale Image", use_column_width=True)
    
    edge = gray.filter(ImageFilter.FIND_EDGES)
    st.image(edge, caption="Edge Detection", use_column_width=True)
    
    inverted = ImageOps.invert(gray)
    st.image(inverted, caption="Inverted Image", use_column_width=True)

def main():
    st.title("Digital Document Authentication and Verification Tool")
    uploaded_file = st.file_uploader("Upload a document or image", type=["pdf", "txt", "png", "jpg", "jpeg"])
    
    if uploaded_file:
        file_type = uploaded_file.type
        
        if file_type == "application/pdf":
            st.subheader("Forensic PDF View")
            display_pdf_forensically(uploaded_file)
        
        elif file_type == "text/plain":
            st.subheader("Text Duplication Check")
            check_text_duplicates(uploaded_file)
        
        elif file_type in ["image/png", "image/jpeg"]:
            st.subheader("Processed Image")
            image = Image.open(uploaded_file)
            process_image(image)

if __name__ == "__main__":
    main()
