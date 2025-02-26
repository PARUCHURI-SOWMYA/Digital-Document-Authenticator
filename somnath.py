import streamlit as st
from PIL import Image, ImageOps, ImageFilter
from pdf2image import convert_from_path

# Function to convert PDF to images (one per page)
def pdf_to_images(pdf_file):
    images = convert_from_path(pdf_file)
    return images  # Return a list of images, one for each page in the PDF

# App Title
st.title("Digital Document Authenticator")

# File Upload Section
st.subheader("Upload Document (PDF or Image)")
original_document = st.file_uploader("Upload the document to process", type=["jpg", "jpeg", "png", "pdf"])

# Process the document when uploaded
if original_document is not None:
    if original_document.type == "application/pdf":
        # Convert PDF to images
        images = pdf_to_images(original_document)
        
        # Show page selection dropdown
        page_numbers = [f"Page {i+1}" for i in range(len(images))]
        page_selected = st.selectbox("Select the page to verify", page_numbers)

        # Get the selected page (0-indexed)
        page_index = page_numbers.index(page_selected)
        selected_image = images[page_index]

        # Display the original page
        st.write(f"### Selected Page: {page_selected}")
        st.image(selected_image, caption=f"Page {page_index+1}", use_column_width=True)

    else:
        # If it's an image, open it directly
        selected_image = Image.open(original_document)
        st.image(selected_image, caption="Original Image", use_column_width=True)

    # Process the selected page/image
    grayscale_image = ImageOps.grayscale(selected_image)
    edge_image = selected_image.filter(ImageFilter.FIND_EDGES)
    invert_image = ImageOps.invert(grayscale_image)

    # Display all processed images with descriptions
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

    # Option to download the processed images
    st.write("### Download Authentication Images")
    grayscale_image.save("grayscale_output.png")
    edge_image.save("edge_output.png")
    invert_image.save("invert_output.png")

    col1, col2, col3 = st.columns(3)
    with col1:
        with open("grayscale_output.png", "rb") as file:
            st.download_button("Download Grayscale", data=file, file_name="grayscale_output.png", mime="image/png")
    with col2:
        with open("edge_output.png", "rb") as file:
            st.download_button("Download Edge Detection", data=file, file_name="edge_output.png", mime="image/png")
    with col3:
        with open("invert_output.png", "rb") as file:
            st.download_button("Download Inverted Colors", data=file, file_name="invert_output.png", mime="image/png")
else:
    st.warning("Please upload an original image or PDF to process.")

# Footer
st.markdown("---")
st.write("Built with Streamlit for digital document authentication.")
