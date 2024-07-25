import jwt
from flask import current_app
from datetime import datetime, timedelta
import re


def generate_token(email, user_type="normal", expirationDays=30):
    payload = {
        'email': email,
        'userType': user_type,
        'exp': datetime.utcnow() + timedelta(days=expirationDays)  # Token expires in 1 hour
    }
    token = jwt.encode(
        payload, current_app.config['SECRET_KEY'], algorithm="HS256")
    return token





def validate_fields(data, required_fields):
    missing_fields = [
        field for field in required_fields 
        if field not in data or (isinstance(data[field], str) and not data[field].strip())
    ]
    return missing_fields


def validate_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None


def validate_password(password):
    # Example: Password must be at least 8 characters, contain at least one number, one uppercase letter, and one special character
    password_regex = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'
    return re.match(password_regex, password) is not None

def are_all_strings(*args):
    return all(isinstance(arg, str) for arg in args)


def allowed_file_img(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config["ALLOWED_IMG_EXTENSIONS"]
def allowed_file_video(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config["ALLOWED_VIDEO_EXTENSIONS"]