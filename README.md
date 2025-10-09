# ConvoHire - Agentic Recruiter

A modular, LLM-powered interview system that reads a **job description** and a **candidate resume**, then conducts a five-question technical interview with smart follow-ups, real-time feedback, and backend evaluation.

---

## ✨ *Features*

- 🔍 Parses resume & job description
- 🧠 Enhanced **skill extraction** from JD/Resume and **matching** using semantic similarity cosine threshold for finding exact and very similar matches, powered by **Gemini 2.5 Flash**. 
- ❓ Technical interview questions powered GPT-4o-mini(or any llm of your choice) varying with the depth of candidate's experience.
- 🔁 Contextual follow-up questions based on candidate’s answers
- 📝 Real-time feedback with hidden scoring (stored server-side)
- 🗂️ Session memory using FastAPI (easily extendable to Redis)
- 💬 Interactive frontend with Streamlit chat interface
- ⚡ Low LLM usage per interview (1 generate + ≤5 eval + optional follow-ups)

---

## *Technical Flow*

### Agentic-Recruiter (ConvoHire) – Technical Flow Brief

**Overview:**
ConvoHire is a modular, LLM-powered interview system that simulates human-like technical interviews. It compares a candidate's resume with a job description (JD), extracts and matches skills, and conducts a dynamic question-answer session with backend evaluation and real-time feedback.

**Main Technical Flow:**

- **Input and Parsing:**
  - The system takes a candidate resume and a job description as input.
  - Uses custom parsers (`resume_parser.py`, `jd_parser.py`) to extract relevant skills and details from both documents.

- **Skill Extraction & Matching:**
  - Extracted skills from resume and JD are processed for semantic similarity (cosine thresholding), powered by Gemini 2.5 Flash LLM.
  - `skill_matching_agent.py` identifies exact and similar matches between candidate and JD skills.

- **Interview Orchestration:**
  - `planner_agent.py` orchestrates the interview in 5 technical questions.
  - `question_generator_agent.py` dynamically creates questions, tailored to candidate experience and JD requirements.
  - For each candidate answer, context-aware follow-up questions can be triggered.

- **Evaluation & Feedback:**
  - `evaluator_agent.py` evaluates candidate answers in real time (hidden scoring stored server-side).
  - Real-time feedback is provided to candidates, with backend maintaining scoring and session details.

- **Session Memory:**
  - Session data persists using FastAPI backend (extensible to Redis for scalable state management).
  - The `memory_agent.py` manages conversational and evaluation states.

- **Frontend Interface:**
  - Interactive chat interface built with Streamlit (`streamlit_app.py`) for easy candidate interaction.
  - Backend API (`orchestrator.py`) handles LLM calls, evaluation, and state updates.

**Low Resource Usage:**
Uses only a few LLM calls per interview session (one for generation, up to five for evaluation, plus optional follow-ups), keeping resource use efficient.

***

**Suggested Flow Diagram Sections:**
- Resume/JD Input → Parsing Agents → Skill Extraction & Matching → Question Planning & Generation → Candidate Answers → Follow-up & Evaluation Agents → Real-time Feedback → Session Memory → Frontend Display[1]

This summary should help map out each module and how data flows from input to candidate interaction and backend evaluation.

---

## 🚀 *Quick Start*

### 1. Clone & Setup

```bash
git clone https://github.com/your-org/agentic_recruiter.git
cd agentic_recruiter
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```
```bash
export OPENAI_API_KEY="your-key-here"
export GEMINI_API_KEY="your-key-here"
```

```bash
uvicorn backend.orchestrator:app --reload
```

```bash
streamlit run frontend/streamlit_app.py
```
│       └── llm_client.py
├── frontend/
│   └── streamlit_app.py
├── requirements.txt
└── README.md

