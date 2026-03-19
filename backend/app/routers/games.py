from fastapi import APIRouter
from app.schemas.prompt import GameFilters
from app.schemas.game import GameResult
from app.services.rawg_service import fetch_games

router = APIRouter(prefix="/games", tags=["games"])


@router.post("/recommend", response_model=list[GameResult])
async def recommend_games(filters: GameFilters):
    results = fetch_games(filters)
    return [GameResult(**game) for game in results]
