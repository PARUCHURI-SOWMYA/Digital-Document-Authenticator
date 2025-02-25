import streamlit as st
from PIL import Image, ImageOps, ImageFilter
import numpy as np
import io
import fitz  # PyMuPDF for PDF handling

def extract_text_from_pdf(pdf_file, page_number):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    if page_number - 1 < len(doc):
        page = doc[page_number - 1]
        return page.get_text("text")
    return ""

def process_image(image):
    grayscale_image = ImageOps.grayscale(image)
    edge_image = image.filter(ImageFilter.FIND_EDGES)
    invert_image = ImageOps.invert(grayscale_image)
    return grayscale_image, edge_image, invert_image

def check_document_authenticity(text):
    if "duplicate" in text.lower():
        return "Duplicate Document Detected"
    return "Original Document Detected"

# App Title
st.title("Digital Document Authenticator")

# File Upload Section
st.subheader("Upload Original Image or Document")
uploaded_file = st.file_uploader("Upload an image (jpg, png) or document (pdf)", type=["jpg", "jpeg", "png", "pdf"])

if uploaded_file is not None:
    file_extension = uploaded_file.name.split(".")[-1].lower()
    
    if file_extension in ["jpg", "jpeg", "png"]:
        st.write("### Original Image")
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        grayscale_image, edge_image, invert_image = process_image(image)
        
        st.write("### Authentication Image Outputs")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.image(grayscale_image, caption="Grayscale", use_column_width=True)
        with col2:
            st.image(edge_image, caption="Edge Detection", use_column_width=True)
        with col3:
            st.image(invert_image, caption="Inverted Colors", use_column_width=True)
    
    elif file_extension == "pdf":
        st.write("### PDF Document Uploaded")
        total_pages = len(fitz.open(stream=uploaded_file.read(), filetype="pdf"))
        page_number = st.number_input(f"Enter page number (1-{total_pages}) to authenticate", min_value=1, max_value=total_pages, step=1)
        
        if st.button("Process Document"):
            uploaded_file.seek(0)  # Reset file pointer after reading page count
            text = extract_text_from_pdf(uploaded_file, page_number)
            st.write("### Extracted Text from Selected Page")
            st.text(text)
            
            authenticity = check_document_authenticity(text)
            st.write(f"### Authenticity Check: {authenticity}")
            
            st.write("Document processing complete.")
else:
    st.warning("Please upload an image or document to process.")

# Footer
st.markdown("---")
st.write("Built with Streamlit for digital document authentication.")
