import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "SatQuery AI"
    SUPABASE_DB_URL: str = os.getenv("SUPABASE_DB_URL", "postgresql://postgres:postgres@localhost:5432/postgres")
    SUPABASE_PROJECT_URL: str = os.getenv("SUPABASE_PROJECT_URL", "")
    SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", SUPABASE_DB_URL)
    JWT_SECRET: str = os.getenv("JWT_SECRET", "super-secret-key-for-dev-only")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 1 week
    STORAGE_BUCKET: str = os.getenv("STORAGE_BUCKET", "satquery")
    STORAGE_ENDPOINT: str = os.getenv("STORAGE_ENDPOINT", "http://localhost:9000")
    MINIO_ROOT_USER: str = os.getenv("MINIO_ROOT_USER", "admin")
    MINIO_ROOT_USER: str = os.getenv("MINIO_ROOT_USER", "admin")
    MINIO_ROOT_PASSWORD: str = os.getenv("MINIO_ROOT_PASSWORD", "password")
    cors_origins: list[str] = [origin.strip() for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000,http://localhost:8000,http://127.0.0.1:8000").split(",") if origin.strip()]

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
