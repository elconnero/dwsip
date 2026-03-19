from pydantic import BaseModel
from datetime import datetime


class SaveGameRequest(BaseModel):
    rawg_id:          int
    name:             str
    background_image: str | None = None
    rating:           float | None = None
    metacritic:       int | None = None
    released:         str | None = None


class SavedGameResponse(BaseModel):
    id:               int
    rawg_id:          int
    name:             str
    background_image: str | None
    rating:           float | None
    metacritic:       int | None
    released:         str | None
    saved_at:         datetime

    class Config:
        from_attributes = True
