from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Database
    database_url: str = "postgresql+asyncpg://corporate:corporate@db:5432/corporate_ai"

    # LLM
    openai_api_key: str = ""
    ollama_base_url: str = ""
    tavily_api_key: str = ""
    llm_model_name: str = "gpt-4o-mini"

    # Models
    bert_model_path: str = "/app/data/models/receptionist/final"
    embedding_model_name: str = "all-MiniLM-L6-v2"

    # App
    cors_origins: str = "http://localhost:3000"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]


settings = Settings()
