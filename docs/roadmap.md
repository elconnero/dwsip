# DWISP Development Roadmap

## Phase 1: Project Setup
> Get the foundation in place

- [ ] **Step 1.1** - Create folder structure
  ```
  dwisp/
  ├── frontend/
  ├── backend/
  └── docs/
  ```

- [ ] **Step 1.2** - Initialize Git repository
  ```bash
  git init
  git add .
  git commit -m "Initial project structure"
  ```

- [ ] **Step 1.3** - Set up Python virtual environment
  ```bash
  cd backend
  python -m venv venv
  source venv/bin/activate  # Linux/Mac
  ```

- [ ] **Step 1.4** - Create `backend/requirements.txt`
  ```
  fastapi
  uvicorn[standard]
  sqlalchemy
  alembic
  psycopg2-binary
  python-jose[cryptography]
  passlib[bcrypt]
  python-dotenv
  openai
  httpx
  pydantic
  ```

- [ ] **Step 1.5** - Install Python dependencies
  ```bash
  pip install -r requirements.txt
  ```

- [ ] **Step 1.6** - Initialize React frontend
  ```bash
  cd frontend
  npm create vite@latest . -- --template react-ts
  npm install
  npm install tailwindcss postcss autoprefixer axios react-router-dom
  npx tailwindcss init -p
  ```

- [ ] **Step 1.7** - Create `.env` files
  ```
  # backend/.env
  DATABASE_URL=
  OPENAI_API_KEY=
  RAWG_API_KEY=
  JWT_SECRET=

  # frontend/.env
  VITE_API_URL=http://localhost:8000
  ```

---

## Phase 2: Backend Foundation
> Set up FastAPI and basic structure

- [ ] **Step 2.1** - Create backend folder structure
  ```
  backend/
  ├── app/
  │   ├── __init__.py
  │   ├── main.py           # FastAPI app entry
  │   ├── config.py         # Environment variables
  │   ├── database.py       # Database connection
  │   ├── models/           # SQLAlchemy models
  │   ├── schemas/          # Pydantic schemas
  │   ├── routers/          # API routes
  │   └── services/         # Business logic
  ├── alembic/              # Migrations
  ├── requirements.txt
  └── .env
  ```

- [ ] **Step 2.2** - Create `app/main.py` with basic FastAPI app
  ```python
  from fastapi import FastAPI
  from fastapi.middleware.cors import CORSMiddleware

  app = FastAPI(title="DWISP API")

  app.add_middleware(
      CORSMiddleware,
      allow_origins=["http://localhost:5173"],
      allow_methods=["*"],
      allow_headers=["*"],
  )

  @app.get("/health")
  def health_check():
      return {"status": "healthy"}
  ```

- [ ] **Step 2.3** - Test backend runs
  ```bash
  uvicorn app.main:app --reload
  # Visit http://localhost:8000/docs for Swagger UI
  ```

---

## Phase 3: Database Setup
> Set up PostgreSQL and define your schema

