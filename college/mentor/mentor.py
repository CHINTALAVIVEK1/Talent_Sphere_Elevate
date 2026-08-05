import streamlit as st
from utils.gemini import client
from google.genai import types

SYSTEM_MOCK_MENTOR = """
You are a career mentor and coach inside TalentSphere Elevate. You help college students with career exploration, selecting courses/certifications, preparing for placements, mock interviews, dynamic roadmaps, and building resume profiles.
Keep answers professional, structured, and highly supportive. 
If the user asks about topics completely unrelated to career guidance, education, software engineering, software learning, or interview preparation, politely redirect them back to career development subjects.
"""

def query_mentor_assistant(chat_history, user_message):
    """
    Queries Gemini under the system mentor coach prompt.
    """
    prompt = "Previous Conversation:\n"
    for role, msg in chat_history:
        prompt += f"{role}: {msg}\n"
    prompt += f"User: {user_message}\n"
    prompt += "Mentor:"
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_MOCK_MENTOR,
                temperature=0.4
            )
        )
        return response.text.strip()
    except Exception as e:
        print(f"Error querying career mentor: {e}")
        return "I am experiencing technical difficulties. Please ask your career question again."

def career_mentor():
    st.markdown("### AI Career Mentor")
    st.write("Ask your career coach about choosing courses, certifications, placement tracking, study plans, or mock interview preparation.")
    
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("Please log in to continue.")
        return
        
    if "mentor_chat_history" not in st.session_state:
        st.session_state.mentor_chat_history = []
        
    # Render chat bubbles
    for idx, (role, text) in enumerate(st.session_state.mentor_chat_history):
        bubble_class = "chat-bubble-user" if role == "User" else "chat-bubble-assistant"
        sender_label = "You" if role == "User" else "Career Mentor"
        st.markdown(f"""
        <div class="{bubble_class}">
            <b>{sender_label}:</b><br/>{text}
        </div>
        """, unsafe_allow_html=True)
        
    with st.form("mentor_chat_form", clear_on_submit=True):
        user_msg = st.text_input("Ask your career mentor...", placeholder="e.g. How do I prepare for a software developer interview?")
        cols_form = st.columns([5, 1])
        with cols_form[1]:
            submit_msg = st.form_submit_button("Send")
            
        if submit_msg and user_msg.strip():
            st.session_state.mentor_chat_history.append(("User", user_msg.strip()))
            with st.spinner("AI thinking..."):
                ai_reply = query_mentor_assistant(st.session_state.mentor_chat_history[:-1], user_msg.strip())
            st.session_state.mentor_chat_history.append(("Assistant", ai_reply))
            st.rerun()
            
    if st.button("Clear Chat History"):
        st.session_state.mentor_chat_history = []
        st.rerun()
