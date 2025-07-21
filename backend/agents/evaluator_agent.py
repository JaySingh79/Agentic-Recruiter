# from utils.llm_client import call_llm

# async def evaluate_and_feedback(question: str, answer: str) -> dict:
#     prompt = (
#         f"Evaluate the candidate's answer. Provide a numeric score (1-5) and a concise feedback message.\n"
#         f"Question: {question}\nAnswer: {answer}"
#     )
#     resp = await call_llm(prompt)
#     # Parse score and feedback naively
#     parts = resp.split('\n', 1)
#     score_line = parts[0] if parts else ''
#     feedback_text = parts[1].strip() if len(parts) > 1 else ''
#     eval_res = {'score_line': score_line, 'feedback': feedback_text}
#     return eval_res

import re
from utils.llm_client import call_llm

async def evaluate_and_feedback(question: str, answer: str) -> tuple[dict, str]:
    prompt = f"""
                You're an experienced technical interviewer.

                Evaluate the candidate's answer to the following question.

                Question: {question}
                Answer: {answer}

                Return your evaluation in this exact format:

                Score: <1 to 5>
                Feedback: <short comment>
                Follow-up: <Yes or No>
            """

    response = await call_llm(prompt)

    # Regex parsing (robust)
    score_match = re.search(r"Score:\s*(\d)", response)
    fb_match    = re.search(r"Feedback:\s*(.+)", response)
    fup_match   = re.search(r"Follow[- ]?up:\s*(Yes|No)", response, re.IGNORECASE)

    eval_dict = {
        "score": score_match.group(1) if score_match else "3",
        "feedback": fb_match.group(1).strip() if fb_match else "No feedback provided.",
        "needs_followup": fup_match.group(1).strip().lower() == "yes" if fup_match else False
    }

    return eval_dict, eval_dict["feedback"]
