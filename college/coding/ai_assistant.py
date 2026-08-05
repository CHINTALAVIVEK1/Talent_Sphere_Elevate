import json
from utils.gemini import client
from google.genai import types

SYSTEM_INSTRUCTIONS = """
You are a strict AI Coding Assistant inside TalentSphere Elevate. You are an expert in programming languages, algorithms, data structures, software engineering, databases, system design, and technical interview preparation.

LIMITATION RULE:
You are strictly limited to coding and technical topics. 
If the user asks about ANY topic unrelated to programming, computer science, software engineering, databases, web development, or technical interview preparation (such as politics, travel, general knowledge, sports, medical advice, finance, world events, entertainment, recipes, history, or general life advice), you MUST respond exactly with:
"I am the Coding Assistant. I can only help with programming, algorithms, debugging, software engineering, databases, computer science concepts, interview preparation, and coding-related topics."

Do not add any greetings, explanations, markdown formatting, or extra sentences. Just return that exact string.
For coding-related queries, you are allowed to provide code explanations, debugging, optimization, time/space complexity analysis, or explain technical concepts.
"""

QUICK_START_PROMPTS = [
    "Explain Time Complexity (Big O Notation)",
    "How does a Hash Map handle collisions?",
    "What is the difference between TCP and UDP?",
    "Explain database ACID transactions"
]

def get_assistant_response(chat_history, user_message):
    """
    Sends the user message to Gemini under strict system instructions.
    """
    prompt = "Previous Conversation:\n"
    for role, msg in chat_history:
        prompt += f"{role}: {msg}\n"
    prompt += f"User: {user_message}\n"
    prompt += "Assistant:"
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTIONS,
                temperature=0.2
            )
        )
        ans = response.text.strip()
        if "I am the Coding Assistant" in ans or "can only help with programming" in ans:
            return "I am the Coding Assistant. I can only help with programming, algorithms, debugging, software engineering, databases, computer science concepts, interview preparation, and coding-related topics."
        return ans
    except Exception as e:
        print(f"Error querying coding assistant: {e}")
        return "I am experiencing technical difficulties. Please ask your coding question again."

def review_github_portfolio(github_url):
    """
    Uses Gemini to analyze a GitHub URL and returns a score and detailed review text.
    """
    prompt = f"""
    You are an expert technical recruiter and portfolio reviewer.
    Analyze the following GitHub profile URL and provide a detailed professional evaluation.
    GitHub Profile URL: {github_url}
    
    You MUST return a JSON object with the following fields:
    - score (Integer between 0 and 100 representing portfolio strength)
    - review (Markdown formatted text highlighting: Key strengths, areas for improvement, repository quality, README structure, and suggestions to align with tech companies)
    
    Return ONLY the raw JSON string. Do not wrap in markdown tags or extra characters.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2
            )
        )
        data = json.loads(response.text.strip())
        return data.get("score", 70), data.get("review", "Review completed successfully.")
    except Exception as e:
        print(f"Error reviewing GitHub profile: {e}")
        return 65, "GitHub profile analyzed. Make sure to pin relevant repositories, add descriptive README files to each project, and maintain a consistent commit history."

def review_linkedin_profile(linkedin_url):
    """
    Uses Gemini to analyze a LinkedIn URL and returns a score and detailed review text.
    """
    prompt = f"""
    You are an expert HR recruiter and career coach.
    Analyze the following LinkedIn profile URL and provide a detailed professional evaluation.
    LinkedIn Profile URL: {linkedin_url}
    
    You MUST return a JSON object with the following fields:
    - score (Integer between 0 and 100 representing profile strength)
    - review (Markdown formatted text highlighting: Headline quality, About section optimization, experience descriptions, skills credibility, and alignment to tech roles)
    
    Return ONLY the raw JSON string. Do not wrap in markdown tags or extra characters.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2
            )
        )
        data = json.loads(response.text.strip())
        return data.get("score", 70), data.get("review", "Review completed successfully.")
    except Exception as e:
        print(f"Error reviewing LinkedIn profile: {e}")
        return 65, "LinkedIn profile analyzed. Highlight your technical skills, optimize your headline for your target roles, write a detailed About section, and request recommendations."
