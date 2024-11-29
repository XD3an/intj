from pydantic_settings  import BaseSettings

class Settings(BaseSettings):
    model: str
    model_base_url: str
    
    class Config:
        env_file = ".env"

settings = Settings()