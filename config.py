import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    MONGO_URI = os.environ.get(
        "MONGO_URI",
        "mongodb://localhost:27017"
    )

    DB_NAME = os.environ.get(
        "DB_NAME",
        "ai_prompt_db"
    )

    OPENAI_API_KEY = os.environ.get(
        "OPENAI_API_KEY",
        "mock_key"
    )