from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, func
from app.database import Base

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    rawg_id = Column(Integer, unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    metacritic_score = Column(Integer)
    background_image = Column(String(500))
    released = Column(Date)
    trailer_url = Column(String(500))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class GameStore(Base):
    __tablename__ = "game_stores"

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    store_name = Column(String(100), nullable=False)
    store_url = Column(String(500), nullable=False)

class GameGenre(Base):
    __tablename__ = "game_genres"

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    genre_name = Column(String(100), nullable=False)

class GameTag(Base):
    __tablename__ = "game_tags"

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    tag_name = Column(String(100), nullable=False)