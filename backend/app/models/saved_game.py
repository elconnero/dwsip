from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, func
from app.database import Base

class SavedGame(Base):
    __tablename__ = "saved_games"

    id = Column(Integer, primary_key=True)
    neon_user_id = Column(String(255), nullable=False)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    saved_at = Column(DateTime, server_default=func.now())

    __table_args__ = (UniqueConstraint("neon_user_id", "game_id"),)