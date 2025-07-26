import uuid
import time
import ast
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from utils.llm_client import call_llm
from agents.input_agent import parse_inputs
from agents.skill_matching_agent import match_skills
from agents.planner_agent import create_plan
# from agents.question_generator_agent import RecruiterAgent
from agents.evaluator_agent import evaluate_and_feedback
from agents.memory_agent import store_interaction
# import contextlib
from transformers import pipeline


app = FastAPI()

class SessionStore:
    def __init__(self):
        self.sessions: Dict[str, Dict] = {}

    def create(self, questions, last_main_question):
        sid = str(uuid.uuid4())
        self.sessions[sid] = {
            # 'jd': jd_struct,
            # 'res': res_struct,
            # 'plan': plan,
            # 'idx': 0
                    
            "questions": [],           # list of 5 questions
            "idx": 0,                     # which question we're on
            "awaiting_followup": False,  # are we in a follow-up loop?
            "last_main_question": "",    # for context
            "jd": {},                 # JD object
            "res": {},                # Resume object
            "discussion_log": []      # optional full chat log

        }
        return sid

    def get(self, sid: str):
        return self.sessions.get(sid)

store = SessionStore()

class StartPayload(BaseModel):
    job_description: str
    resume: str

class AnswerPayload(BaseModel):
    session_id: str
    answer: str
    

# SESSION_TTL = 30 * 60  # 30 minutes
# CLEANUP_INTERVAL = 60  # 1 minute

# async def session_cleaner(app: FastAPI):
#     """Background task to remove expired sessions."""
#     while True:
#         now = time.time()
#         sessions = app.state.sessions
#         for sid, data in list(sessions.items()):
#             if now - data["ts"] > SESSION_TTL:
#                 sessions.pop(sid, None)
#         await asyncio.sleep(CLEANUP_INTERVAL)

# @contextlib.asynccontextmanager
# async def lifespan(app: FastAPI):
#     app.state.sessions = {}
#     cleanup_task = asyncio.create_task(session_cleaner(app))
#     yield
#     cleanup_task.cancel()
#     with contextlib.suppress(asyncio.CancelledError):
#         await cleanup_task



# class StartReq(BaseModel):
#     job_description: str
#     resume: str

# class AnsReq(BaseModel):
#     session_id: str
#     answer: str

# @app.post("/interview/start")
# async def start_interview(payload: StartReq):
#     jd = await jd_parser(payload.job_description)
#     res = await resume_parser(payload.resume)
#     matches = await vector_db.match_all(jd["skills"], res["skills"])
#     plan = ["warmup"] + list(matches.keys())[:5] + ["wrapup"]
#     sid = str(uuid.uuid4())
#     app.state.sessions[sid] = {
#         "jd": jd,
#         "plan": plan,
#         "idx": 0,
#         "ts": time.time(),
#     }
#     question = await _ask_next(sid)
#     return {"session_id": sid, "question": question}

# @app.post("/interview/answer")
# async def submit_answer(payload: AnsReq):
#     sess = app.state.sessions.get(payload.session_id)
#     if not sess:
#         raise HTTPException(404, "Invalid or expired session_id")
#     sess["ts"] = time.time()  # refresh TTL
#     response = await call_llm(
#         f"<|system|>You are an interviewer. Phase: {sess['plan'][sess['idx']]}.\n"
#         f"<|user|>Candidate answered: {payload.answer}\n"
#         "Respond with: score (1-5), feedback sentence, and next question, or DONE if finished."
#     )
#     score, feedback, next_q = _parse_llm_response(response)
#     sess["idx"] += 1
#     if next_q.upper() == "DONE" or sess["idx"] >= len(sess["plan"]):
#         app.state.sessions.pop(payload.session_id, None)
#         return {"done": True, "feedback": feedback}
#     return {"done": False, "feedback": feedback, "question": next_q}

# async def _ask_next(sid: str) -> str:
#     sess = app.state.sessions[sid]
#     phase = sess["plan"][sess["idx"]]
#     return (await call_llm(
#         f"<|system|>You are an interviewer for phase: {phase}. Ask a focused question."
#     )).strip()

