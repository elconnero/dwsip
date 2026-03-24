from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.services.auth import verify_token
from app.models.recommendation import Recommendation, RecommendationGame
from app.models.game import Game

router = APIRouter(prefix="/my-games", tags=["my-games"])


class MyGameItem(BaseModel):
    rawg_id:          int
    name:             str
    background_image: str | None = None


class MyRecommendation(BaseModel):
    id:          int
    user_prompt: str
    created_at:  str
    games:       list[MyGameItem]


@router.get("", response_model=list[MyRecommendation])
async def get_my_games(
    db: Session = Depends(get_db),
    authorization: str | None = Header(default=None),
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="NOT LOGGED IN")

    token = authorization.split(" ")[1]
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="INVALID TOKEN")

    recs = (
        db.query(Recommendation)
        .filter(Recommendation.neon_user_id == payload["sub"])
        .order_by(Recommendation.created_at.desc())
        .all()
    )

    results = []
    for rec in recs:
        links = (
            db.query(RecommendationGame)
            .filter(RecommendationGame.recommendation_id == rec.id)
            .order_by(RecommendationGame.position)
            .all()
        )
        games = []
        for link in links:
            game = db.query(Game).filter(Game.id == link.game_id).first()
            if game:
                games.append(MyGameItem(
                    rawg_id=game.rawg_id,
                    name=game.name,
                    background_image=game.background_image,
                ))
        results.append(MyRecommendation(
            id=rec.id,
            user_prompt=rec.user_prompt,
            created_at=rec.created_at.isoformat(),
            games=games,
        ))

    return results
