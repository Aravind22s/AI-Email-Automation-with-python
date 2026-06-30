from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


Categories = ["GENERAL", "HR", "INTERVIEW", "CUSTOMER_SUPPORT",
              "COMPLAINT", "SALES", "LEAVE_REQUEST"]

def classify_email(email):
    prompt = f"""
    You are an email classifier.
    Return ONLY ONE category.
    Available Categories: {Categories}
    Email Information: 
    Email Subject: {email["subject"]}
    Email Body:{email["body"]}"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt)
    return response.text.strip()