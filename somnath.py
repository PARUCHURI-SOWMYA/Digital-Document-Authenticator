import streamlit as st
from PIL import Image, ImageOps, ImageFilter
import numpy as np
import io
from pdfminer.six import pdfinterp, pdfparser, pdfdocument, pdfpage, pdfpageaggregator, pdfdevice
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

def extract_text_from_pdf(pdf_file):
    output_string = io.StringIO()
    parser = pdfparser.PDFParser(pdf_file)
    doc = pdfdocument.PDFDocument(parser)
    if not doc.is_extractable:
        return ""
    rsrcmgr = pdfinterp.PDFResourceManager()
    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
    interpreter = pdfinterp.PDFPageInterpreter(rsrcmgr, device)
    for page in pdfpage.PDFPage.create_pages(doc):
        interpreter.process_page(page)
    return output_string.getvalue()

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
        pdf_text = extract_text_from_pdf(io.BytesIO(uploaded_file.getvalue()))
        text_pages = pdf_text.split("\f")
        total_pages = len(text_pages)
        page_number = st.number_input(f"Enter page number (1-{total_pages}) to authenticate", min_value=1, max_value=total_pages, step=1)
        
        if st.button("Process Document"):
            text = text_pages[page_number - 1] if page_number <= total_pages else "No text found"
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
