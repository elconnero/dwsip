import base64
import httpx
import jwt as pyjwt
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from fastapi import Header, HTTPException, status
from app.config import JWKS_URL


def _b64url_decode(s: str) -> bytes:
    s += "=" * (4 - len(s) % 4)
    return base64.urlsafe_b64decode(s)


def get_jwks():
    response = httpx.get(JWKS_URL)
    return response.json()


def verify_token(token: str) -> dict:
    try:
        header = pyjwt.get_unverified_header(token)
        kid = header.get("kid")

        jwks = get_jwks()
        matching_key = next(
            (k for k in jwks["keys"] if k.get("kid") == kid),
            None,
        )
        if not matching_key:
            print(f"[auth] No JWKS key found for kid: {kid}")
            return None

        public_key = Ed25519PublicKey.from_public_bytes(_b64url_decode(matching_key["x"]))
        payload = pyjwt.decode(
            token,
            public_key,
            algorithms=["EdDSA"],
            options={"verify_aud": False},
        )
        return payload
    except Exception as e:
        print(f"[auth] JWT verification failed: {e}")
        return None


async def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token format")
    token = authorization.split(" ")[1]
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    return payload
