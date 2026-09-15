from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    database_url: str
    redis_url: str


    jwt_secret_key: str

    access_token_expire_minutes: int
    refresh_token_expire_days: int

    environment: str
    
    upload_dir: str
    job_description_upload_dir: str
    
    gemini_api_key: str
    gemini_model: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()

print(
    "Gemini key loaded:",
    bool(settings.gemini_api_key),
)

print(
    "Gemini key prefix:",
    settings.gemini_api_key[:8]
    if settings.gemini_api_key
    else "MISSING",
)

print(
    "Gemini model:",
    settings.gemini_model,
)