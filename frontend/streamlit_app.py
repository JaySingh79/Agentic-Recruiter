# import streamlit as st
# import httpx
# import logging
# # from resume_pdf_to_text import extract_text_from_file
# from pypdf import PdfReader


# logging.basicConfig(level=logging.ERROR, filename='app.log', format='%(asctime)s - %(levelname)s - %(message)s')

# # Add natural conversation styling
# st.markdown("""
# <style>
# .user-message {
#     background-color: rgba(52, 152, 219, 0.1);
#     padding: 12px 16px;
#     border-radius: 18px;
#     margin: 8px 0;
#     border-left: 3px solid #3498db;
# }

# .assistant-message {
#     background-color: rgba(46, 204, 113, 0.1);
#     padding: 12px 16px;
#     border-radius: 18px;
#     margin: 8px 0;
#     border-left: 3px solid #2ecc71;
# }

# .conversation-container {
#     max-height: 600px;
#     overflow-y: auto;
#     padding: 10px;
#     scroll-behavior: smooth;
# }

# .next-question {
#     background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#     color: white;
#     padding: 16px;
#     border-radius: 12px;
#     margin: 16px 0;
#     box-shadow: 0 4px 15px rgba(0,0,0,0.1);
# }

# .user-answer-preview {
#     background-color: rgba(52, 152, 219, 0.15);
#     padding: 10px 14px;
#     border-radius: 12px;
#     margin: 8px 0;
#     opacity: 0.9;
#     border-left: 4px solid #3498db;
# }
# </style>
# """, unsafe_allow_html=True)


# API = "http://127.0.0.1:8000"

# st.set_page_config(page_title="Agentic Recruiter", page_icon="😎", layout="wide")
# st.title("Agentic Recruiter – Interactive Interview")

# # Safe defaults for session state
# if 'session_id' not in st.session_state:
#     st.session_state.session_id = None
# if 'connection_status' not in st.session_state:
#     st.session_state.connection_status = None
# if 'parsed' not in st.session_state:
#     st.session_state.parsed = False
# if 'resume_text' not in st.session_state:
#     st.session_state.resume_text = ""
# if 'jd_text' not in st.session_state:
#     st.session_state.jd_text = ""
# if 'parsed_info' not in st.session_state:
#     st.session_state.parsed_info = {}
# if 'chat_history' not in st.session_state:
#     st.session_state.chat_history = []
# if 'is_processing' not in st.session_state:
#     st.session_state.is_processing = False
# if 'current_question' not in st.session_state:
#     st.session_state.current_question = None

# try:
        
#     with st.sidebar:
#         if st.button("Status Check"):
#             response_back = httpx.get(f"{API}/interview/status")
#             data = response_back.json()
#             try:
#                 if data["status"] == "ok":
#                     st.write("All Good!")
#             except:
#                 st.markdown("Server down")


#         st.header("Input Job Details")

#         jd_input = st.text_area("Paste Job Description")
#         resume_file = st.file_uploader("Upload Resume (txt/pdf)")
#         # resume_file = st.text_area("Input resume skills area")
#         if resume_file:
#             page = PdfReader(resume_file).pages[0]
#             st.session_state.resume_text = page.extract_text()
#             # st.session_state.resume_text = resume_file
#         st.session_state.jd_text = jd_input
        
#         client = httpx.Client(timeout=httpx.Timeout(60.0, read=60.0))

#         if st.button("1️⃣ Parse Inputs"):
#             with st.spinner("Parsing and planning..."):
#                 resp = client.post(f"{API}/interview/plan", 
#                                 json={
#                                         "job_description": st.session_state.jd_text,
#                                         "resume": st.session_state.resume_text
#                                     }).json()
#                 st.session_state.parsed_info = resp
#                 st.session_state.parsed = True
#                 st.success("Inputs parsed successfully!")

#         if st.session_state.parsed:
#             st.write("**Experience:**", st.session_state.parsed_info.get("experience", "N/A"))
#             st.write("**Matched Skills:**", st.session_state.parsed_info.get("skills", []))

