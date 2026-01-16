# DWISP Database Schema

## Overview

This document describes the relational database design for DWISP.
Use this as reference when creating your draw.io diagram.

**Note:** Users are managed by Neon Auth - we only store their `neon_user_id` (string) to link data.

---

## Tables

### 1. games
Cached game data from RAWG API. We store this so we don't call RAWG repeatedly for the same game.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Internal ID |
| rawg_id | INTEGER | UNIQUE, NOT NULL | RAWG's game ID |
| name | VARCHAR(255) | NOT NULL | Game title |
| description | TEXT | | Game description |
| metacritic_score | INTEGER | | Metacritic rating (0-100) |
| background_image | VARCHAR(500) | | URL to cover image |
| released | DATE | | Release date |
| trailer_url | VARCHAR(500) | | YouTube/video URL from RAWG |
| created_at | TIMESTAMP | DEFAULT NOW() | When we cached this |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last cache update |

---

### 2. game_stores
Store links for each game (one game can be on multiple stores).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Internal ID |
| game_id | INTEGER | FOREIGN KEY (games.id) | Reference to game |
| store_name | VARCHAR(100) | NOT NULL | "Steam", "PlayStation Store", etc. |
| store_url | VARCHAR(500) | NOT NULL | Direct link to buy |

**Relationship:** games (1) → game_stores (many)

---

### 3. game_genres
Genres for each game (many-to-many via junction).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Internal ID |
| game_id | INTEGER | FOREIGN KEY (games.id) | Reference to game |
| genre_name | VARCHAR(100) | NOT NULL | "RPG", "Action", etc. |

**Relationship:** games (1) → game_genres (many)

---

### 4. game_tags
Tags/keywords for each game.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Internal ID |
| game_id | INTEGER | FOREIGN KEY (games.id) | Reference to game |
| tag_name | VARCHAR(100) | NOT NULL | "Open World", "Story Rich", etc. |

**Relationship:** games (1) → game_tags (many)

---

### 5. recommendations
Each time a user submits a prompt and gets results.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Internal ID |
| neon_user_id | VARCHAR(255) | NOT NULL | User ID from Neon Auth |
| user_prompt | TEXT | NOT NULL | Original user prompt |
| parsed_keywords | JSONB | | OpenAI extracted keywords |
| openai_game_predict | JSONB | | Games OpenAI predicted |
| filters_used | JSONB | | Snapshot of filters applied |
| was_valid | BOOLEAN | DEFAULT TRUE | TEST field from OpenAI |
| was_jailed | BOOLEAN | DEFAULT FALSE | JAIL field from OpenAI |
| created_at | TIMESTAMP | DEFAULT NOW() | When recommendation was made |

---

### 6. recommendation_games
Junction table linking recommendations to the games returned.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Internal ID |
| recommendation_id | INTEGER | FOREIGN KEY (recommendations.id) | Reference to recommendation |
| game_id | INTEGER | FOREIGN KEY (games.id) | Reference to game |
| position | INTEGER | | Order shown (1, 2, or 3) |

**Relationship:** recommendations (1) → recommendation_games (many) → games (many)

---

### 7. saved_games
Games a user has saved/liked.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Internal ID |
| neon_user_id | VARCHAR(255) | NOT NULL | User ID from Neon Auth |
| game_id | INTEGER | FOREIGN KEY (games.id) | Reference to game |
| saved_at | TIMESTAMP | DEFAULT NOW() | When user saved it |

**Constraint:** UNIQUE(neon_user_id, game_id) - user can't save same game twice

**Relationship:** saved_games (many) → games (1)

---

### 8. user_violations
Tracks jail counts and bans per user.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Internal ID |
| neon_user_id | VARCHAR(255) | UNIQUE, NOT NULL | User ID from Neon Auth |
| jail_count | INTEGER | DEFAULT 0 | Number of times jailed |
| banned_at | TIMESTAMP | NULL | When ban started (NULL if not banned) |
| banned_until | TIMESTAMP | NULL | When ban expires (NULL if not banned) |
| last_violation_at | TIMESTAMP | | Most recent violation |

**Logic:**
- When `was_jailed = TRUE` in recommendations → increment `jail_count`
- When `jail_count >= 5` → set `banned_at = NOW()`, `banned_until = NOW() + 1 month`
- On login/request: if `banned_until > NOW()` → reject request
- Cleanup job (optional): DELETE WHERE `banned_until < NOW()` to wipe expired bans

