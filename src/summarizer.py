from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def summarize(title: str, description: str) -> str:
    prompt = f"""You are a helpful assistant that writes short, clear summaries for a daily news digest.

Video title: {title}

YouTube description:
{description[:1000]}

Write exactly 2 sentences summarizing what this video is about. Be specific and informative. No fluff."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()