from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth import get_current_user
from app.models.recommendation import Recommendation, RecommendationGame
from app.models.saved_game import SavedGame
from app.models.user import RateLimit, UserViolation, UserPreferences

router = APIRouter(prefix="/account", tags=["account"])


@router.delete("")
async def delete_account(
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    neon_user_id = user["sub"]

    # Delete recommendation_games first (FK references recommendations)
    recommendation_ids = [
        r.id for r in db.query(Recommendation.id)
        .filter(Recommendation.neon_user_id == neon_user_id)
        .all()
    ]
    if recommendation_ids:
        db.query(RecommendationGame).filter(
            RecommendationGame.recommendation_id.in_(recommendation_ids)
        ).delete(synchronize_session=False)

    db.query(Recommendation).filter(Recommendation.neon_user_id == neon_user_id).delete()
    db.query(SavedGame).filter(SavedGame.neon_user_id == neon_user_id).delete()
    db.query(RateLimit).filter(RateLimit.neon_user_id == neon_user_id).delete()
    db.query(UserViolation).filter(UserViolation.neon_user_id == neon_user_id).delete()
    db.query(UserPreferences).filter(UserPreferences.neon_user_id == neon_user_id).delete()

    db.commit()

    return Response(status_code=204)
