from pydantic import BaseModel


class GameResult(BaseModel):
    id:               int
    name:             str
    background_image: str | None = None
    rating:           float | None = None
    metacritic:       int | None = None
    released:         str | None = None
