import os

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/auth_db")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "my_super_secret_jwt_key")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = int(os.getenv("JWT_EXPIRATION_MINUTES", "30"))

settings = Settings()
