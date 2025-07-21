# 🧠 Agentic Recruiter

A modular, LLM-powered interview system that reads a **job description** and a **candidate resume**, then conducts a five-question technical interview with smart follow-ups, real-time feedback, and backend evaluation.

---

## ✨ Features

- 🔍 Parses resume & job description
- 🧠 Enhanced **skill extraction** from JD/Resume and **matching** using semantic similarity cosine threshold for finding exact and very similar matches, powered by **Gemini 2.5 Flash**. 
- ❓ Technical interview questions powered GPT-4o-mini(or any llm of your choice) varying with the depth of candidate's experience.
- 🔁 Contextual follow-up questions based on candidate’s answers
- 📝 Real-time feedback with hidden scoring (stored server-side)
- 🗂️ Session memory using FastAPI (easily extendable to Redis)
- 💬 Interactive frontend with Streamlit chat interface
- ⚡ Low LLM usage per interview (1 generate + ≤5 eval + optional follow-ups)

---


---

## 🚀 Quick Start

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

## Flow
agentic_recruiter/
├── backend/
│   ├── orchestrator.py
│   ├── agents/
│   │   ├── input_agent.py
│   │   ├── skill_matching_agent.py
│   │   ├── planner_agent.py
│   │   ├── question_generator_agent.py
│   │   ├── evaluator_agent.py
│   │   └── memory_agent.py
│   └── utils/
│       ├── resume_parser.py
│       ├── jd_parser.py
│       ├── vector_db.py
│       └── llm_client.py
├── frontend/
│   └── streamlit_app.py
├── requirements.txt
└── README.md

