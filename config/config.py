from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USER:Optional[str]
    DB_PASSWORD:Optional[str]
    DB_HOST:Optional[str]
    DB_PORT:Optional[int]
    DB_NAME:Optional[str]
    DB_CONNECTION:Optional[str]
    DB_DRIVER:Optional[str]

    
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS:int
    
    SMTP_EMAIL: str
    SMTP_PASSWORD: str
    SMTP_SERVER: str
    SMTP_PORT: int
    
    GOOGLE_CLIENT_ID:str
    GOOGLE_CLIENT_SECRET:str
    


    class Config:
        env_file = ".env"


      
class setting:
	PROJECT_NAME="websocket_project"
	PROJECT_VERSION="0.1.1"

      

    
settings = Settings()
