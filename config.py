import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'aOklcBhmQ-5Q7KEvTEPy6L8wJkYUKU-qMR5V8v9pJlRhxLlKnvYuz-H2-84TTWzBidE'
    
    # PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://admin:3132@localhost/microcreditos'
    SQLALCHEMY_TRACK_MODIFICATIONS = False