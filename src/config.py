from pydantic import BaseSettings, SecretStr

class Settings(BaseSettings):
    MONGO_DB_URI: str
    JWT_SECRET_KEY: str
    
    class Config:
        case_sensitive = True


settings = Settings()  # type: ignore
