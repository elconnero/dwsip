import httpx
from jose import jwt, JWTError
from fastapi import Header, HTTPException, status
from app.config import JWKS_URL


def get_jwks():
    response = httpx.get(JWKS_URL)
    return response.json()

def verify_token(token: str) -> dict:
    jwks = get_jwks()
    try:
        payload = jwt.decode(token, jwks, algorithms=["RS256"], options={"verify_aud": False})
        return payload
    except JWTError:
        return None

async def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token format")
    token = authorization.split(" ")[1]
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    return payload
