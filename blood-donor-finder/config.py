"""
config.py – LifeLine Blood Donor Finder
Configuration loaded from environment variables with sensible local defaults.
"""
import os


class Config:
    # ── Flask ────────────────────────────────────────────────────────────────
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "change-me-in-production-lifeline-2025")
    DEBUG: bool = os.environ.get("FLASK_DEBUG", "true").lower() == "true"

    # ── MySQL ─────────────────────────────────────────────────────────────────
    DB_HOST: str = os.environ.get("DB_HOST", "localhost")
    DB_PORT: int = int(os.environ.get("DB_PORT", 3306))
    DB_USER: str = os.environ.get("DB_USER", "root")
    DB_PASSWORD: str = os.environ.get("DB_PASSWORD", "")
    DB_NAME: str = os.environ.get("DB_NAME", "blood_donor_finder")

    # Connection pool
    POOL_NAME: str = "lifeline_pool"
    POOL_SIZE: int = int(os.environ.get("POOL_SIZE", 5))
    POOL_RESET_SESSION: bool = True

    # ── Session ───────────────────────────────────────────────────────────────
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SAMESITE: str = "Lax"
    # Set to True behind HTTPS in production:
    SESSION_COOKIE_SECURE: bool = os.environ.get("SESSION_SECURE", "false").lower() == "true"
    PERMANENT_SESSION_LIFETIME: int = 3600  # 1 hour
