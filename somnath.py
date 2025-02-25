import streamlit as st
from PIL import Image, ImageOps, ImageFilter
import PyPDF2
import docx

def display_pdf_pages(file, page_number):
    pdf_reader = PyPDF2.PdfReader(file)
    if page_number < 1 or page_number > len(pdf_reader.pages):
        st.error("Invalid page number")
        return
    
    page = pdf_reader.pages[page_number - 1]
    text = page.extract_text()
    if text:
        st.text_area(f"Page {page_number} Text", text, height=200)
    else:
        st.warning(f"Page {page_number} has no extractable text.")

def highlight_duplicate_text(text):
    words = text.split()
    word_count = {}
    highlighted_text = ""
    
    for word in words:
        if word in word_count:
            word_count[word] += 1
            highlighted_text += f"**{word}** "
        else:
            word_count[word] = 1
            highlighted_text += word + " "
    
    return highlighted_text.strip()

def check_text_duplicates(file):
    text = file.read().decode("utf-8")
    highlighted_text = highlight_duplicate_text(text)
    st.markdown(highlighted_text)

def process_image(image):
    gray = ImageOps.grayscale(image)
    st.image(gray, caption="Grayscale Image", use_column_width=True)
    
    edge = gray.filter(ImageFilter.FIND_EDGES)
    st.image(edge, caption="Edge Detection", use_column_width=True)
    
    inverted = ImageOps.invert(gray)
    st.image(inverted, caption="Inverted Image", use_column_width=True)

def extract_text_from_docx(file):
    doc = docx.Document(file)
    full_text = "\n".join([para.text for para in doc.paragraphs])
    return full_text

def main():
    st.title("Digital Document Authentication and Verification Tool")
    uploaded_file = st.file_uploader("Upload a document or image", type=["pdf", "txt", "docx", "png", "jpg", "jpeg"])
    
    if uploaded_file:
        file_type = uploaded_file.type
        
        if file_type == "application/pdf":
            st.subheader("PDF Text Display")
            page_number = st.number_input("Enter Page Number to Process", min_value=1, step=1)
            if st.button("Process PDF Page"):
                display_pdf_pages(uploaded_file, page_number)
        
        elif file_type == "text/plain":
            st.subheader("Text Duplication Check")
            check_text_duplicates(uploaded_file)
        
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            st.subheader("Word Document Text")
            extracted_text = extract_text_from_docx(uploaded_file)
            highlighted_text = highlight_duplicate_text(extracted_text)
            st.markdown(highlighted_text)
        
        elif file_type in ["image/png", "image/jpeg"]:
            st.subheader("Processed Image")
            image = Image.open(uploaded_file)
            process_image(image)

if __name__ == "__main__":
    main()
