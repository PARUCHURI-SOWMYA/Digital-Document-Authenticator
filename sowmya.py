import streamlit as st
from PIL import Image, ImageOps, ImageFilter
from pdf2image import convert_from_bytes
import pytesseract
from io import BytesIO
import os

# Install required packages if not available
try:
    import pdf2image
    import pytesseract
    from PIL import Image, ImageOps, ImageFilter
except ImportError:
    os.system('pip install pdf2image pytesseract Pillow')
    import pdf2image
    import pytesseract
    from PIL import Image, ImageOps, ImageFilter

# App Title
st.title("Digital Document Authenticator")

# File Upload Section
st.subheader("Upload Document (Image or PDF)")
document = st.file_uploader("Upload an image (JPG, PNG) or PDF", type=["jpg", "jpeg", "png", "pdf"])

if document is not None:
    # Process PDF or Image
    if document.type == "application/pdf":
        st.write("### Extracting First Page from PDF")
        images = convert_from_bytes(document.read())
        image = images[0]  # Process only the first page
    else:
        image = Image.open(document)
    
    # Display Original Image
    st.image(image, caption="Original Document", use_column_width=True)
    
    # Display Image Details
    image_info = {
        "Image Type": document.type,
        "Image Dimensions": f"{image.width} x {image.height}",
        "Image Mode": image.mode,
    }
    
    st.write("### Document Details")
    for key, value in image_info.items():
        st.write(f"{key}: {value}")
    
    # Document Authentication Processing Options
    st.write("### Authentication Processing Options")
    process_type = st.selectbox("Select the transformation:", 
                                ["Grayscale", "Edge Detection", "Invert Colors", "Extract Text"])
    
    # Process Image
    if process_type == "Grayscale":
        auth_image = ImageOps.grayscale(image)
    elif process_type == "Edge Detection":
        auth_image = image.filter(ImageFilter.CONTOUR)
    elif process_type == "Invert Colors":
        auth_image = ImageOps.invert(image.convert("RGB"))
    elif process_type == "Extract Text":
        extracted_text = pytesseract.image_to_string(image)
        st.write("### Extracted Text")
        st.text_area("Text from Document:", extracted_text, height=200)
        auth_image = None
    
    # Display Processed Image
    if auth_image:
        st.write("### Processed Image Output")
        st.image(auth_image, caption="Authenticated Output", use_column_width=True)
    
        # Download Processed Image
        img_byte_arr = BytesIO()
        auth_image.save(img_byte_arr, format="PNG")
        st.download_button("Download Processed Image", data=img_byte_arr.getvalue(), file_name="processed_image.png", mime="image/png")
else:
    st.warning("Please upload a document to process.")

# Footer
st.markdown("---")
st.write("Built with Streamlit for digital document authentication.")
