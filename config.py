import os

class Config:
    SECRET_KEY = 'vetcare_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///vetcare.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False