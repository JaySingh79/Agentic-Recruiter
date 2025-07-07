import pymupdf  # Instead of: import fitz

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        pdf_bytes = uploaded_file.read()
        doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
        text = ""
        
        for page in doc:
            text += page.get_text() + "\n"  # Now recognized by Pylance
        
        doc.close()
        return text.strip()
