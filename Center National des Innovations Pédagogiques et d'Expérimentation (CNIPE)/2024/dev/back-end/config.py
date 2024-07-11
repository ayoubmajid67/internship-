import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    MONGO_URI = os.getenv('MONGO_URI')
    UPLOAD_FOLDER = 'data/profiles'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
