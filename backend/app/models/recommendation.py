from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True)
    neon_user_id = Column(String(255), nullable=False)
    user_prompt = Column(Text, nullable=False)
    parsed_keywords = Column(JSONB)
    openai_game_predict = Column(JSONB)
    filters_used = Column(JSONB)
    was_valid = Column(Boolean, default=True)
    was_jailed = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

class RecommendationGame(Base):
    __tablename__ = "recommendation_games"

    id = Column(Integer, primary_key=True)
    recommendation_id = Column(Integer, ForeignKey("recommendations.id"), nullable=False)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    position = Column(Integer)
