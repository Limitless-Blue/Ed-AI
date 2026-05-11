from pathlib import Path
from pydantic_settings import BaseSettings

# Project root = three levels up from backend/app/config.py
ROOT = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    google_api_key: str

    content_dir: Path = ROOT / "content"
    data_dir: Path = ROOT / "data"
    chroma_dir: Path = ROOT / "data" / "chroma"

    model_config = {"env_file": str(ROOT / ".env")}


settings = Settings()
