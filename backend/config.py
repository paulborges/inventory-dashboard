import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY','dev-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    JWT_EXPIRATION_HOURS = 96