- [ ] **Step 3.1** - Sign up for Neon (https://neon.tech) - get your DATABASE_URL

- [ ] **Step 3.2** - Create `app/database.py` with SQLAlchemy setup

- [ ] **Step 3.3** - Initialize Alembic
  ```bash
  alembic init alembic
  ```

- [ ] **Step 3.4** - Create SQLAlchemy models in `app/models/`
  - `user.py` - User model
  - `recommendation.py` - Recommendation model
  - `game.py` - Game model
  - `saved_game.py` - UserSavedGame model

- [ ] **Step 3.5** - Create first migration
  ```bash
  alembic revision --autogenerate -m "initial tables"
  alembic upgrade head
  ```

---

## Phase 4: Authentication
> Let users sign up and log in

- [ ] **Step 4.1** - Create Pydantic schemas in `app/schemas/`
  - `user.py` - UserCreate, UserLogin, UserResponse

- [ ] **Step 4.2** - Create auth utilities in `app/services/auth.py`
  - Password hashing with passlib
  - JWT token creation/verification with python-jose

- [ ] **Step 4.3** - Create auth router in `app/routers/auth.py`
  - POST `/auth/register` - Create new user
  - POST `/auth/login` - Return JWT token
  - GET `/auth/me` - Get current user (protected)

- [ ] **Step 4.4** - Create dependency for protected routes
  ```python
  def get_current_user(token: str = Depends(oauth2_scheme)):
      # Verify JWT and return user
  ```

- [ ] **Step 4.5** - Test auth endpoints in Swagger UI

---

## Phase 5: OpenAI Integration
> Turn user prompts into game filters

- [ ] **Step 5.1** - Get OpenAI API key from https://platform.openai.com

- [ ] **Step 5.2** - Create `app/services/openai_service.py`

- [ ] **Step 5.3** - Design your JSON schema for game filters
  ```json
  {
    "genres": ["rpg", "action"],
    "tags": ["story-rich", "open-world"],
    "mood": "relaxing",
    "multiplayer": false,
    "platforms": ["pc"]
  }
  ```

- [ ] **Step 5.4** - Write the OpenAI prompt that generates this JSON

- [ ] **Step 5.5** - Create router in `app/routers/prompt.py`
  - POST `/prompt/parse` - Takes user prompt, returns game filters

- [ ] **Step 5.6** - Add JSON validation with Pydantic

- [ ] **Step 5.7** - Test with various user inputs

---

## Phase 6: Gaming API Integration
> Fetch real game recommendations

- [ ] **Step 6.1** - Sign up for RAWG API at https://rawg.io/apidocs

- [ ] **Step 6.2** - Create `app/services/rawg_service.py`

- [ ] **Step 6.3** - Map your JSON filters to RAWG query parameters

- [ ] **Step 6.4** - Create router in `app/routers/games.py`
  - POST `/games/recommend` - Takes filters, returns game list

- [ ] **Step 6.5** - Test the full flow: prompt → OpenAI → RAWG → results

---

## Phase 7: Frontend Foundation
> Build the React app structure

- [ ] **Step 7.1** - Set up folder structure
  ```
  frontend/src/
  ├── components/        # Reusable UI components
  ├── pages/            # Route pages
  ├── services/         # API calls
  ├── hooks/            # Custom React hooks
  ├── context/          # Auth context
  ├── types/            # TypeScript types
  └── App.tsx
  ```

- [ ] **Step 7.2** - Configure Tailwind CSS

- [ ] **Step 7.3** - Set up React Router in `App.tsx`
  - `/` - Home page
  - `/login` - Login page
  - `/signup` - Signup page
  - `/saved` - Saved games page

- [ ] **Step 7.4** - Create API service in `services/api.ts`
  ```typescript
  import axios from 'axios';

  const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
  });
  ```

- [ ] **Step 7.5** - Create auth context for managing login state

---

## Phase 8: Frontend UI
> Build the main user interface

- [ ] **Step 8.1** - Create Navbar component

- [ ] **Step 8.2** - Create Login page

- [ ] **Step 8.3** - Create Signup page

- [ ] **Step 8.4** - Create Home page with prompt input

- [ ] **Step 8.5** - Create GameCard component

- [ ] **Step 8.6** - Create Results display (grid of GameCards)

- [ ] **Step 8.7** - Add loading states and spinners

- [ ] **Step 8.8** - Add error handling and error messages

---

## Phase 9: Save & Like Features
> Let users save their favorites

- [ ] **Step 9.1** - Create backend endpoints in `app/routers/saved_games.py`
  - POST `/saved-games` - Save a game
  - GET `/saved-games` - Get user's saved games
  - DELETE `/saved-games/{id}` - Remove saved game

- [ ] **Step 9.2** - Add save/like buttons to GameCard component

- [ ] **Step 9.3** - Create Saved Games page

- [ ] **Step 9.4** - Show recommendation history

---

## Phase 10: Polish & Deploy
> Make it production-ready

- [ ] **Step 10.1** - Add proper error handling throughout

- [ ] **Step 10.2** - Make frontend responsive for mobile

- [ ] **Step 10.3** - Add loading skeletons

- [ ] **Step 10.4** - Write README.md with setup instructions

- [ ] **Step 10.5** - Deploy backend to Railway (https://railway.app)
  ```bash
  # Railway auto-detects Python apps
  ```

- [ ] **Step 10.6** - Deploy frontend to Vercel
  ```bash
  cd frontend
  npm run build
  npx vercel
  ```

- [ ] **Step 10.7** - Update CORS and environment variables for production

- [ ] **Step 10.8** - Test full production flow

---

## Bonus Features (After MVP)
> Nice-to-haves for later

- [ ] Caching for similar prompts (Redis)
- [ ] Rate limiting on API calls
- [ ] Docker Compose for local development
- [ ] Share recommendations with friends
- [ ] Dark mode toggle
- [ ] Game details page
- [ ] User profile page

---

## File Structure Reference

```
dwisp/
├── docs/
│   ├── claude-notes.md
│   ├── tech-stack.md
│   └── roadmap.md
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── game.py
│   │   │   ├── recommendation.py
│   │   │   └── saved_game.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── game.py
│   │   │   └── prompt.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── prompt.py
│   │   │   ├── games.py
│   │   │   └── saved_games.py
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── openai_service.py
│   │       └── rawg_service.py
│   ├── alembic/
│   ├── alembic.ini
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.tsx
│   │   │   ├── GameCard.tsx
│   │   │   ├── PromptInput.tsx
│   │   │   └── LoadingSpinner.tsx
│   │   ├── pages/
│   │   │   ├── Home.tsx
│   │   │   ├── Login.tsx
│   │   │   ├── Signup.tsx
│   │   │   └── SavedGames.tsx
│   │   ├── services/
│   │   │   └── api.ts
│   │   ├── context/
│   │   │   └── AuthContext.tsx
│   │   ├── types/
│   │   │   └── index.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── .env
├── .gitignore
└── README.md
```

---

## Commands Cheat Sheet

```bash
# Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload        # Run dev server
alembic revision --autogenerate -m "msg"  # Create migration
alembic upgrade head                  # Apply migrations

# Frontend
cd frontend
npm run dev                          # Run dev server
npm run build                        # Build for production
```

---

*10 Phases | Take it one step at a time!*
