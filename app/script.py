from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()
gemini_key = os.getenv("GEMINAI_API_KEY")
base_dir = Path(__file__).resolve().parent
email_path = base_dir / "email.txt"

PROMPT= """
You are an expert email analyst.

Analyze the following HTML email and extract:

- A score from 0 to 100 indicating the email's quality or relevance
- An engagement score from 0 to 100 indicating how engaging the email is likely to be
- Insights on areas for improvement (e.g., subject line, content quality, call to action)
- Warnings about potential issues (e.g., phishing, spam, sensitive content)
- The emotional tone (e.g., professional, friendly, urgent, angry)
- A field `spam_classification` that must be either:
  - `"spam"`
  - `"suspicious"`
  - `"not_spam"`

Respond in the following JSON format:
{
  "score": 0,
  "engagement": 0,
  "insights": ["string"],
  "tone": "string",
  "warnings": ["string"],
  "spam_classification": "spam" | "suspicious" | "not_spam"
}

Here is the email content (HTML):
<EMAIL_HTML>

"""
with open(email_path, "r", encoding="utf-8") as f:
    email_html = f.read().strip()


final_prompt = PROMPT.replace("<EMAIL_HTML>", email_html)

from google import genai

client = genai.Client(api_key=gemini_key)
completion = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=final_prompt,

)


print(completion.text)