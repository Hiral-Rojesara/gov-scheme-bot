import streamlit as st
import google.generativeai as genai
import json
import os

# 1. API Configuration
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Secrets mein GEMINI_API_KEY nahi mili!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

# 2. SYSTEM_PROMPT (Triple Quotes sahi se lagaye gaye hain)
SYSTEM_PROMPT = """
You are AI Government Scheme Copilot for India.

Purpose / उद्देश्य:
- Guide citizens about only officially announced Central and State Government schemes.
- Focus: Easy-to-understand, trustworthy guidance for low-digital literacy users.
- Never suggest private, unofficial, or non-government schemes.

--------------------------------------------------
1. First Message / Language Selection / पहला संदेश
--------------------------------------------------
Which language would you prefer to speak?
1. English  2. Hindi (हिन्दी)  3. Tamil  4. Bengali  5. Marathi 
6. Telugu   7. Gujarati      8. Kannada 9. Malayalam 10. Odia 
11. Punjabi 12. Assamese     13. Nepali 14. Santali  15. Konkani

--------------------------------------------------
RULES:
- Ask details one by one (State, Age, Occupation).
- Show 3-5 relevant schemes.
- Always add disclaimer: "Yeh jaankari sirf guidance ke liye hai."
"""

# 3. Session State for Chat Memory
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
    st.session_state.initialized = False

# 4. API Endpoint Logic
params = st.query_params
if "action" in params:
    action = params["action"]
    if action == "init" and not st.session_state.initialized:
        response = st.session_state.chat_session.send_message(SYSTEM_PROMPT)
        st.session_state.initialized = True
        st.json({"reply": response.text})
        st.stop()
    elif action == "chat":
        user_msg = params.get("msg", "")
        response = st.session_state.chat_session.send_message(user_msg)
        st.json({"reply": response.text})
        st.stop()

# 5. UI Hosting
st.set_page_config(page_title="Gov Scheme Bot", layout="centered")
current_dir = os.path.dirname(__file__)
html_path = os.path.join(current_dir, "static", "index.html")

if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        st.components.v1.html(f.read(), height=800, scrolling=True)
else:
    st.error("static/index.html nahi mili!")
