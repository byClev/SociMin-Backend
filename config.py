from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY                          = os.environ.get('SECRET_KEY') or 'dev-key-very-secret'
    SQLALCHEMY_DATABASE_URI             = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS      = False
    JWT_ACCESS_TOKEN_EXPIRES            = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES           = timedelta(days=30)
    JWT_SECRET_KEY                      = os.environ.get('JWT_SECRET_KEY') or SECRET_KEY