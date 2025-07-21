from fastapi import FastAPI
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Set up OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_ai_news():
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Give me one current AI news headline from today. Just the headline, nothing else."}
            ],
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return "Unable to fetch AI news at the moment"

@app.get("/")
def read_root():
    ai_news = get_ai_news()
    return {
        "message": "Hello! Welcome to AI News App",
        "ai_news_today": ai_news
    }