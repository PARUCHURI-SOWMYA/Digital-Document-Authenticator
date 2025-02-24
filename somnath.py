import streamlit as st
from PIL import Image, ImageOps, ImageFilter
import os

# App Title
st.title("Digital Document Authenticator")

# File Upload Section
st.subheader("Upload Original Image")
original_image = st.file_uploader("Upload the original image to process", type=["jpg", "jpeg", "png"])

# Display and Process the Uploaded Image
if original_image is not None:
    st.write("### Original Image")
    
    # Open the uploaded image
    image = Image.open(original_image)
    st.image(image, caption="Original Image", use_column_width=True)

    # Display image details
    image_info = {
        "Image Type": original_image.type,
        "Image Format": image.format,
        "Image Size (in bytes)": len(original_image.getvalue()),
        "Image Dimensions (width x height)": f"{image.width} x {image.height}",
        "Image Mode": image.mode,
    }

    st.write("### Uploaded Image Details")
    for key, value in image_info.items():
        st.write(f"{key}: {value}")

    # Generate all three transformations
    grayscale_image = ImageOps.grayscale(image)
    edge_image = image.filter(ImageFilter.FIND_EDGES)
    invert_image = ImageOps.invert(grayscale_image)

    # Display all three processed images
    st.write("### Authentication Image Outputs")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(grayscale_image, caption="Grayscale", use_column_width=True)
        st.write("Grayscale: Converts the original image to grayscale, removing all color information. Helps in analyzing document texture and structure without color interference.")
    with col2:
        st.image(edge_image, caption="Edge Detection", use_column_width=True)
        st.write("Edge Detection: Highlights the edges of objects in the image. Useful for detecting tampering, alterations, or inconsistencies in document scans.")
    with col3:
        st.image(invert_image, caption="Inverted Colors", use_column_width=True)
        st.write("Inverted Colors: Inverts the grayscale image, swapping light and dark areas. Can help reveal hidden patterns, marks, or alterations not easily visible.")

    # Option to Download the Processed Images
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
    st.warning("Please upload an original image to process.")

# Footer
st.markdown("---")
st.write("Built with Streamlit for digital document authentication.")
