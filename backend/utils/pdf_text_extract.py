from pypdf import PdfReader

reader = PdfReader("test pdfs/Jay Singh Resume AI-ML-DS.pdf")
text_all = ""
for page in reader.pages:
    text_all+=page.extract_text()
    

with open("test pdfs/resume_text.txt", 'w', encoding='utf-8') as file:
    file.write(text_all)