#         if st.session_state.parsed and st.button("2️⃣ Start Interview"):
#             with st.spinner("Generating first question..."):
#                 resp = httpx.post(
#                     f"{API}/interview/start",
#                     json={
#                         "job_description": st.session_state.jd_text,
#                         "resume": st.session_state.resume_text
#                     },
#                     timeout=120.0
#                 ).json()
#                 st.session_state.session_id = resp["session_id"]
#                 st.session_state.current_question = resp["question"]

# ### Question Answering starts from here !!

#     if st.session_state.session_id:
        
#         st.subheader("💬 Interview in Progress")

#         # Show all previous messages
#         for message in st.session_state.chat_history:
#             if message["role"] == "interviewer":
#                 with st.chat_message("assistant", avatar="🤖"):
#                     st.write(f"**Question:** {message['content']}")
#             else:
#                 with st.chat_message("user", avatar="👤"):
#                     st.write(f"**Your Answer:** {message['content']}")

        
#         if st.session_state.current_question:
#             with st.chat_message("assistant", avatar="🤖"):
#                 st.write(f"**Current Question:** {st.session_state.current_question}")

#         # st.chat_message("system").write(st.session_state.current_question)
#         # Show processing indicator
#             if st.session_state.is_processing:
#                 with st.spinner("🧠 AI is analyzing your response..."):
#                     st.empty()

#             user_input = st.chat_input("Type your answer here...", disabled=st.session_state.is_processing)
#             if user_input and not st.session_state.is_processing:
#                 # Set processing state
#                 st.session_state.is_processing = True
                
#                 # Show user's answer immediately
#                 with st.chat_message("user", avatar="👤"):
#                     st.write(f"**Your Answer ---** {user_input}")
                
#                 # Add to chat history
#                 st.session_state.chat_history.append({
#                     "question": st.session_state.current_question,
#                     "role": "user", 
#                     "content": user_input
#                 })

        
#         # Show processing indicator
#         if st.session_state.is_processing:
#             with st.spinner("🧠 AI is analyzing your response..."):
#                 st.empty()
        
                
#         if user_input:
#             payload = {"session_id": st.session_state.session_id, "answer": user_input}
#             resp = httpx.post(f"{API}/interview/answer", json=payload).json()
#             feedback = resp.get("feedback")
#             if feedback:
#                 with st.chat_message("assistant"):
#                     st.write(feedback)
#                 # st.markdown("")
#             if resp.get("done"):
#                 st.success("Interview complete! Thank you.")
#                 st.session_state.session_id = None
            
#             elif resp.get("follow_up"):
#                 st.session_state.current_question = resp.get("next_question")
#                 with st.chat_message("assistant", avatar="🤖"):
#                     st.write(f"**Follow Up Question ---** {st.session_state.current_question}")
#             else:
#                 st.chat_message("system").write("Lets go ahead ..")
#                 st.session_state.current_question = resp.get("next_question")
#                 with st.chat_message("assistant", avatar="🤖"):
#                     st.write(f"**Current Question ---** {st.session_state.current_question}")
        
        
#         if st.session_state.chat_history:
#             questions_asked = len([m for m in st.session_state.chat_history if m["role"] == "interviewer"])
#             st.sidebar.metric("Questions Asked", questions_asked)
            
# except httpx.ReadTimeout as e:
#     st.error(f"Server took too long to respond\n")
#     logging.error("Here is the error", exc_info=True)
#     st.write(f"{e}")
#     st.stop()
# except httpx.RequestError as e:
#     st.error(f"Network error: {e}")
#     logging.error("Here is the error", exc_info=True)
#     st.write(f"{e}")
#     st.stop()
























# import streamlit as st
# import httpx
# import logging
# from pypdf import PdfReader

# logging.basicConfig(level=logging.ERROR, filename='app.log', format='%(asctime)s - %(levelname)s - %(message)s')

# API = "http://127.0.0.1:8000"

# st.set_page_config(page_title="Agentic Recruiter", page_icon="😎", layout="wide")

