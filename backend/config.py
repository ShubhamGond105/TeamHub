import os


class Config:
    SECRET_KEY = os.environ.get('JWT_SECRET', 'dev-secret-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///taskmanager.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Fix for Railway PostgreSQL URL (uses postgres:// but SQLAlchemy needs postgresql://)
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://', 1)
