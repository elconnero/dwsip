from pydantic import BaseModel
from app.schemas.prompt import GameFilters


class GameResult(BaseModel):
    id:               int
    name:             str
    background_image: str | None = None
    rating:           float | None = None
    metacritic:       int | None = None
    released:         str | None = None


class RecommendRequest(GameFilters):
    user_prompt: str | None = None