# # Custom CSS for natural conversation styling
# st.markdown("""
# <style>
#     .chat-container {
#         max-height: 600px;
#         overflow-y: auto;
#         padding: 1rem;
#         border-radius: 10px;
#         background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
#         margin-bottom: 1rem;
#     }
    
#     .question-message {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         color: white;
#         padding: 1rem 1.5rem;
#         border-radius: 18px 18px 18px 4px;
#         margin: 0.5rem 0;
#         box-shadow: 0 2px 10px rgba(0,0,0,0.1);
#         animation: slideInLeft 0.5s ease-out;
#     }
    
#     .answer-message {
#         background: rgba(255, 255, 255, 0.7);
#         backdrop-filter: blur(10px);
#         padding: 1rem 1.5rem;
#         border-radius: 18px 18px 4px 18px;
#         margin: 0.5rem 0;
#         margin-left: auto;
#         max-width: 80%;
#         box-shadow: 0 2px 10px rgba(0,0,0,0.1);
#         animation: slideInRight 0.5s ease-out;
#         border-left: 4px solid #667eea;
#     }
    
#     .feedback-message {
#     background: linear-gradient(135deg, #e8f5e8 0%, #f0f8f0 100%);
#     color: #2d5a2d;
#     padding: 0.8rem 1.2rem;
#     border-radius: 12px;
#     margin: 0.3rem 0;
#     font-size: 0.9rem;
#     box-shadow: 0 2px 8px rgba(0,0,0,0.1);
#     animation: fadeIn 0.5s ease-out;
#     border-left: 4px solid #28a745;
#     }

    
#     .next-question-indicator {
#         background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
#         color: white;
#         padding: 0.5rem 1rem;
#         border-radius: 20px;
#         font-size: 0.8rem;
#         font-weight: bold;
#         margin: 0.5rem 0;
#         text-align: center;
#         animation: pulse 2s infinite;
#     }
    
#     .current-question {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         color: white;
#         padding: 1.2rem 1.8rem;
#         border-radius: 18px 18px 18px 4px;
#         margin: 1rem 0;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.2);
#         border-left: 5px solid #ffeaa7;
#         animation: glow 2s ease-in-out infinite alternate;
#     }
    
#     .processing-indicator {
#         background: rgba(255, 255, 255, 0.9);
#         padding: 1rem;
#         border-radius: 15px;
#         text-align: center;
#         margin: 1rem 0;
#         animation: breathe 2s ease-in-out infinite;
#     }
    
#     @keyframes slideInLeft {
#         from { transform: translateX(-50px); opacity: 0; }
#         to { transform: translateX(0); opacity: 1; }
#     }
    
#     @keyframes slideInRight {
#         from { transform: translateX(50px); opacity: 0; }
#         to { transform: translateX(0); opacity: 1; }
#     }
    
#     @keyframes fadeIn {
#         from { opacity: 0; }
#         to { opacity: 1; }
#     }
    
#     @keyframes pulse {
#         0% { transform: scale(1); }
#         50% { transform: scale(1.05); }
#         100% { transform: scale(1); }
#     }
    
#     @keyframes glow {
#         from { box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3); }
#         to { box-shadow: 0 4px 25px rgba(102, 126, 234, 0.6); }
#     }
    
#     @keyframes breathe {
#         0% { transform: scale(1); }
#         50% { transform: scale(1.02); }
#         100% { transform: scale(1); }
#     }
    
#     .stTextInput > div > div > input {
#         border-radius: 25px;
#         border: 2px solid #667eea;
#         padding: 0.8rem 1.5rem;
#         font-size: 1rem;
#     }
    
#     .conversation-header {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         color: white;
#         padding: 1rem;
#         border-radius: 15px;
#         margin-bottom: 1rem;
#         text-align: center;
#     }
# </style>
# """, unsafe_allow_html=True)

# st.title("AI Recruiter – Interview")

