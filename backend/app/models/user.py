from sqlalchemy import Column, Integer, String, DateTime, Date, func
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base

class UserViolation(Base):
    __tablename__ = "user_violations"

    id = Column(Integer, primary_key=True)
    neon_user_id = Column(String(255), unique=True, nullable=False)
    jail_count = Column(Integer, default=0)
    banned_at = Column(DateTime, nullable=True)
    banned_until = Column(DateTime, nullable=True)
    last_violation_at = Column(DateTime)

class RateLimit(Base):
    __tablename__ = "rate_limits"

    id = Column(Integer, primary_key=True)
    neon_user_id = Column(String(255), nullable=False)
    request_date = Column(Date, nullable=False)
    request_count = Column(Integer, default=0)

class UserPreferences(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True)
    neon_user_id = Column(String(255), unique=True, nullable=False)
    platforms = Column(JSONB, default=list)
    excluded_tags = Column(JSONB, default=list)
    excluded_genres = Column(JSONB, default=list)
    min_metacritic = Column(Integer, nullable=True)
    max_metacritic = Column(Integer, nullable=True)
    release_year_min = Column(Integer, nullable=True)
    release_year_max = Column(Integer, nullable=True)
    multiplayer_pref = Column(String(20), default="any")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())