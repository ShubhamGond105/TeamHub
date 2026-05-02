import os


class Config:
    SECRET_KEY = os.environ.get('JWT_SECRET', 'dev-secret-key-change-in-production')
    # Use /tmp/ for SQLite so Vercel doesn't crash on read-only filesystem if DATABASE_URL is missing
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:////tmp/taskmanager.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Fix for Railway PostgreSQL URL (uses postgres:// but SQLAlchemy needs postgresql://)
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://', 1)

    # Fix for Supabase Pooler (SQLAlchemy must use direct port 5432 instead of transaction port 6543)
    if SQLALCHEMY_DATABASE_URI and 'supabase.com:6543' in SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('6543', '5432')
