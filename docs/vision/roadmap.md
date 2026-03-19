# DWISP Development Roadmap

## Phase 1: Project Setup
> Get the foundation in place

- [x] **Step 1.1** - Create folder structure
- [x] **Step 1.2** - Initialize Git repository
- [x] **Step 1.3** - Set up Python virtual environment
- [x] **Step 1.4** - Create `backend/requirements.txt`
- [x] **Step 1.5** - Install Python dependencies
- [x] **Step 1.6** - Initialize React frontend (Vite + React + TypeScript)
- [x] **Step 1.7** - Create `.env` files

---

## Phase 2: Backend Foundation
> Set up FastAPI and basic structure

- [x] **Step 2.1** - Create backend folder structure
- [x] **Step 2.2** - Create `app/main.py` with FastAPI + CORS middleware
- [x] **Step 2.3** - Confirm backend runs with `/health_check` endpoint

---

## Phase 3: Database Setup
> Set up PostgreSQL and define schema

- [x] **Step 3.1** - Sign up for Neon — get `DATABASE_URL`
- [x] **Step 3.2** - Create `app/database.py` with SQLAlchemy setup
- [x] **Step 3.3** - Initialize Alembic
- [x] **Step 3.4** - Create SQLAlchemy models in `app/models/`
  - `game.py` — Game, GameStore, GameGenre, GameTag
  - `recommendation.py` — Recommendation, RecommendationGame
  - `saved_game.py` — SavedGame
  - `user.py` — UserViolation, RateLimit, UserPreferences
- [x] **Step 3.5** - Create and apply initial migration (all 10 tables)

---

## Phase 4: Authentication (Neon Auth)
> Let users sign up and log in

- [x] **Step 4.1** - Get Neon Auth credentials (JWKS URL)
- [x] **Step 4.2** - Install Neon Auth SDK in frontend (`@neondatabase/neon-js`)
- [x] **Step 4.3** - Create `app/services/auth.py` — JWT verification via Neon JWKS
- [x] **Step 4.4** - Create `get_current_user` dependency for protected routes
- [x] **Step 4.5** - Create `app/schemas/user.py` — UserResponse schema
- [x] **Step 4.6** - Set up frontend auth — `NeonAuthUIProvider`, `Auth.tsx`, `lib/auth.ts`
- [x] **Step 4.7** - Test auth flow end-to-end

---

## Phase 5: OpenAI Integration
> Turn user prompts into game filters

- [x] **Step 5.1** - Get OpenAI API key
- [x] **Step 5.2** - Create `app/services/openai_service.py`
  - Modern `OpenAI` client (gpt-4o-mini)
  - `response_format={"type": "json_object"}` for guaranteed valid JSON
- [x] **Step 5.3** - Design JSON schema for game filters
  ```json
  {
    "genres": ["rpg", "action"],
    "tags": ["story-rich", "open-world"],
    "mood": "relaxing",
    "multiplayer": false,
    "platforms": ["pc"],
    "search_query": "open world rpg"
  }
  ```
- [x] **Step 5.4** - Write detailed system prompt with RAWG genre/tag constraints
- [x] **Step 5.5** - Create `app/routers/prompt.py` — `POST /prompt/parse`
  - Optional rate limiting for logged-in users (20 requests/day via RateLimit table)
- [x] **Step 5.6** - Add Pydantic validation with `GameFilters` schema
- [x] **Step 5.7** - Test with various user inputs

---

## Phase 6: Gaming API Integration
> Fetch real game recommendations

- [x] **Step 6.1** - Sign up for RAWG API — get `RAWG_API_KEY`
- [x] **Step 6.2** - Create `app/services/rawg_service.py`
- [x] **Step 6.3** - Map JSON filters to RAWG query parameters
  - `search_query` → RAWG `search` param (most impactful for relevance)
  - `genres`, `tags`, `platforms` → RAWG filters
  - `VALID_TAGS` set to prevent invalid tag filtering
  - `PLATFORM_MAP` dict to convert platform names to RAWG IDs
- [x] **Step 6.4** - Create `app/routers/games.py` — `POST /games/recommend`
- [x] **Step 6.5** - Results limited to 3 games, ordered by rating

---

## Phase 7: Frontend Foundation
> Build the React app structure

- [x] **Step 7.1** - Set up folder structure (`pages/`, `components/`, `services/`, `hooks/`, `types/`)
- [x] **Step 7.2** - Configure Tailwind CSS v4 with NES color theme
  - Colors: `nes-gold`, `nes-red`, `nes-blue`, `nes-green`, `nes-black`, `nes-dark`, `nes-white`, `nes-gray`
  - Font: Press Start 2P (pixel font via Google Fonts)
