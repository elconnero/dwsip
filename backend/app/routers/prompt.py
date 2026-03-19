from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.prompt import PromptRequest, GameFilters
from app.services.openai_service import openai_generate_json
from app.services.rate_limit import check_and_increment
from app.services.auth import verify_token
from app.database import get_db

router = APIRouter(prefix="/prompt", tags=["prompt"])


@router.post("/parse", response_model=GameFilters)
async def parse_prompt(
    body: PromptRequest,
    db: Session = Depends(get_db),
    authorization: str | None = None,
):
    # If logged in, enforce daily rate limit
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        payload = verify_token(token)
        if payload:
            allowed = check_and_increment(payload["sub"], db)
            if not allowed:
                raise HTTPException(
                    status_code=429,
                    detail="DAILY LIMIT REACHED. COME BACK TOMORROW."
                )

    result = openai_generate_json(body.prompt)
    return GameFilters(**result)
