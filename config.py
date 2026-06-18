import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'vetcare_secret_key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///vetcare.db').replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False