# # Safe defaults for session state
# if 'session_id' not in st.session_state:
#     st.session_state.session_id = None
# if 'connection_status' not in st.session_state:
#     st.session_state.connection_status = None
# if 'parsed' not in st.session_state:
#     st.session_state.parsed = False
# if 'resume_text' not in st.session_state:
#     st.session_state.resume_text = ""
# if 'jd_text' not in st.session_state:
#     st.session_state.jd_text = ""
# if 'parsed_info' not in st.session_state:
#     st.session_state.parsed_info = {}
# if 'chat_history' not in st.session_state:
#     st.session_state.chat_history = []
# if 'is_processing' not in st.session_state:
#     st.session_state.is_processing = False
# if 'current_question' not in st.session_state:
#     st.session_state.current_question = None

# try:
#     with st.sidebar:
#         if st.button("Status Check"):
#             response_back = httpx.get(f"{API}/interview/status")
#             data = response_back.json()
#             try:
#                 if data["status"] == "ok":
#                     st.write("All Good!")
#             except:
#                 st.markdown("Server down")

#         st.header("Input Job Details")
#         jd_input = st.text_area("Paste Job Description")
#         resume_file = st.file_uploader("Upload Resume (txt/pdf)")

#         if resume_file:
#             page = PdfReader(resume_file).pages[0]
#             st.session_state.resume_text = page.extract_text()

#         st.session_state.jd_text = jd_input

#         client = httpx.Client(timeout=httpx.Timeout(60.0, read=60.0))

#         if st.button("1️⃣ Parse Inputs"):
#             with st.spinner("Parsing and planning..."):
#                 resp = client.post(f"{API}/interview/plan",
#                                 json={
#                                     "job_description": st.session_state.jd_text,
#                                     "resume": st.session_state.resume_text
#                                 }).json()
#                 st.session_state.parsed_info = resp
#                 st.session_state.parsed = True
#                 st.success("Inputs parsed successfully!")

#         if st.session_state.parsed:
#             st.write("**Experience:**", st.session_state.parsed_info.get("experience", "N/A"))
#             st.write("**Matched Skills:**", st.session_state.parsed_info.get("skills", []))

#         if st.session_state.parsed and st.button("2️⃣ Start Interview"):
#             with st.spinner("Generating first question..."):
#                 resp = httpx.post(
#                     f"{API}/interview/start",
#                     json={
#                         "job_description": st.session_state.jd_text,
#                         "resume": st.session_state.resume_text
#                     },
#                     timeout=120.0
#                 ).json()
#                 st.session_state.session_id = resp["session_id"]
#                 st.session_state.current_question = resp["question"]

#     ### Question Answering starts from here !!
#     if st.session_state.session_id:
#         # Conversation header
#         st.markdown("""
#         <div class="conversation-header">
#             <h3>💬 Interview in Progress</h3>
#             <p>Answer questions wisely, All the best!</p>
#         </div>
#         """, unsafe_allow_html=True)

#         # Create scrollable chat container
#         chat_placeholder = st.container()
        
#         with chat_placeholder:
#             # Display conversation history
#             for i, message in enumerate(st.session_state.chat_history):
#                 if message["role"] == "interviewer":
#                     st.markdown(f"""
#                     <div class="question-message">
#                         <strong>🤖 Interviewer:</strong><br>
#                         {message['content']}
#                     </div>
#                     """, unsafe_allow_html=True)
#                 elif message["role"] == "user":
#                     st.markdown(f"""
#                     <div class="answer-message">
#                         <strong>👤 You:</strong><br>
#                         {message['content']}
#                     </div>
#                     """, unsafe_allow_html=True)
#                 elif message["role"] == "feedback":
#                     st.markdown(f"""
#                     <div class="feedback-message">
#                         <strong>📝 Feedback:</strong> {message['content']}
#                     </div>
#                     """, unsafe_allow_html=True)

#             # Show current question with special styling
#             if st.session_state.current_question:
#                 # Check if it's a new question (not in history)
#                 is_new_question = True
#                 if st.session_state.chat_history:
#                     last_message = st.session_state.chat_history[-1]
#                     if last_message.get("role") == "interviewer" and last_message.get("content") == st.session_state.current_question:
#                         is_new_question = False

#                 if is_new_question:
#                     st.markdown("""
#                     <div class="next-question-indicator">
#                         ⚡ Next Question
#                     </div>
#                     """, unsafe_allow_html=True)

