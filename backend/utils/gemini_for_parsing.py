from google import genai
from dotenv import load_dotenv
from pypdf import PdfReader
import asyncio

load_dotenv()


reader = PdfReader("test pdfs/Jay Singh Resume AI-ML-DS.pdf")
text_all = ""
for page in reader.pages:
    text_all+=page.extract_text()


# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()

async def gemini_client(prompt):
    response = client.models.generate_content(
        model="models/gemini-2.5-flash-lite-preview-06-17", contents=prompt
    )
    return response.text



async def resume_parser():
    
    resume_text = text_all.replace("\n", " ").strip()
    prompt = f"""
    You are a highly experienced HR professional with 20 years of expertise in talent acquisition and resume evaluation.

    Task:
    Given the following Resume Text, identify and extract all technical skills explicitly mentioned in the Resume.

    Definition:
    Technical Skills include (this is just for reference):

    Programming languages (e.g., Python, Java, SQL)
    Software tools and platforms (e.g., Excel, Tableau, Salesforce)
    Frameworks and libraries (e.g., React, TensorFlow, Django)
    Technical methodologies or techniques (e.g., Agile, DevOps, Data Analysis)
    Specialized technologies or systems (e.g., AWS, Docker, SAP)
    
    Instructions:

    - Exclude soft skills, personal traits, languages spoken, or general education.
    - Extract all technical skills, including programming languages, frameworks, software, and libraries, explicitly mentioned in "Skills" or similar sections.
    - Return the answer as a clean list of technical skills(string format) only, with strictly no additional text/characters/numbers.

    Output Format:
    ['python', 'sql', 'Machine Learning', 'LLMs', 'React', 'Flask']

    Resume Text:
    {resume_text}
    
    """
    ans = await gemini_client(prompt)
    print(ans)
    

async def jd_parser(jd_text: str):

    

asyncio.run(resume_parser())
