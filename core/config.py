import os
from dotenv import load_dotenv

from pydantic_settings import BaseSettings
from pathlib import Path

 


class Settings(BaseSettings):
    DB_USER:str
    DB_HOST:str
    DB_PORT:str
    DB_PASSWORD:str
    DB_NAME:str
    DB_DRIVER:str
    DB_DIALECT:str
    JWT_SECRET:str
    JWT_ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    BUCKET_SECRET_KEY:str
    BUCKET_ENDPOINT:str
    BUCKET_ACCESS_KEY:str
    BUCKET_NAME:str
    BUCKET_ID:str

    
    def get_db_url(self):
        return f"{self.DB_DIALECT}+{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    
    def get_token_congigurations(self):
        return {
            "algorithm": self.JWT_ALGORITHM,
            "secret": self.JWT_SECRET,
            "expiry_minutes": self.ACCESS_TOKEN_EXPIRE_MINUTES
        }
    
    def get_bucket_endpoint(self):
        return self.BUCKET_ENDPOINT
    
    def get_bucket_secret_key(self):
        return self.BUCKET_SECRET_KEY
    
    def get_bucket_access_key(self):
        return self.BUCKET_ACCESS_KEY
    
    def get_bucket_name(self):
        return self.BUCKET_NAME
    
    
    
    class Config:
        env_file = ".env"

def get_settings() -> Settings:
    return Settings()
