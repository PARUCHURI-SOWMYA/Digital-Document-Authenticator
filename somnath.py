import streamlit as st
from PIL import Image, ImageOps, ImageFilter
import PyPDF2
import io

# Function to extract images from a PDF using PyPDF2
def pdf_to_images(pdf_file):
    try:
        images = []
        reader = PyPDF2.PdfReader(pdf_file)
        
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            if "/XObject" in page["/Resources"]:
                xObject = page["/Resources"]["/XObject"].get_object()
                for obj in xObject:
                    if xObject[obj]["/Subtype"] == "/Image":
                        data = xObject[obj]._data
                        image = Image.open(io.BytesIO(data))
                        images.append(image)
        return images
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return None

# Function to process an image
def process_image(image):
    grayscale_image = ImageOps.grayscale(image)
    edge_image = image.filter(ImageFilter.FIND_EDGES)
    invert_image = ImageOps.invert(grayscale_image)
    return grayscale_image, edge_image, invert_image

# Streamlit UI
st.title("Digital Document Authenticator")

# File Upload
st.subheader("Upload an Image or PDF")
uploaded_file = st.file_uploader("Upload a JPG, PNG, or PDF", type=["jpg", "jpeg", "png", "pdf"])

if uploaded_file is not None:
    file_extension = uploaded_file.name.split(".")[-1].lower()
    
    # If an image is uploaded
    if file_extension in ["jpg", "jpeg", "png"]:
        st.write("### Uploaded Image")
        image = Image.open(uploaded_file)
        st.image(image, caption="Original Image", use_column_width=True)

        # Process image
        grayscale_image, edge_image, invert_image = process_image(image)

        st.write("### Processed Outputs")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.image(grayscale_image, caption="Grayscale", use_column_width=True)
        with col2:
            st.image(edge_image, caption="Edge Detection", use_column_width=True)
        with col3:
            st.image(invert_image, caption="Inverted Colors", use_column_width=True)

    # If a PDF is uploaded
    elif file_extension == "pdf":
        st.write("### PDF Uploaded")
        images = pdf_to_images(uploaded_file)  # Convert PDF to images
        
        if images:
            total_pages = len(images)
            page_number = st.number_input(f"Enter page number (1-{total_pages})", min_value=1, max_value=total_pages, step=1)

            if st.button("Process Page"):
                image = images[page_number - 1]
                st.image(image, caption=f"Extracted Page {page_number}", use_column_width=True)

                # Process image
                grayscale_image, edge_image, invert_image = process_image(image)

                st.write("### Processed Outputs")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.image(grayscale_image, caption="Grayscale", use_column_width=True)
                with col2:
                    st.image(edge_image, caption="Edge Detection", use_column_width=True)
                with col3:
                    st.image(invert_image, caption="Inverted Colors", use_column_width=True)
        else:
            st.error("Could not process PDF!")

else:
    st.warning("Please upload an image or document.")

# Footer
st.markdown("---")
st.write("Built with Streamlit for digital document authentication.")
