import streamlit as st
import cv2
import numpy as np
from PIL import Image

def process_image(image):
    img_array = np.array(image)
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    inverted = cv2.bitwise_not(gray)
    return gray, edges, inverted

def main():
    st.title("Digital Document Authenticator")
    st.write("Upload an academic certificate or ID proof (image format) to check for authenticity.")
    
    uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Original Document", use_column_width=True)
        gray, edges, inverted = process_image(image)
        
        st.image(gray, caption="Grayscale Version", use_column_width=True, channels="GRAY")
        st.image(edges, caption="Edge Detection", use_column_width=True, channels="GRAY")
        st.image(inverted, caption="Color Inverted", use_column_width=True, channels="GRAY")
        
        st.download_button(
            label="Download Grayscale Image",
            data=cv2.imencode(".png", gray)[1].tobytes(),
            file_name="grayscale.png",
            mime="image/png"
        )
        st.download_button(
            label="Download Edge Detection Image",
            data=cv2.imencode(".png", edges)[1].tobytes(),
            file_name="edges.png",
            mime="image/png"
        )
        st.download_button(
            label="Download Color Inverted Image",
            data=cv2.imencode(".png", inverted)[1].tobytes(),
            file_name="inverted.png",
            mime="image/png"
        )
            
if __name__ == "__main__":
    main()
