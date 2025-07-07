# importing required modules
from pypdf import PdfReader

# creating a pdf reader object
reader = PdfReader("test pdfs\\New Resume with Projects.pdf")

# printing number of pages in pdf file
print(len(reader.pages))

# getting a specific page from the pdf file
page = reader.pages[0]

# extracting text from page
text = page.extract_text()
with open('test.txt', 'w', encoding="utf-8") as file:
    file.write(text)
    
print(text)