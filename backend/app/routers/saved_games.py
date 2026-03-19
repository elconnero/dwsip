from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth import get_current_user
from app.models.game import Game
from app.models.saved_game import SavedGame
from app.schemas.saved_game import SaveGameRequest, SavedGameResponse

router = APIRouter(prefix="/saved-games", tags=["saved-games"])


@router.post("", response_model=SavedGameResponse, status_code=status.HTTP_201_CREATED)
async def save_game(
    body: SaveGameRequest,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Upsert game into our games table
    game = db.query(Game).filter(Game.rawg_id == body.rawg_id).first()
    if not game:
        game = Game(
            rawg_id=body.rawg_id,
            name=body.name,
            background_image=body.background_image,
            metacritic_score=body.metacritic,
        )
        db.add(game)
        db.commit()
        db.refresh(game)

    # Check if already saved
    existing = db.query(SavedGame).filter(
        SavedGame.neon_user_id == user["sub"],
        SavedGame.game_id == game.id,
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Game already saved")

    saved = SavedGame(neon_user_id=user["sub"], game_id=game.id)
    db.add(saved)
    db.commit()
    db.refresh(saved)

    return SavedGameResponse(
        id=saved.id,
        rawg_id=game.rawg_id,
        name=game.name,
        background_image=game.background_image,
        rating=body.rating,
        metacritic=game.metacritic_score,
        released=body.released,
        saved_at=saved.saved_at,
    )


@router.get("", response_model=list[SavedGameResponse])
async def get_saved_games(
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    rows = (
        db.query(SavedGame, Game)
        .join(Game, SavedGame.game_id == Game.id)
        .filter(SavedGame.neon_user_id == user["sub"])
        .order_by(SavedGame.saved_at.desc())
        .all()
    )

    return [
        SavedGameResponse(
            id=saved.id,
            rawg_id=game.rawg_id,
            name=game.name,
            background_image=game.background_image,
            rating=None,
            metacritic=game.metacritic_score,
            released=None,
            saved_at=saved.saved_at,
        )
        for saved, game in rows
    ]


@router.delete("/{rawg_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_saved_game(
    rawg_id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    game = db.query(Game).filter(Game.rawg_id == rawg_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    saved = db.query(SavedGame).filter(
        SavedGame.neon_user_id == user["sub"],
        SavedGame.game_id == game.id,
    ).first()
    if not saved:
        raise HTTPException(status_code=404, detail="Saved game not found")

    db.delete(saved)
    db.commit()
