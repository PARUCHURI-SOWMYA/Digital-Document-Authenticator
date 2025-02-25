import streamlit as st
from PIL import Image, ImageOps, ImageFilter
import os
import subprocess
import shutil

# Set ImageMagick Path (Modify for your system if needed)

DEFAULT_IMAGEMAGICK_PATH = r"C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"  # Adjust as needed
IMAGE_MAGICK_PATH = shutil.which("magick") or DEFAULT_IMAGEMAGICK_PATH
def check_imagemagick():
    """Check if ImageMagick is installed and supports PDF."""
    if not IMAGE_MAGICK_PATH:
        return False, "ImageMagick is not installed. Please install it and restart the app."
    
    try:
        result = subprocess.run([IMAGE_MAGICK_PATH, "-list", "format"], capture_output=True, text=True)
        if "PDF" not in result.stdout:
            return False, "ImageMagick is installed but does not support PDF processing. Install Ghostscript."
    except Exception as e:
        return False, f"Error checking ImageMagick: {e}"
    
    return True, "ImageMagick is installed and ready to use!"

# Check ImageMagick installation
installed, message = check_imagemagick()
if not installed:
    st.error(message)
else:
    st.success(message)

def pdf_page_to_image(pdf_file, page_number):
    """Convert a PDF page to an image using ImageMagick."""
    try:
        output_dir = "pdf_images"
        os.makedirs(output_dir, exist_ok=True)
        pdf_path = os.path.join(output_dir, "temp.pdf")
        
        with open(pdf_path, "wb") as f:
            f.write(pdf_file.read())
        
        output_image_path = os.path.join(output_dir, f"page_{page_number}.jpg")
        command = [IMAGE_MAGICK_PATH, "convert", f"{pdf_path}[{page_number - 1}]", output_image_path]
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode != 0:
            st.error(f"ImageMagick error: {result.stderr}")
            return None
        
        if os.path.exists(output_image_path):
            return Image.open(output_image_path)
        else:
            st.error("ImageMagick failed to process the PDF.")
            return None
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return None

def process_image(image):
    grayscale_image = ImageOps.grayscale(image)
    edge_image = image.filter(ImageFilter.FIND_EDGES)
    invert_image = ImageOps.invert(grayscale_image)
    return grayscale_image, edge_image, invert_image

# Streamlit App
st.title("Digital Document Authenticator")
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
        page_number = st.number_input("Enter page number to authenticate", min_value=1, step=1)
        
        if st.button("Process Document"):
            uploaded_file.seek(0)
            image = pdf_page_to_image(uploaded_file, page_number)
            
            if image is not None:
                st.write("### Extracted Page as Image")
                st.image(image, caption=f"Page {page_number}", use_column_width=True)
                
                grayscale_image, edge_image, invert_image = process_image(image)
                
                st.write("### Authentication Image Outputs")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.image(grayscale_image, caption="Grayscale", use_column_width=True)
                with col2:
                    st.image(edge_image, caption="Edge Detection", use_column_width=True)
                with col3:
                    st.image(invert_image, caption="Inverted Colors", use_column_width=True)
            else:
                st.error("Invalid page number or unable to process the document.")
else:
    st.warning("Please upload an image or document to process.")

st.markdown("---")
st.write("Built with Streamlit for digital document authentication.")
