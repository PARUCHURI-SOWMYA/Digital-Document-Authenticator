import os
import cv2
import pytesseract
import numpy as np
from PIL import Image
import streamlit as st
from pdf2image import convert_from_path

# Set up Tesseract if needed (on Windows, adjust the path accordingly)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Directories for storing uploads and processed images
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Streamlit Interface for Uploading Document
st.title("Digital Document Authenticator and Verification Tool")

st.sidebar.title("Upload Your Document")
uploaded_file = st.sidebar.file_uploader("Choose a PDF or image file", type=['pdf', 'jpg', 'jpeg', 'png'])

if uploaded_file:
    # Save uploaded file to the system
    uploaded_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(uploaded_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.sidebar.success(f"Uploaded {uploaded_file.name}")

    # Convert PDF to images if the uploaded file is a PDF
    if uploaded_file.name.endswith('.pdf'):
        images = convert_from_path(uploaded_path)
        image_filenames = []
        for i, img in enumerate(images):
            img_filename = os.path.join(PROCESSED_FOLDER, f'page_{i + 1}.png')
            img.save(img_filename, 'PNG')
            image_filenames.append(img_filename)
        
        selected_page = st.selectbox("Select a Page", range(len(image_filenames)))
        selected_image_path = image_filenames[selected_page]
    else:
        selected_image_path = uploaded_path

    # Display the selected page/image
    st.image(selected_image_path, caption="Selected Document Page", use_column_width=True)

    # Choose Output Mode
    mode = st.selectbox("Choose Output Mode", ["Original", "Greyscale", "Edge Detection", "Color Inversion"])

    # Apply the selected mode
    image = cv2.imread(selected_image_path)

    if mode == "Greyscale":
        processed_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif mode == "Edge Detection":
        processed_image = cv2.Canny(image, 100, 200)
    elif mode == "Color Inversion":
        processed_image = cv2.bitwise_not(image)
    else:
        processed_image = image

    # Show the processed image
    if mode != "Original":
        st.image(processed_image, caption=f"Processed Document ({mode})", use_column_width=True)
    
    # OCR Text Extraction
    if st.button("Extract Text"):
        extracted_text = pytesseract.image_to_string(processed_image)
        st.text_area("Extracted Text", extracted_text, height=300)

    # Option to download the processed image
    processed_image_filename = os.path.join(PROCESSED_FOLDER, f"processed_{mode}_{uploaded_file.name}")
    cv2.imwrite(processed_image_filename, processed_image)
    st.download_button("Download Processed Image", processed_image_filename, file_name=f"processed_{mode}_{uploaded_file.name}")
