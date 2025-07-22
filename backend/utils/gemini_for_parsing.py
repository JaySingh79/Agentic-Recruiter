from google import genai
from dotenv import load_dotenv
from pypdf import PdfReader
import asyncio
import re

load_dotenv()


# reader = PdfReader("test pdfs/Jay Singh Resume AI-ML-DS.pdf")
# text_all = ""
# for page in reader.pages:
#     text_all+=page.extract_text()


# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()

async def gemini_client(prompt):
    response = client.models.generate_content(
        model="models/gemini-2.5-flash-lite-preview-06-17", contents=prompt
    )
    return response.text


# text_all = text_all.replace("\n", " ").strip()

async def resume_parser(resume_text):
    
    
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
    
    lines = ans.strip().split('\n')
    skill_lines = []
    for line in lines:
        # Remove common introductory phrases
        if re.match(r'^\s*(technical skills|skills|list of skills)\s*[:\-]*\s*$', line, re.I):
            continue
        skill_lines.append(line.strip())

    # Join lines for further processing
    text = '\n'.join(skill_lines)

    # Try to extract comma-separated list in a single line
    # e.g., "Python, Java, SQL, React"
    if ',' in text and '\n' not in text.strip(','):
        skills = [s.strip() for s in text.split(',') if s.strip()]
        return skills

    # Otherwise, extract bullet points or numbered lists
    bullets = re.findall(r'^[\-\*\d\.\)]*\s*([A-Za-z0-9\+\#\.\- ]+)$', text, re.M)
    if bullets:
        # Remove any empty or generic lines
        skills = [s.strip() for s in bullets if s.strip() and len(s.strip()) > 1]
        return skills

    # Fallback: extract quoted skills
    quoted = re.findall(r'"([^"]+)"', text)
    if quoted:
        return [q.strip() for q in quoted if q.strip()]

    # Final fallback: split by newlines or semicolons
    skills = []
    for line in text.split('\n'):
        for part in re.split(r',|;', line):
            skill = part.strip()
            if skill and len(skill) > 1:
                skills.append(skill)
    return skills

    # print(ans)
    

async def jd_parser(jd_text: str):

    # resume_text = text_all.replace("\n", " ").strip()
    prompt = f"""
            You are a highly experienced HR professional with 20 years of expertise in talent acquisition and resume evaluation.

            Task:
            Extract all technical skills required or preferred in the following job description.
            Technical skills include programming languages, frameworks, software, tools, libraries, platforms, and technical methodologies.

            Instructions:
            Return only a clean list of technical skills(string), strictly without any text/character/alphanumeric; take reference from Output Format.
            Exclude soft skills, languages spoken, and general traits.

            Output Format:
            ['python', 'sql', 'docker', 'llm', 'aws', 'deep learning']
            
            Job Description:
            {jd_text}
    
            """
            
    ans = await gemini_client(prompt)
    
    lines = ans.strip().split('\n')
    skill_lines = []
    for line in lines:
        # Remove common introductory phrases
        if re.match(r'^\s*(technical skills|skills|list of skills)\s*[:\-]*\s*$', line, re.I):
            continue
        skill_lines.append(line.strip())

    # Join lines for further processing
    text = '\n'.join(skill_lines)

    # Try to extract comma-separated list in a single line
    # e.g., "Python, Java, SQL, React"
    if ',' in text and '\n' not in text.strip(','):
        skills = [s.strip() for s in text.split(',') if s.strip()]
        return skills

    # Otherwise, extract bullet points or numbered lists
    bullets = re.findall(r'^[\-\*\d\.\)]*\s*([A-Za-z0-9\+\#\.\- ]+)$', text, re.M)
    if bullets:
        # Remove any empty or generic lines
        skills = [s.strip() for s in bullets if s.strip() and len(s.strip()) > 1]
        return skills

    # Fallback: extract quoted skills
    quoted = re.findall(r'"([^"]+)"', text)
    if quoted:
        return [q.strip() for q in quoted if q.strip()]

    # Final fallback: split by newlines or semicolons
    skills = []
    for line in text.split('\n'):
        for part in re.split(r',|;', line):
            skill = part.strip()
            if skill and len(skill) > 1:
                skills.append(skill)
    return skills

    # print(ans)    


jobdescrip = """
                About the job

                Job Title: LLM Engineer
                Department: Engineering
                Location: Bangalore
                Years of Experience: 2-5 years
                Employment Type: Full-time, Permanent
                Key Relationships: Director - Engineering
                We are looking for an LLM Engineer to accelerate our generative AI roadmap by building scalable, production-grade systems that leverage large language models across healthcare workflows. This role goes beyond prompt design, you’ll own the end-to-end application of LLMs, from architecting internal tools and APIs to ensuring robust performance, usability, and compliance in real-world deployments. If you're passionate about building the foundational tech to make LLMs work reliably in critical settings, we want to talk to you.


                Key Responsibilities

                Design and implement LLM-based features across Qure’s products, from clinician-facing assistants to automated diagnostic flows.
                Build internal tools, APIs, and developer-facing utilities to enable scalable LLM integrations.
                Collaborate with prompt engineers to design modular, composable workflows (e.g., RAG, chaining, structured prompting).
                Evaluate model performance and behavior across tasks using both human feedback and automated metrics.

                Optimize latency, cost, and reliability of LLM systems using caching, batching, and fallback strategies.
                Deploy and monitor LLM services in production, integrating observability and usage analytics.
                Build systems to manage prompt versioning, LLM configurations, and multi-model experimentation.
                Lead cross-functional initiatives and drive end-to-end project execution across engineering, product, and clinical teams.
                Contribute to internal LLM guidelines, safety practices, and developer enablement.
                Foster a culture of collaboration, ownership, and technical excellence in building impactful LLM-driven solutions.


                Required Skills and Qualifications

                Bachelor’s degree in Computer Science, Information Technology, or a related field.
                Solid understanding of LLM architectures, inference workflows, context management, and prompt patterns.
                Strong programming skills in Python, familiarity with frameworks like LangChain, Haystack, or Pydantic AI.
                Experience integrating OpenAI, Anthropic, or open-source models into production systems.
                Familiarity with emerging LLM protocols such as MCP and frameworks that enable agentic behaviours (e.g., autonomous agents, task decomposition, memory systems)
                Proven ability to work across infra, product, and research teams.
                Comfort with cloud platforms (AWS/GCP), containerized deployments (Docker/K8s), and observability tools.
                Solid understanding of how to set up guardrails around LLMs to ensure responsible, safe, and reliable usage in production systems.
                Strong problem-solving, communication, and cross-functional collaboration skills.


                Preferred Skills

                Experience in the healthcare industry, with an understanding of compliance and security requirements.
                Experience building user-facing tools or assistants powered by LLMs.
                Strong sense of ownership and ability to balance experimentation with production-readiness.
                Familiarity with agile methodologies and project management practices.

            """


# asyncio.run(jd_parser(jobdescrip))