# def _parse_llm_response(text: str):
#     # Very basic parser; customize based on actual LLM output format.
#     parts = text.strip().split("\n", 2)
#     score = int(parts[0].strip())
#     feedback = parts[1].strip()
#     next_q = parts[2].strip() if len(parts) > 2 else "DONE"
#     return score, feedback, next_q

    

    # Load the job role classifier pipeline
# jr_identify = pipeline("text-classification", model="srivihari/resume-job-role-classifier")

# Input your job description text

@app.get('/interview/status')
async def status_check():
    return {"status": "ok"}
    
@app.post('/interview/plan')
async def plan_interview(payload: StartPayload):
    # jd_struct = await parse_inputs.parse_jd(payload.job_description)
    jd_skills = await parse_inputs.parse_jd(payload.job_description)
    # res_skills, experience = await parse_inputs.parse_resume_text(payload.resume)
    res_skills = await parse_inputs.parse_resume_text(payload.resume)
    matched_skills = await match_skills(jd_skills, res_skills)
    # plan = create_plan(matches, res_struct['experience'])
    return {
        'skills': matched_skills,
        # 'experience': experience
    }



@app.post('/interview/start')
async def start_interview(payload: StartPayload):
    # 1. Parse JD & resume
    jd_struct = await parse_inputs.parse_jd(payload.job_description)
    res_skills = await parse_inputs.parse_resume_text(payload.resume)

    # 2. Extract and match skills
    # jd_skills = jd_struct
    # res_skills = res_struct[0]
    matches = await match_skills(jd_struct, res_skills)

    # 3. Generate 5 main questions in one LLM call
    from agents.question_generator_agent import generate_questions
    questions = await generate_questions(jd=payload.job_description, common_skills=matches)

    # 4. Create a session with full tracking info
    sid = str(uuid.uuid4())
    store.sessions[sid] = {
        "jd": jd_struct,
        "res": res_skills,
        "questions": questions,
        "idx": 0,
        "awaiting_followup": False,
        "last_main_question": "",
        "discussion_log": []
    }

    # 5. Return the first question to the frontend
    return {
        "session_id": sid,
        "question": questions[0]
    }



@app.post('/interview/answer')
async def submit_answer(payload: AnswerPayload):
    session = store.get(payload.session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Invalid session_id")
    q_list = session["questions"]

    # CASE A: We are waiting for a follow‑up reply

    if session["awaiting_followup"]:
        main_q = session["last_main_question"]
        follow_q = q_list[session["idx"]]  # not used, but could log
        # store follow‑up interaction
        await store_interaction(
                                    jd_struct=session["jd"],
                                    res_struct=session["res"],
                                    question=main_q,
                                    answer=payload.answer,
                                    eval_res=None,
                                    is_followup=True
                                )
        
        session["awaiting_followup"] = False
        session["idx"] += 1

        done = session["idx"] >= len(q_list)
        next_q = None if done else q_list[session["idx"]]
        return {"done": done, "next_question": next_q, "follow_up": False}

    # CASE B: Answer to a main question

    idx      = session["idx"]
    question = q_list[idx]

    eval_result = await evaluate_and_feedback(question, payload.answer)
    needs_fup   = eval_result[0].get("needs_followup", False)
    feedback    = eval_result[0].get("feedback", "")


    #(B1) Needs follow‑up
    
    if needs_fup:
        follow_prompt = f"""
                You are a senior interviewer.

                Original question: "{question}"
                Candidate answer: "{payload.answer}"

                Generate ONE concise follow‑up question to probe deeper.
                Return only the question text.
                """
        follow_up_q = await call_llm(follow_prompt)

        session["awaiting_followup"]   = True
        session["last_main_question"]  = question

        return {"done": False, "next_question": follow_up_q, "feedback": feedback, "follow_up": True}

    # (B2) No follow‑up → move on
    await store_interaction(session['jd'], session['res'], question, payload.answer, eval_result, is_followup=False)
    session["idx"] += 1

    done = session["idx"] >= len(q_list)
    next_q = None if done else q_list[session["idx"]]

    return {"done": done, "next_question": next_q, "feedback": feedback, "follow_up": False}



# ___________________________________________________
## CODE FOR EVALUATOR AGENT
