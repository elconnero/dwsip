from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth import get_current_user
from app.models.saved_game import SavedGame
from app.models.recommendation import Recommendation
from app.models.user import RateLimit
from datetime import date

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("")
async def get_profile(
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    neon_user_id = user["sub"]

    saved_count = db.query(SavedGame).filter(
        SavedGame.neon_user_id == neon_user_id
    ).count()

    recommendation_count = db.query(Recommendation).filter(
        Recommendation.neon_user_id == neon_user_id
    ).count()

    today_limit = db.query(RateLimit).filter(
        RateLimit.neon_user_id == neon_user_id,
        RateLimit.request_date == date.today(),
    ).first()

    requests_today = today_limit.request_count if today_limit else 0

    return {
        "user_id":            neon_user_id,
        "email":              user.get("email"),
        "saved_games":        saved_count,
        "total_searches":     recommendation_count,
        "requests_today":     requests_today,
        "daily_limit":        20,
    }
