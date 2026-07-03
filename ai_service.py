import os
from dotenv import load_dotenv
from google import genai
from prompt import SYSTEM_PROMPT
from email_context import build_email_context
from email_classifier import classify_email
from prompt_selector import get_prompt

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_reply(email):
    context = build_email_context(email)
    category = classify_email(email)
    System_prompt = get_prompt(category)

    prompt = f"""{SYSTEM_PROMPT}
    Email Information: {context}
    Write only the reply."""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt)
    return {
        "category": category,
        "reply": response.text
    }
