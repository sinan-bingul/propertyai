from pydantic_settings import BaseSettings 
from dotenv import load_dotenv

load_dotenv()
class Settings(BaseSettings):
    openai_api_key: str

settings = Settings()