import os


class Config:
    postUrl = 'postgresql://postgres:tobi@localhost/handyhub_db'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', postUrl)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
