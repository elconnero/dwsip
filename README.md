# DWISP — Dude, What Should I Play?

DWISP is a web app that helps gamers decide what to play next when they're stuck endlessly scrolling their backlog. You describe how you're feeling, what kind of experience you want, or how much time you have — and DWISP uses AI to recommend three games tailored to that moment. It pulls real game data from a massive database and filters results based on your platform, rating preferences, and content settings so the suggestions actually make sense for you.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React, TypeScript, Vite, Tailwind CSS v4 |
| Backend | FastAPI (Python) |
| Database | PostgreSQL via Neon (serverless) |
| ORM / Migrations | SQLAlchemy + Alembic |
| Authentication | Neon Auth (JWT) |
| AI | OpenAI API (gpt-4o-mini) |
| Game Data | RAWG API |

---

## How It Works

```
User types a prompt (e.g. "something relaxing like Zelda")
        │
        ▼
Pre-flight checks
  - Is the user banned?
  - Have they hit their daily limit? (20 searches/day)
        │
        ▼
OpenAI parses the prompt
  - Extracts genres, tags, mood, platform, search query
  - Flags invalid or abusive prompts (jail system)
        │
        ▼
RAWG API is queried
  - Uses AI-extracted filters + user preferences
  - Returns top 3 games ordered by rating
        │
        ▼
Results are cached in the database
  - Games, genres, tags, and store links saved
  - Recommendation logged to user history
        │
        ▼
Frontend displays 3 GameCards
  - Cover image, title, Metacritic score
  - Store links (Steam, PS Store, etc.)
  - Save button to bookmark the game
```

---

## Database Schema

DWISP uses 10 tables. Users are managed by Neon Auth — only their `neon_user_id` is stored here to link data.

| Table | Purpose |
|---|---|
| `games` | Cached game data from RAWG (avoids repeat API calls) |
| `game_stores` | Store links per game (Steam, PlayStation Store, etc.) |
| `game_genres` | Genres per game (RPG, Action, etc.) |
| `game_tags` | Tags per game (Open World, Story Rich, etc.) |
| `recommendations` | Every search a user runs, with prompt and filters |
| `recommendation_games` | Junction table — links recommendations to games |
| `saved_games` | Games a user has bookmarked |
| `user_violations` | Tracks prompt abuse (jail count + bans) |
| `rate_limits` | Daily search limits per user |
| `user_preferences` | Default filters saved per user |

### Relationships

```
games (1) ──▶ game_stores (many)
games (1) ──▶ game_genres (many)
games (1) ──▶ game_tags (many)

recommendations (1) ──▶ recommendation_games (many) ──▶ games (many)

saved_games (many) ──▶ games (1)

neon_user_id links:
  recommendations, saved_games, user_violations, rate_limits, user_preferences
```

---

## Local Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- A [Neon](https://neon.tech) database (free tier works)
- An [OpenAI](https://platform.openai.com) API key
- A [RAWG](https://rawg.io/apidocs) API key

---

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/dwsip.git
cd dwsip
```

---

### 2. Backend setup

```bash
cd backend

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

Create `backend/.env`:

```env
DATABASE_URL=your_neon_connection_string
OPENAI_API_KEY=your_openai_key
RAWG_API_KEY=your_rawg_key
JWKS_URL=your_neon_auth_jwks_url
```

Run database migrations:

```bash
alembic upgrade head
```

Start the backend:

```bash
uvicorn app.main:app --reload
```

Backend runs at `http://localhost:8000`

---

### 3. Frontend setup

```bash
cd frontend
npm install
```

Create `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000
VITE_NEON_AUTH_URL=your_neon_auth_url
```

Start the frontend:

```bash
npm run dev
```

Frontend runs at `http://localhost:5173`

---

## Features

- **AI-powered recommendations** — describe your mood or vibe, get 3 matching games
- **Smart filtering** — filter by platform, Metacritic score, release year, genre, and tags
- **Saved preferences** — set default filters once, applied automatically every search
- **Save games** — bookmark games to revisit later
- **Guest access** — try one search without signing up
- **Rate limiting** — 20 searches/day per logged-in user
- **Abuse protection** — prompt jail system with escalating bans for bad actors
- **Profile page** — view your stats, saved count, and daily usage

---

## Project Structure

```
dwsip/
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI app + CORS
│   │   ├── database.py        # SQLAlchemy setup
│   │   ├── models/            # SQLAlchemy table models
│   │   ├── routers/           # API route handlers
│   │   ├── schemas/           # Pydantic request/response schemas
│   │   └── services/          # OpenAI, RAWG, auth, rate limiting logic
│   ├── alembic/               # Database migrations
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── pages/             # Home, SavedGames, Profile, Auth
    │   ├── components/        # Navbar, GameCard, LoadingSpinner
    │   ├── hooks/             # useAuth
    │   ├── services/          # Axios API client
    │   └── types/             # TypeScript interfaces
    └── package.json
```

---

## Environment Variables Reference

### Backend (`backend/.env`)

| Variable | Description |
|---|---|
| `DATABASE_URL` | Neon PostgreSQL connection string |
| `OPENAI_API_KEY` | OpenAI API key |
| `RAWG_API_KEY` | RAWG API key |
| `JWKS_URL` | Neon Auth JWKS endpoint for JWT verification |

### Frontend (`frontend/.env`)

| Variable | Description |
|---|---|
| `VITE_API_URL` | URL of the running backend |
| `VITE_NEON_AUTH_URL` | Neon Auth base URL |
