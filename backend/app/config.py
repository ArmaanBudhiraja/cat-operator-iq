import os
from pathlib import Path
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"

# Ensure directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)
KNOWLEDGE_BASE_DIR.mkdir(parents=True, exist_ok=True)

class Settings(BaseModel):
    PROJECT_NAME: str = "CAT OperatorIQ"
    TAGLINE: str = "Your intelligent companion for safer and smarter machine operations."
    SAFETY_DISCLAIMER: str = (
        "AI-generated recommendations are advisory and must not replace official "
        "operating procedures, safety procedures, operator training, or professional judgment."
    )
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{DATA_DIR}/cat_operator_iq.db")
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY", None)
    WEATHER_API_KEY: str | None = os.getenv("WEATHER_API_KEY", None)
    CORS_ORIGINS: list[str] = ["*"]
    RANDOM_SEED: int = int(os.getenv("RANDOM_SEED", 42))

settings = Settings()
