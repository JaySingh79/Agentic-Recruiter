# from utils.llm_client import call_llm

# async def generate_question(step: dict, matches: dict, res_struct: dict) -> str:
#     if step['type'] == 'behavioral':
#         prompt = """
# You are an interviewer. Ask a behavioral question about teamwork or problem-solving.
# """
#     elif step['type'] == 'technical':
#         skill = step['skills'][0] if step['skills'] else 'programming'
#         prompt = f"Generate a technical question testing {skill}."
#     elif step['type'] == 'case':
#         prompt = "Present a real-world scenario relevant to the role and ask the candidate to outline their approach."
#     else:
#         prompt = "Ask a closing question about candidate expectations and next steps."
#     return await call_llm(prompt)


import asyncio
import re
import json
from utils.llm_client import call_llm

async def generate_questions(jd: str, common_skills: list) -> list[str]:
    prompt = f"""
                You're an AI interviewer.

                Here are the job-description: {jd}
                Here is a candidate's skill profile: {common_skills}

                Generate 6 interview questions covering key technical concepts involved in job-description. Out of these atleast 2 questions should cover practical implementation of those technical skills.

                Return only the list of questions.
            """
    response_text = await call_llm(prompt)
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        pass

    # If not JSON, try regex for quoted text
    quoted = re.findall(r'"(.*?)"', response_text)
    if quoted:
        return quoted

    # Fallback: split lines, clean formatting
    lines = response_text.strip().split("\n")
    questions = []
    for line in lines:
        line = line.strip()
        if re.match(r"^\d+[\.\)]\s*", line):  # e.g., "1. " or "1) "
            line = re.sub(r"^\d+[\.\)]\s*", "", line)
        elif line.startswith("- "):
            line = line[2:]
        if line:
            questions.append(line)
    return questions


# class RecruiterAgent:
#     """
#     Conducts a 5-question technical interview based on a job description,
#     asking follow-ups when answers are vague.
#     """
#     def __init__(self, job_description: str, role: str, max_questions: int = 5):
#         self.job_description = job_description
#         self.role = role
#         self.max_questions = max_questions

#     async def run_interview(self):
#         print(f"Starting interview for {self.role}\n")
#         for i in range(1, self.max_questions + 1):
#             question = await self._ask_llm(
#                 f"You are a {self.role} interviewer. "
#                 f"Based on this job description, ask one focused technical question.\n"
#                 f"Job Description: {self.job_description}\n"
#                 f"Return only the question."
#             )
#             # print(f"Question {i}: {question}\n")
#             answer = await asyncio.to_thread(input, "Your answer: ")

#             followup = await self._ask_llm(
#                 f"Expert interviewer check:\nQuestion: {question}\n"
#                 f"Answer: {answer}\n"
#                 "If vague, ask a concise follow-up; otherwise reply 'NO_FOLLOWUP'."
#             )
#             if followup.strip().upper() != 'NO_FOLLOWUP':
#                 print(f"Follow-up: {followup}\n")
#                 await asyncio.to_thread(input, "Your follow-up answer: ")

#         #     print("-----\n")
#         # print("Interview complete. Thank you!")

#     async def _ask_llm(self, prompt: str) -> str:
#         try:
#             return (await call_llm(prompt)).strip()
#         except Exception as e:
#             print(f"Error calling LLM: {e}")
#             return ""

# if __name__ == '__main__':
#     import argparse

#     p = argparse.ArgumentParser()
#     p.add_argument('--role', '-r', required=True, help='Role title')
#     p.add_argument('--description', '-d', required=True, help='Full job description')
#     p.add_argument('--questions', '-n', type=int, default=5, help='Number of questions')
#     args = p.parse_args()

#     agent = RecruiterAgent(args.description, args.role, args.questions)
#     asyncio.run(agent.run_interview())