- [x] **Step 7.3** - Set up React Router — `/`, `/auth/sign-in`, `/auth/sign-up`, `/saved`, `/profile`
- [x] **Step 7.4** - Create `services/api.ts` — axios instance pointing at `VITE_API_URL`
- [x] **Step 7.5** - Auth state handled by `NeonAuthUIProvider` + `useAuth` hook

---

## Phase 8: Frontend UI
> Build the main user interface

- [x] **Step 8.1** - Create `Navbar` — auth-aware (Profile/Saved when logged in, Login when not)
- [x] **Step 8.2** - Auth pages handled by Neon Auth (`Auth.tsx`)
- [x] **Step 8.3** - Create `Home` page with prompt textarea + search button
- [x] **Step 8.4** - Create `GameCard` — cover image, title, rating, metacritic, release date, save button
- [x] **Step 8.5** - Create results grid (3 GameCards)
- [x] **Step 8.6** - Create `LoadingSpinner` component
- [x] **Step 8.7** - Add error messages and states

---

## Phase 9: Save Features + Profile
> Let users save games and view their profile

- [x] **Step 9.1** - Create `app/routers/saved_games.py`
  - `POST /saved-games` — save a game (upserts into games table)
  - `GET /saved-games` — get user's saved games
  - `DELETE /saved-games/{rawg_id}` — remove saved game
- [x] **Step 9.2** - Add `+ SAVE` / `✓ SAVED` button to GameCard
- [x] **Step 9.3** - Create `SavedGames` page — displays saved games with `✕ REMOVE`
- [x] **Step 9.4** - Create `app/routers/profile.py` — `GET /profile`
  - Returns email, saved games count, total searches, daily usage
- [x] **Step 9.5** - Create `Profile` page — account info, stats, daily usage bar, quick links
- [ ] **Step 9.6** - Recommendation history on profile (show past prompts + results)

---

## Phase 10: Guest Limiting + Rate Limiting
> Control access and prevent abuse

- [x] **Step 10.1** - Guest limit: 1 free search via `localStorage`
  - After first search, show signup banner prompting account creation
  - Second search attempt blocked with signup prompt
- [x] **Step 10.2** - Logged-in rate limiting: 20 searches/day via `RateLimit` table
  - `app/services/rate_limit.py` — `check_and_increment()`
  - Returns 429 when daily limit exceeded
- [ ] **Step 10.3** - Show remaining daily searches in Navbar for logged-in users

---

## Phase 11: Auth Fix + Settings + My Games
> Fix login state reactivity and build new pages

- [ ] **Step 11.1** - Fix `useAuth.ts` — replace one-time `getToken()` with reactive `useAuthenticate()` hook
- [ ] **Step 11.2** - Clear `localStorage.guestRequestUsed` on login transition
- [ ] **Step 11.3** - Update `Navbar.tsx` — show `HELLO, email` + MY GAMES + SETTINGS when logged in
- [ ] **Step 11.4** - Redirect to `/` after sign-in/sign-up in `Auth.tsx`
- [ ] **Step 11.5** - Create `backend/app/routers/account.py` — `DELETE /account` endpoint
- [ ] **Step 11.6** - Register account router in `main.py`
- [ ] **Step 11.7** - Create `src/pages/Settings.tsx` — email display + delete account with confirmation
- [ ] **Step 11.8** - Add `/settings` route to `App.tsx`

---

## Phase 12: Polish & Deploy
> Make it production-ready

- [ ] **Step 11.1** - Add proper error handling throughout
- [ ] **Step 11.2** - Make frontend responsive for mobile
- [ ] **Step 11.3** - Add loading skeletons
- [ ] **Step 11.4** - Write README.md with setup instructions
- [ ] **Step 11.5** - Deploy backend to Railway
- [ ] **Step 11.6** - Deploy frontend to Vercel
- [ ] **Step 11.7** - Update CORS and environment variables for production
- [ ] **Step 11.8** - Test full production flow

---

## Bonus Features (After MVP)
> Nice-to-haves for later

- [ ] Recommendation history page (past prompts + results)
- [ ] User preferences page (excluded tags, preferred platforms, min metacritic)
- [ ] Caching for similar prompts (Redis)
- [ ] Docker Compose for local development
- [ ] Share recommendations with friends
- [ ] Game details page

---

*11 Phases | Take it one step at a time!*
