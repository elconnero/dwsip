# I am glad we are here
from pydantic import BaseModel


class PromptRequest(BaseModel):
    prompt: str


class GameFilters(BaseModel):
    genres:         list[str] = []
    tags:           list[str] = []
    mood:           str = ""
    multiplayer:    bool = False
    platforms:      list[str] = []
    search_query:   str = ""
    predicted_game: str | None = None
