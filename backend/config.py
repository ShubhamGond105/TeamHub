import os


class Config:
    SECRET_KEY = os.environ.get('JWT_SECRET', 'dev-secret-key-change-in-production')
    
    # Get DB URL, strip it, and ensure it's not empty
    db_url = os.environ.get('DATABASE_URL', '').strip()
    if not db_url:
        db_url = 'sqlite:////tmp/taskmanager.db'

    # Fix for Railway PostgreSQL URL
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)

    # Fix for Supabase Pooler
    if 'supabase.com:6543' in db_url:
        db_url = db_url.replace('6543', '5432')

    # Force psycopg3 for Serverless compatibility
    if db_url.startswith('postgresql://'):
        db_url = db_url.replace('postgresql://', 'postgresql+psycopg://', 1)

    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
