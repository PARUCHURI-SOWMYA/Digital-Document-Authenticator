import streamlit as st
from PIL import Image, ImageOps, ImageFilter
import os
import subprocess

# Function to convert PDF to image using Poppler's pdftoppm
def pdf_page_to_image(pdf_file, page_number):
    try:
        output_dir = "pdf_images"
        os.makedirs(output_dir, exist_ok=True)
        
        # Save the uploaded PDF temporarily
        pdf_path = os.path.join(output_dir, "temp.pdf")
        with open(pdf_path, "wb") as f:
            f.write(pdf_file.read())

        # Convert PDF to image using pdftoppm
        output_image_path = os.path.join(output_dir, f"page_{page_number}")
        command = ["pdftoppm", "-jpeg", "-f", str(page_number), "-l", str(page_number), pdf_path, output_image_path]
        subprocess.run(command, check=True)

        image_path = f"{output_image_path}-1.jpg"
        return Image.open(image_path) if os.path.exists(image_path) else None
    except Exception as e:
        st.error(f"Error processing PDF: {e}")
        return None

# Function to process an image
def process_image(image):
    grayscale_image = ImageOps.grayscale(image)
    edge_image = image.filter(ImageFilter.FIND_EDGES)
    invert_image = ImageOps.invert(grayscale_image)
    return grayscale_image, edge_image, invert_image

# Streamlit App Title
st.title("Digital Document Authenticator")

# File Upload Section
st.subheader("Upload an Image or PDF Document")
uploaded_file = st.file_uploader("Upload an image (JPG, PNG) or document (PDF)", type=["jpg", "jpeg", "png", "pdf"])

if uploaded_file is not None:
    file_extension = uploaded_file.name.split(".")[-1].lower()

    # Process Image Files
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

    # Process PDF Documents
    elif file_extension == "pdf":
        st.write("### PDF Document Uploaded")
        page_number = st.number_input("Enter page number to authenticate", min_value=1, step=1)

        if st.button("Process Document"):
            uploaded_file.seek(0)  # Reset file pointer
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

# Footer
st.markdown("---")
st.write("Built with Streamlit for digital document authentication.")