---

### 9. rate_limits
Prevents API abuse (optional but recommended).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Internal ID |
| neon_user_id | VARCHAR(255) | NOT NULL | User ID from Neon Auth |
| request_date | DATE | NOT NULL | Date of requests |
| request_count | INTEGER | DEFAULT 0 | Number of requests that day |

**Constraint:** UNIQUE(neon_user_id, request_date)

**Logic:**
- On each request: UPSERT increment `request_count`
- If `request_count > 50` (or your limit) → reject request
- Old rows auto-cleanup or just ignore (date won't match)

---

### 10. user_preferences
Stores user's default search filters. Applied automatically to every search.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Internal ID |
| neon_user_id | VARCHAR(255) | UNIQUE, NOT NULL | User ID from Neon Auth |
| platforms | JSONB | DEFAULT '[]' | Preferred platforms |
| excluded_tags | JSONB | DEFAULT '[]' | Tags to always exclude |
| excluded_genres | JSONB | DEFAULT '[]' | Genres to always exclude |
| min_metacritic | INTEGER | DEFAULT NULL | Minimum metacritic score |
| max_metacritic | INTEGER | DEFAULT NULL | Maximum metacritic score |
| release_year_min | INTEGER | DEFAULT NULL | Oldest release year |
| release_year_max | INTEGER | DEFAULT NULL | Newest release year |
| multiplayer_pref | VARCHAR(20) | DEFAULT 'any' | 'singleplayer', 'multiplayer', 'any' |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last preference update |

**Example data:**
```json
{
  "platforms": ["pc", "playstation5"],
  "excluded_tags": ["horror", "gore", "difficult"],
  "excluded_genres": ["sports", "racing"],
  "min_metacritic": 70,
  "max_metacritic": null,
  "release_year_min": 2015,
  "release_year_max": null,
  "multiplayer_pref": "singleplayer"
}
```

---

## RAWG Platform IDs (Reference)

Use these when storing/querying platforms:

| Platform | RAWG ID | Slug |
|----------|---------|------|
| PC | 4 | pc |
| PlayStation 5 | 187 | playstation5 |
| PlayStation 4 | 18 | playstation4 |
| Xbox Series X/S | 186 | xbox-series-x |
| Xbox One | 1 | xbox-one |
| Nintendo Switch | 7 | nintendo-switch |
| iOS | 3 | ios |
| Android | 21 | android |
| macOS | 5 | macos |
| Linux | 6 | linux |

---

## RAWG Common Tags to Exclude (Starter List)

Offer these as quick toggles in the UI:

| Tag Slug | Display Name | Why exclude? |
|----------|--------------|--------------|
| horror | Horror | Too scary |
| gore | Gore | Too violent |
| difficult | Difficult | Too hard |
| sexual-content | Sexual Content | Inappropriate |
| nudity | Nudity | Inappropriate |
| pvp | PvP | Competitive stress |
| pay-to-win | Pay to Win | Unfair monetization |
| early-access | Early Access | Unfinished games |
| grinding | Grinding | Time sink |
| permadeath | Permadeath | Too punishing |

---

## Entity Relationship Diagram (for draw.io)

```
┌─────────────────┐
│     games       │
├─────────────────┤
│ id (PK)         │
│ rawg_id (UQ)    │
│ name            │
│ description     │
│ metacritic_score│
│ background_image│
│ released        │
│ trailer_url     │
│ created_at      │
│ updated_at      │
└────────┬────────┘
         │
         │ 1
         │
    ┌────┴────┬──────────┬──────────────┐
    │         │          │              │
    ▼ M       ▼ M        ▼ M            ▼ M
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌────────────────────┐
│game_    │ │game_    │ │game_    │ │recommendation_games│
│stores   │ │genres   │ │tags     │ ├────────────────────┤
├─────────┤ ├─────────┤ ├─────────┤ │ id (PK)            │
│id (PK)  │ │id (PK)  │ │id (PK)  │ │ recommendation_id  │──┐
│game_id  │ │game_id  │ │game_id  │ │ game_id (FK)       │  │
│store_   │ │genre_   │ │tag_name │ │ position           │  │
│  name   │ │  name   │ └─────────┘ └────────────────────┘  │
│store_url│ └─────────┘                                     │
└─────────┘                                                 │
                                                            │
                          ┌─────────────────────────────────┘
                          │ M
                          ▼
                    ┌─────────────────┐       ┌─────────────────┐
                    │ recommendations │       │ user_violations │
                    ├─────────────────┤       ├─────────────────┤
                    │ id (PK)         │       │ id (PK)         │
                    │ neon_user_id    │──────▶│ neon_user_id(UQ)│
                    │ user_prompt     │       │ jail_count      │
                    │ parsed_keywords │       │ banned_at       │
                    │ openai_game_    │       │ banned_until    │
                    │   predict       │       │ last_violation  │
                    │ filters_used    │       └─────────────────┘
                    │ was_valid       │
                    │ was_jailed      │
                    │ created_at      │
                    └─────────────────┘


┌─────────────────┐         ┌─────────────────┐
│  saved_games    │         │     games       │
├─────────────────┤         │   (see above)   │
│ id (PK)         │    M:1  │                 │
│ neon_user_id    │────────▶│                 │
│ game_id (FK)    │         │                 │
│ saved_at        │         │                 │
└─────────────────┘         └─────────────────┘


┌─────────────────┐         ┌───────────────────┐
│  rate_limits    │         │ user_preferences  │
├─────────────────┤         ├───────────────────┤
│ id (PK)         │         │ id (PK)           │
│ neon_user_id    │         │ neon_user_id (UQ) │
│ request_date    │         │ platforms         │
│ request_count   │         │ excluded_tags     │
└─────────────────┘         │ excluded_genres   │
                            │ min_metacritic    │
                            │ max_metacritic    │
                            │ release_year_min  │
                            │ release_year_max  │
                            │ multiplayer_pref  │
                            │ updated_at        │
                            └───────────────────┘
```

---

## Data Flow (Updated with Filters)

```
User Prompt + Filter Selection (UI)
     │
     │  User can adjust filters per-search OR use saved preferences
     │
     ▼
┌─────────────────────────────────────┐
│         Pre-flight Checks           │
│                                     │
│  1. Check user_violations table     │
│     - If banned_until > NOW()       │
│       → REJECT (show ban message)   │
│                                     │
│  2. Check rate_limits table         │
│     - If request_count > limit      │
│       → REJECT (rate limited)       │
│                                     │
│  3. Load user_preferences           │
│     - Merge with per-search filters │
└─────────────────────────────────────┘
     │
     │ (if passed)
     ▼
┌─────────────┐
│   OpenAI    │ ──▶ Extract: TEST, GAME_CALL, GAME_PREDICT, KEYWORDS, JAIL
└─────────────┘
     │
     ├──▶ If JAIL = True:
     │      - Increment jail_count in user_violations
     │      - If jail_count >= 5: set banned_until = NOW() + 1 month
     │      - Save recommendation with was_jailed = True
     │      - REJECT (show warning)
     │
     │ (if valid and not jailed)
     ▼
┌─────────────────────────────────────┐
│           Build RAWG Query          │
│                                     │
│  Combine:                           │
│  - OpenAI keywords/tags             │
│  - User's platform filter           │
│  - Excluded tags (from prefs)       │
│  - Metacritic range                 │
│  - Release year range               │
│  - Multiplayer preference           │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────┐
│  RAWG API   │ ──▶ Search with combined filters, get 3 games
└─────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│           Database                  │
│                                     │
│  1. Cache games in `games` table    │
│  2. Cache stores in `game_stores`   │
│  3. Cache genres in `game_genres`   │
│  4. Cache tags in `game_tags`       │
│  5. Save recommendation record      │
│     (include filters_used snapshot) │
│  6. Link games via                  │
│     `recommendation_games`          │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│           Frontend                  │
│                                     │
│  Display 3 games with:              │
│  - Title                            │
│  - Trailer (video player)           │
│  - Metacritic score                 │
│  - Store links (buy buttons)        │
│  - Save/Like button                 │
└─────────────────────────────────────┘
```

---

## Frontend Filter UI (Suggestion)

Show these options alongside the prompt input:

```
┌─────────────────────────────────────────────────────────┐
│  What game are you looking for?                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │ I want a relaxing open world game like Zelda...   │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  ▼ Filters (optional)                                   │
│  ┌─────────────────────────────────────────────────────┐│
│  │ Platform:  [x] PC  [ ] PS5  [ ] Xbox  [ ] Switch   ││
│  │                                                     ││
│  │ Min Rating: [70 ▼]    Max Rating: [Any ▼]          ││
│  │                                                     ││
│  │ Release Year: [2015 ▼] to [Any ▼]                  ││
│  │                                                     ││
│  │ Exclude:  [x] Horror  [x] Gore  [ ] Difficult      ││
│  │           [ ] PvP     [ ] Grinding                 ││
│  │                                                     ││
│  │ Multiplayer: ( ) Any  (•) Single  ( ) Multi        ││
│  │                                                     ││
│  │ [ ] Save as my default preferences                 ││
│  └─────────────────────────────────────────────────────┘│
│                                                         │
│                              [Get Recommendations]      │
└─────────────────────────────────────────────────────────┘
```

---

## Security Considerations

### 1. SQL Injection Prevention
- SQLAlchemy uses parameterized queries by default - you're safe if you use it properly
- NEVER concatenate user input into raw SQL strings

### 2. Input Sanitization
- Sanitize user prompts before sending to OpenAI (remove weird unicode, limit length)
- Max prompt length: recommend 500 characters

### 3. Rate Limiting
- The `rate_limits` table handles daily limits
- Also consider per-minute limits in your API middleware (FastAPI has libraries for this)

### 4. Don't Expose Internal IDs
- In API responses, use `rawg_id` instead of your internal `id`
- Or use UUIDs instead of auto-increment IDs

### 5. API Key Security
- Never expose OPENAI_API_KEY or RAWG_API_KEY to frontend
- All API calls to external services happen on backend only

### 6. CORS Configuration
- Only allow your frontend domain, not `*`
- In production: `allow_origins=["https://yourdomain.com"]`

### 7. Neon Auth Token Validation
- Always validate JWT tokens on every protected request
- Check token expiration
- Verify token signature using Neon's JWKS

---

## Indexes (Performance)

Add these indexes for faster queries:

```sql
-- Fast lookup by RAWG ID
CREATE INDEX idx_games_rawg_id ON games(rawg_id);

-- Fast lookup of user's saved games
CREATE INDEX idx_saved_games_user ON saved_games(neon_user_id);

-- Fast lookup of user's recommendations
CREATE INDEX idx_recommendations_user ON recommendations(neon_user_id);

-- Fast ban check
CREATE INDEX idx_violations_user ON user_violations(neon_user_id);

-- Fast rate limit check
CREATE INDEX idx_rate_limits_user_date ON rate_limits(neon_user_id, request_date);

-- Fast preferences lookup
CREATE INDEX idx_preferences_user ON user_preferences(neon_user_id);
```

---

## Cleanup Jobs (Optional)

Run these periodically (daily cron job or scheduled task):

```sql
-- Remove expired bans (users can start fresh)
DELETE FROM user_violations
WHERE banned_until IS NOT NULL
AND banned_until < NOW();

-- Remove old rate limit records (older than 7 days)
DELETE FROM rate_limits
WHERE request_date < CURRENT_DATE - INTERVAL '7 days';

-- Update stale game cache (older than 30 days)
-- You might want to re-fetch from RAWG instead of deleting
UPDATE games
SET updated_at = NOW()
WHERE updated_at < NOW() - INTERVAL '30 days';
```

---

## Table Count Summary

| Table | Purpose |
|-------|---------|
| games | Cached RAWG game data |
| game_stores | Store links per game |
| game_genres | Genres per game |
| game_tags | Tags per game |
| recommendations | User search history |
| recommendation_games | Links recommendations to games |
| saved_games | User's liked/saved games |
| user_violations | Jail counts and bans |
| rate_limits | Daily request limits |
| user_preferences | User's default filters |

**Total: 10 tables**

---

## Why This Design?

1. **games table is cached** - If two users get the same game recommended, we don't call RAWG twice.

2. **Separate tables for stores/genres/tags** - One game has multiple of each. This is normalized (proper relational design).

3. **recommendations tracks history** - You can show users their past searches, analyze what prompts work best, etc.

4. **recommendation_games is a junction table** - Links the many-to-many relationship between recommendations and games.

5. **saved_games is simple** - Just links a user to games they liked.

6. **user_violations is separate** - Easy to query, easy to wipe, doesn't clutter other tables.

7. **rate_limits per day** - Simple, effective, easy to clean up.

8. **user_preferences stores filters** - Users don't have to re-select every time.

9. **No users table** - Neon Auth handles that. We just reference `neon_user_id` wherever needed.

10. **filters_used in recommendations** - Snapshot of what filters were active, useful for debugging/analytics.
