import os


class Config:
    SECRET_KEY = os.environ.get('JWT_SECRET', 'dev-secret-key-change-in-production')
    # Use /tmp/ for SQLite so Vercel doesn't crash on read-only filesystem if DATABASE_URL is missing
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:////tmp/taskmanager.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Fix for Railway PostgreSQL URL (uses postgres:// but SQLAlchemy needs postgresql://)
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://', 1)
