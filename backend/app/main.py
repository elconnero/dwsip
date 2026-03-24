from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import prompt, games, saved_games, profile, account, my_games

app = FastAPI(title="DWISP API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prompt.router)
app.include_router(games.router)
app.include_router(saved_games.router)
app.include_router(profile.router)
app.include_router(account.router)
app.include_router(my_games.router)


@app.get("/health_check")
def health_check():
    return {"status": "healthy"}