#                 st.markdown(f"""
#                 <div class="current-question">
#                     <strong>🤖 Interviewer:</strong><br>
#                     {st.session_state.current_question}
#                 </div>
#                 """, unsafe_allow_html=True)

#         # Processing indicator
#         if st.session_state.is_processing:
#             st.markdown("""
#             <div class="processing-indicator">
#                 <strong>🧠 AI is analyzing your response...</strong><br>
#                 Please wait while I process your answer
#             </div>
#             """, unsafe_allow_html=True)

#         # User input
#         user_input = st.chat_input("Type your answer here...", disabled=st.session_state.is_processing)

#         if user_input and not st.session_state.is_processing:
#             # Set processing state
#             st.session_state.is_processing = True
            
#             # Add current question to history if not already there
#             if st.session_state.current_question:
#                 # Check if current question is already in history
#                 question_in_history = False
#                 for msg in st.session_state.chat_history:
#                     if msg.get("role") == "interviewer" and msg.get("content") == st.session_state.current_question:
#                         question_in_history = True
#                         break
                
#                 if not question_in_history:
#                     st.session_state.chat_history.append({
#                         "role": "interviewer",
#                         "content": st.session_state.current_question
#                     })

#             # Add user's answer to history
#             st.session_state.chat_history.append({
#                 "role": "user",
#                 "content": user_input
#             })

#             # Process the answer
#             try:
#                 payload = {"session_id": st.session_state.session_id, "answer": user_input}
#                 resp = httpx.post(f"{API}/interview/answer", json=payload).json()
                
#                 feedback = resp.get("feedback")
#                 if feedback:
#                     st.session_state.chat_history.append({
#                         "role": "feedback",
#                         "content": feedback
#                     })

#                 if resp.get("done"):
#                     st.session_state.chat_history.append({
#                         "role": "system",
#                         "content": "🎉 Interview Complete! Thank you for your time."
#                     })
#                     st.success("Interview complete! Thank you.")
#                     st.session_state.session_id = None
#                     st.balloons()
#                 else:
#                     # Update current question
#                     if resp.get("follow_up"):
#                         st.session_state.current_question = resp.get("next_question")
#                     else:
#                         st.session_state.current_question = resp.get("next_question")

#             except Exception as e:
#                 st.error(f"Error processing response: {str(e)}")
#                 logging.error("Error in answer processing", exc_info=True)
            
#             finally:
#                 # Reset processing state and refresh
#                 st.session_state.is_processing = False
#                 st.rerun()

#         # Progress indicator in sidebar
#         if st.session_state.chat_history:
#             questions_asked = len([m for m in st.session_state.chat_history if m["role"] == "interviewer"])
#             st.sidebar.metric("Questions Asked", questions_asked)
#             if questions_asked > 0:
#                 st.sidebar.progress(min(questions_asked / 10, 1.0))

# except httpx.ReadTimeout as e:
#     st.error(f"Server took too long to respond\n")
#     logging.error("Here is the error", exc_info=True)
#     st.write(f"{e}")
#     st.stop()

# except httpx.RequestError as e:
#     st.error(f"Network error: {e}")
#     logging.error("Here is the error", exc_info=True)
#     st.write(f"{e}")
#     st.stop()















import streamlit as st
import httpx
import logging
from pypdf import PdfReader

logging.basicConfig(level=logging.ERROR, filename='app.log', format='%(asctime)s - %(levelname)s - %(message)s')

API = "http://127.0.0.1:8000"

st.set_page_config(page_title="Agentic Recruiter", page_icon="😎", layout="wide")

