from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    database_url: str

    jwt_secret_key: str

    access_token_expire_minutes: int
    refresh_token_expire_days: int

    environment: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()