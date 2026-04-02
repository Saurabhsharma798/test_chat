from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:str
    DATABASE_URL:str
    GEMINI_API_KEY:str


    model_config={'from_attributes':True}


settings=Settings()