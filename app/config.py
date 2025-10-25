from pydantic import BaseSettings, Field, AnyHttpUrl
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "truthguard"
    APP_ENV: str = "development"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    APP_SECRET_KEY: str = Field(..., env="APP_SECRET_KEY")
    FERNET_KEY: Optional[str] = Field(None, env="FERNET_KEY")  
    OPENAI_API_KEY: Optional[str] = Field(None, env="OPENAI_API_KEY")
    GEMINI_API_KEY: Optional[str] = Field(None, env="GEMINI_API_KEY")

    SERPAPI_KEY: Optional[str] = Field(None, env="SERPAPI_KEY")
    BING_SEARCH_KEY: Optional[str] = Field(None, env="BING_SEARCH_KEY")
    GOOGLE_CUSTOM_SEARCH_KEY: Optional[str] = Field(None, env="GOOGLE_CUSTOM_SEARCH_KEY")
    GOOGLE_CSE_ID: Optional[str] = Field(None, env="GOOGLE_CSE_ID")

    MONGO_URI: Optional[str] = Field(None, env="MONGO_URI")

    MAX_CLAIMS: int = Field(30, env="MAX_CLAIMS")
    SEARCH_RESULTS_PER_PROVIDER: int = Field(3, env="SEARCH_RESULTS_PER_PROVIDER")
    MAX_EVIDENCE_PER_CLAIM: int = Field(6, env="MAX_EVIDENCE_PER_CLAIM")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

