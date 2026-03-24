from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from app.schemas.game import GameResult, RecommendRequest
from app.services.rawg_service import fetch_games
from app.services.auth import verify_token
from app.database import get_db
from app.models.game import Game
from app.models.recommendation import Recommendation, RecommendationGame

router = APIRouter(prefix="/games", tags=["games"])


@router.post("/recommend", response_model=list[GameResult])
async def recommend_games(
    filters: RecommendRequest,
    db: Session = Depends(get_db),
    authorization: str | None = Header(default=None),
):
    results = fetch_games(filters)
    game_results = [GameResult(**game) for game in results]

    # Save recommendation history for logged-in users
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        payload = verify_token(token)
        if payload and filters.user_prompt:
            # Upsert each game into the games table
            db_games = []
            for g in game_results:
                db_game = db.query(Game).filter(Game.rawg_id == g.id).first()
                if not db_game:
                    db_game = Game(
                        rawg_id=g.id,
                        name=g.name,
                        background_image=g.background_image,
                        metacritic_score=g.metacritic,
                    )
                    db.add(db_game)
                    db.flush()
                db_games.append(db_game)

            # Create the recommendation row
            rec = Recommendation(
                neon_user_id=payload["sub"],
                user_prompt=filters.user_prompt,
            )
            db.add(rec)
            db.flush()

            # Link each game to the recommendation
            for position, db_game in enumerate(db_games):
                db.add(RecommendationGame(
                    recommendation_id=rec.id,
                    game_id=db_game.id,
                    position=position,
                ))

            db.commit()

    return game_results