# Custom CSS for natural conversation styling
st.markdown("""
<style>
    .chat-container {
        max-height: 600px;
        overflow-y: auto;
        padding: 1rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        margin-bottom: 1rem;
    }
    
    .question-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 18px 18px 18px 4px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        animation: slideInLeft 0.5s ease-out;
    }
    
    .answer-message {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        padding: 1rem 1.5rem;
        border-radius: 18px 18px 4px 18px;
        margin: 0.5rem 0;
        margin-left: auto;
        max-width: 80%;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        animation: slideInRight 0.5s ease-out;
        border-left: 4px solid #667eea;
    }
    
    .feedback-message {
    background: linear-gradient(135deg, #e8f5e8 0%, #f0f8f0 100%);
    color: #2d5a2d;
    padding: 0.8rem 1.2rem;
    border-radius: 12px;
    margin: 0.3rem 0;
    font-size: 0.9rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    animation: fadeIn 0.5s ease-out;
    border-left: 4px solid #28a745;
    }

    
    .next-question-indicator {
        background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        margin: 0.5rem 0;
        text-align: center;
        animation: pulse 2s infinite;
    }
    
    .current-question {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.2rem 1.8rem;
        border-radius: 18px 18px 18px 4px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        border-left: 5px solid #ffeaa7;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    .processing-indicator {
        background: rgba(255, 255, 255, 0.9);
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        animation: breathe 2s ease-in-out infinite;
    }
    
    @keyframes slideInLeft {
        from { transform: translateX(-50px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideInRight {
        from { transform: translateX(50px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes glow {
        from { box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3); }
        to { box-shadow: 0 4px 25px rgba(102, 126, 234, 0.6); }
    }
    
    @keyframes breathe {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #667eea;
        padding: 0.8rem 1.5rem;
        font-size: 1rem;
    }
    
    .conversation-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.title("Agentic Recruiter – Interactive Interview")

# Safe defaults for session state
if 'session_id' not in st.session_state:
    st.session_state.session_id = None
if 'connection_status' not in st.session_state:
    st.session_state.connection_status = None
if 'parsed' not in st.session_state:
    st.session_state.parsed = False
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""
if 'jd_text' not in st.session_state:
    st.session_state.jd_text = ""
if 'parsed_info' not in st.session_state:
    st.session_state.parsed_info = {}
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'is_processing' not in st.session_state:
    st.session_state.is_processing = False
if 'current_question' not in st.session_state:
    st.session_state.current_question = None

try:
    with st.sidebar:
        if st.button("Status Check"):
            response_back = httpx.get(f"{API}/interview/status")
            data = response_back.json()
            try:
                if data["status"] == "ok":
                    st.write("All Good!")
            except:
                st.markdown("Server down")

        st.header("Input Job Details")
        jd_input = st.text_area("Paste Job Description")
        resume_file = st.file_uploader("Upload Resume (txt/pdf)")

        if resume_file:
            page = PdfReader(resume_file).pages[0]
            st.session_state.resume_text = page.extract_text()

        st.session_state.jd_text = jd_input

        client = httpx.Client(timeout=httpx.Timeout(60.0, read=60.0))

        if st.button("1️⃣ Parse Inputs"):
            with st.spinner("Parsing and planning..."):
                resp = client.post(f"{API}/interview/plan",
                                json={
                                    "job_description": st.session_state.jd_text,
                                    "resume": st.session_state.resume_text
                                }).json()
                st.session_state.parsed_info = resp
                st.session_state.parsed = True
                st.success("Inputs parsed successfully!")

        if st.session_state.parsed:
            st.write("**Experience:**", st.session_state.parsed_info.get("experience", "N/A"))
            st.write("**Matched Skills:**", st.session_state.parsed_info.get("skills", []))

        if st.session_state.parsed and st.button("2️⃣ Start Interview"):
            with st.spinner("Generating first question..."):
                resp = httpx.post(
                    f"{API}/interview/start",
                    json={
                        "job_description": st.session_state.jd_text,
                        "resume": st.session_state.resume_text
                    },
                    timeout=120.0
                ).json()
                st.session_state.session_id = resp["session_id"]
                st.session_state.current_question = resp["question"]

    ### Question Answering starts from here !!
    if st.session_state.session_id:
        # Conversation header
        st.markdown("""
        <div class="conversation-header">
            <h3>💬 Interview in Progress</h3>
            <p>Have a natural conversation with our AI recruiter</p>
        </div>
        """, unsafe_allow_html=True)

        # Create scrollable chat container
        chat_placeholder = st.container()
        
        with chat_placeholder:
            # Display conversation history
            for i, message in enumerate(st.session_state.chat_history):
                if message["role"] == "interviewer":
                    st.markdown(f"""
                    <div class="question-message">
                        <strong>🤖 Interviewer:</strong><br>
                        {message['content']}
                    </div>
                    """, unsafe_allow_html=True)
                elif message["role"] == "user":
                    st.markdown(f"""
                    <div class="answer-message">
                        <strong>👤 You:</strong><br>
                        {message['content']}
                    </div>
                    """, unsafe_allow_html=True)
                elif message["role"] == "feedback":
                    st.markdown(f"""
                    <div class="feedback-message">
                        <strong>📝 Feedback:</strong> {message['content']}
                    </div>
                    """, unsafe_allow_html=True)

            # Show current question with special styling
            if st.session_state.current_question:
                # Check if it's a new question (not in history)
                is_new_question = True
                if st.session_state.chat_history:
                    last_message = st.session_state.chat_history[-1]
                    if last_message.get("role") == "interviewer" and last_message.get("content") == st.session_state.current_question:
                        is_new_question = False

                if is_new_question:
                    st.markdown("""
                    <div class="next-question-indicator">
                        ⚡ Next Question
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="current-question">
                    <strong>🤖 Interviewer:</strong><br>
                    {st.session_state.current_question}
                </div>
                """, unsafe_allow_html=True)

        # Processing indicator
        if st.session_state.is_processing:
            st.markdown("""
            <div class="processing-indicator">
                <strong>🧠 AI is analyzing your response...</strong><br>
                Please wait while I process your answer
            </div>
            """, unsafe_allow_html=True)

        # User input
        user_input = st.chat_input("Type your answer here...", disabled=st.session_state.is_processing)

        if user_input and not st.session_state.is_processing:
            # Set processing state
            st.session_state.is_processing = True
            
            # Add current question to history if not already there
            if st.session_state.current_question:
                # Check if current question is already in history
                question_in_history = False
                for msg in st.session_state.chat_history:
                    if msg.get("role") == "interviewer" and msg.get("content") == st.session_state.current_question:
                        question_in_history = True
                        break
                
                if not question_in_history:
                    st.session_state.chat_history.append({
                        "role": "interviewer",
                        "content": st.session_state.current_question
                    })

            # Add user's answer to history
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_input
            })

            # Process the answer
            try:
                payload = {"session_id": st.session_state.session_id, "answer": user_input}
                resp = httpx.post(f"{API}/interview/answer", json=payload).json()
                
                feedback = resp.get("feedback")
                if feedback:
                    st.session_state.chat_history.append({
                        "role": "feedback",
                        "content": feedback
                    })

                if resp.get("done"):
                    st.session_state.chat_history.append({
                        "role": "system",
                        "content": "🎉 Interview Complete! Thank you for your time."
                    })
                    st.success("Interview complete! Thank you.")
                    st.session_state.session_id = None
                    st.balloons()
                else:
                    # Update current question
                    if resp.get("follow_up"):
                        st.session_state.current_question = resp.get("next_question")
                    else:
                        st.session_state.current_question = resp.get("next_question")

            except Exception as e:
                st.error(f"Error processing response: {str(e)}")
                logging.error("Error in answer processing", exc_info=True)
            
            finally:
                # Reset processing state and refresh
                st.session_state.is_processing = False
                st.rerun()

        # Progress indicator in sidebar
        if st.session_state.chat_history:
            questions_asked = len([m for m in st.session_state.chat_history if m["role"] == "interviewer"])
            st.sidebar.metric("Questions Asked", questions_asked)
            if questions_asked > 0:
                st.sidebar.progress(min(questions_asked / 10, 1.0))

except httpx.ReadTimeout as e:
    st.error(f"Server took too long to respond\n")
    logging.error("Here is the error", exc_info=True)
    st.write(f"{e}")
    st.stop()

except httpx.RequestError as e:
    st.error(f"Network error: {e}")
    logging.error("Here is the error", exc_info=True)
    st.write(f"{e}")
    st.stop()
