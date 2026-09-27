import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    app_name = os.getenv("APP_NAME", "FitBuddy AI")
    database_url = os.getenv("DATABASE_URL", "sqlite:///./fitbuddy.db")

    # Admin dashboard token (used to gate /view-all-users)
    admin_token = os.getenv("ADMIN_TOKEN", "changeme")

    # Gemini API configuration
    gemini_api_key = os.getenv("GEMINI_API_KEY", "")
    workout_model = os.getenv("WORKOUT_MODEL", "gemini-2.0-flash")
    nutrition_model = os.getenv("NUTRITION_MODEL", "gemini-2.0-flash")


settings = Settings()
