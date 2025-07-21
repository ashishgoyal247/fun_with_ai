from fastapi import FastAPI
import openai
import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()

# Set up OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    logger.info("OpenAI API key found and loaded successfully")
    openai.api_key = api_key
else:
    logger.error("OpenAI API key not found in environment variables")
    logger.error("Please check if OPENAI_API_KEY is set in your .env file")

def get_ai_news():
    logger.info("Attempting to fetch AI news from OpenAI")
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Give me one current AI news headline from today. Just the headline, nothing else."}
            ],
            max_tokens=100
        )
        logger.info("Successfully received response from OpenAI")
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error fetching AI news: {type(e).__name__}: {str(e)}")
        logger.error(f"Full exception details: {repr(e)}")
        return "Unable to fetch AI news at the moment"

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    ai_news = get_ai_news()
    logger.info("Returning response to client")
    return {
        "message": "Hello! Welcome to AI News App",
        "ai_news_today": ai_news
    }