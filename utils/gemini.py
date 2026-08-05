import os

from dotenv import load_dotenv

from google import genai

from utils.prompts import SYSTEM_PROMPT

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def ask_gemini(history, question):

    prompt = SYSTEM_PROMPT + "\n\n"

    for role, msg in history:

        prompt += f"{role}: {msg}\n"

    prompt += f"User: {question}"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text