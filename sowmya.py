import streamlit as st
from PIL import Image, ImageOps, ImageFilter
from pdf2image import convert_from_path
import pytesseract
import cv2
import numpy as np

def pdf_to_images(pdf_file):
    images = convert_from_path(pdf_file)
    return images

def extract_text(image):
    text = pytesseract.image_to_string(image)
    return text

def detect_tampering(original_text, new_text):
    original_lines = original_text.splitlines()
    new_lines = new_text.splitlines()
    tampered_lines = []
    for i in range(max(len(original_lines), len(new_lines))):
        if i >= len(original_lines) or i >= len(new_lines) or original_lines[i] != new_lines[i]:
            tampered_lines.append(i)
    return tampered_lines

def highlight_tampered_text(original_text, tampered_lines):
    highlighted_text = original_text.splitlines()
    for line in tampered_lines:
        highlighted_text[line] = f"**{highlighted_text[line]}**"
    return "\n".join(highlighted_text)

st.title("Digital Document Authenticator and Verification Tool")

uploaded_file = st.file_uploader("Upload the document to process", type=["pdf"])

if uploaded_file is not None:
    images = pdf_to_images(uploaded_file)
    page_numbers = [f"Page {i+1}" for i in range(len(images))]
    page_selected = st.selectbox("Select the page to verify", page_numbers)
    page_index = page_numbers.index(page_selected)
    selected_image = images[page_index]

    st.write(f"### Selected Page: {page_selected}")
    st.image(selected_image, caption=f"Page {page_index+1}", use_column_width=True)

    grayscale_image = ImageOps.grayscale(selected_image)
    edge_image = selected_image.filter(ImageFilter.FIND_EDGES)
    invert_image = ImageOps.invert(grayscale_image)

    st.write("### Authentication Image Outputs")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(grayscale_image, caption="Grayscale", use_column_width=True)
        st.write("Grayscale: Highlights alterations in document texture.")
    with col2:
        st.image(edge_image, caption="Edge Detection", use_column_width=True)
        st.write("Edge Detection: Detects tampered areas based on edge misalignment.")
    with col3:
        st.image(invert_image, caption="Inverted Colors", use_column_width=True)
        st.write("Inverted Colors: Reveals hidden marks, watermarks, or text alterations.")

    original_text = extract_text(selected_image)
    new_text = original_text + "\nThis is a tampered line."
    tampered_lines = detect_tampering(original_text, new_text)

    st.write("### Text Verification Results")
    st.write("Original Text:")
    st.code(original_text)
    st.write("Tampered Text:")
    st.code(highlight_tampered_text(new_text, tampered_lines))
    if tampered_lines:
        st.warning("Tampering detected on lines: " + ", ".join(map(str, tampered_lines)))
    else:
        st.success("No tampering detected.")

    st.write("### Before and After Document Comparison")
    col1, col2 = st.columns(2)
    with col1:
        st.image(selected_image, caption="Original Document", use_column_width=True)
    with col2:
        st.image(invert_image, caption="Tampered Document", use_column_width=True)

else:
    st.warning("Please upload a PDF document to process.")
