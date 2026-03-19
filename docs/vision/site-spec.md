# DWISP Site Specification

> This document defines how the site should behave for every user state,
> on every page. Reference this before building any new feature or fixing
> any existing behavior.

---

## User States

DWISP has two user states. Every page decision flows from this.

| | Guest | Logged-In |
|---|---|---|
| Who are they? | Anyone who visits without an account | Authenticated via Neon Auth |
| Search limit | 1 free search (tracked in `localStorage`) | 20 searches/day (tracked in `rate_limits` table) |
| Can save games? | No — blocked, shown signup prompt | Yes — saves to `saved_games` table |
| Has search history? | No — results are gone on refresh | Yes — stored in `recommendations` table |
| Can view Saved Games? | No — redirected or shown message | Yes |
| Can view My Games? | No — redirected or shown message | Yes |
| Can view Settings? | No — redirected or shown message | Yes |

---

## Known Bug to Fix (Auth State Refresh)

After a user logs in, the Navbar still shows LOGIN / SIGN UP and the guest
lock from `localStorage` is still active. Two things need to happen on login:

1. `useAuth` must re-check auth state (currently only runs once on mount)
2. `localStorage.guestRequestUsed` must be cleared when a user authenticates

Until this is fixed, logging in does nothing visually and guests who
already searched cannot search after creating an account.

---

## Navbar

The Navbar is the same component on every page.

### Guest State
```
🎮 DWISP                          LOGIN   SIGN UP
```

### Logged-In State
```
🎮 DWISP          HELLO, user@email.com   MY GAMES   SAVED   SETTINGS
```

**Notes:**
- Email is truncated if too long (e.g. `user@emai...` at a certain width)
- MY GAMES, SAVED, and SETTINGS are nav links
- Clicking the email or "HELLO" text does nothing (it's a greeting, not a link)
- No logout button in Navbar — logout lives in Settings

---

## Pages

---

### Home (`/`)

The main page. Available to everyone.

**Purpose:** User describes what they want to play, gets 3 game recommendations.

#### Guest — First Visit
- Textarea + search button visible
- No banner, no block
- User types prompt, hits search
- Results appear (3 GameCards)
- Below results: signup banner appears
  - "WANT UNLIMITED SEARCHES AND TO SAVE GAMES? CREATE A FREE ACCOUNT."
  - CTA button: `▶ CREATE ACCOUNT` → `/auth/sign-up`
- Save button on GameCards → shows signup banner (does not save)
- `localStorage.guestRequestUsed` is set to `'true'`

#### Guest — Returning (Already Used Free Search)
- Textarea + search button visible
- User hits search
- Immediately blocked — signup banner appears in place of results
  - "YOU HAVE USED YOUR FREE SEARCH."
  - "CREATE A FREE ACCOUNT TO KEEP PLAYING."
  - CTA button: `▶ CREATE ACCOUNT` → `/auth/sign-up`
- No API call is made

#### Logged-In
- Textarea + search button visible
- User types prompt, hits search
- Results appear (3 GameCards)
- Save button on GameCards is active — saves to `saved_games` table
- If daily limit (20) is hit → error: "DAILY LIMIT REACHED. COME BACK TOMORROW."
- No signup banner ever shown to logged-in users

---

### Sign In (`/auth/sign-in`) / Sign Up (`/auth/sign-up`)

Handled by Neon Auth's `AuthView` component.

**Purpose:** Let users create an account or log in.

#### On Successful Login/Signup:
- Auth state updates throughout the app (Navbar re-renders)
- `localStorage.guestRequestUsed` is cleared
- User is redirected to Home (`/`)

#### Already Logged In:
- Redirect to Home — no reason to show auth pages to a logged-in user

---

### My Games (`/my-games`) — NEW

Logged-in users only. Guests see a "YOU MUST BE LOGGED IN" message with a login CTA.

**Purpose:** Show the user's full search history — every prompt they've made
and the 3 games that came back from it.

#### Layout
A table or stacked list. Each row/entry is one search session.

```
┌─────────────────────────────────────────────────────────────┐
│  PROMPT: "I want a relaxing open world game like Zelda"     │
│  March 15, 2026                                             │
│                                                             │
│  [Game Card 1]  [Game Card 2]  [Game Card 3]                │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│  PROMPT: "A co-op shooter that isn't too hardcore"          │
│  March 16, 2026                                             │
│                                                             │
│  [Game Card 1]  [Game Card 2]  [Game Card 3]                │
└─────────────────────────────────────────────────────────────┘
```

- Sorted newest first
- GameCards in history are display-only (no save button — they can save
  from Home, this is just history)
- If no history yet: "NO SEARCHES YET. GO FIND SOME GAMES." with CTA to Home
- Paginated or scrollable if many entries exist

#### Data Source
- `GET /my-games` (new backend endpoint)
- Reads from `recommendations` joined with `recommendation_games` joined with `games`
- Returns list of: `{ prompt, created_at, games: [GameResult x3] }`

#### ⚠️ Backend Requirement
Right now the `recommendations` and `recommendation_games` tables are never
written to. For My Games to work, the `/games/recommend` endpoint must save
the recommendation to the DB **when the user is logged in**. Guests are not
saved. This is the one backend addition required.

---

### Saved Games (`/saved`)

Logged-in users only. Guests see a "YOU MUST BE LOGGED IN" message with a login CTA.

**Purpose:** Show all games the user has manually saved. No changes to existing behavior.

#### Layout
Grid of saved game cards. Each card has:
- Cover image
- Title
- Metacritic score
- `✕ REMOVE` button → deletes from `saved_games` table

If empty: "NO SAVED GAMES YET." with CTA to Home.

**No changes needed here** — this page already works correctly.

---

### Settings (`/settings`) — NEW

Logged-in users only. Guests see a "YOU MUST BE LOGGED IN" message with a login CTA.

**Purpose:** Simple account management.

#### What's on this page

**Account Info**
- Email address (display only, cannot be changed — managed by Neon Auth)

**Danger Zone**
- `DELETE ACCOUNT` button
  - Shows a confirmation: "ARE YOU SURE? THIS CANNOT BE UNDONE."
  - Two buttons: `✕ CANCEL` and `▶ DELETE`
  - On confirm: deletes all user data from DB (saved_games, recommendations,
    recommendation_games, rate_limits, user_violations) then calls Neon Auth
    to delete the auth account, then redirects to Home as guest
  - On cancel: dismisses the confirmation, no action taken

**That's it.** Keep it simple for now. Preferences and other settings
are a future bonus feature.

---

## Data Storage Summary (What Goes to DB and When)

| Action | Guest | Logged-In |
|---|---|---|
| Makes a search | Nothing stored | `recommendations` + `recommendation_games` rows created |
| Gets game results | Nothing stored | `games` table upserted (cache) |
| Saves a game | Blocked | `saved_games` row created |
| Removes a saved game | N/A | `saved_games` row deleted |
| Hits daily limit | N/A | `rate_limits` row incremented |
| Deletes account | N/A | All user rows deleted across all tables |

---

## Navigation Map

```
/                   → Home (everyone)
/auth/sign-in       → Sign In (guests only, redirect logged-in to /)
/auth/sign-up       → Sign Up (guests only, redirect logged-in to /)
/my-games           → My Games (logged-in only)
/saved              → Saved Games (logged-in only)
/settings           → Settings (logged-in only)
```

---

## What's Not Changing

- GameCard component — no changes
- LoadingSpinner — no changes
- Saved Games page behavior — no changes
- Backend routes: `/prompt/parse`, `/games/recommend`, `/saved-games`, `/profile`
  - Exception: `/games/recommend` needs to save to recommendations table for logged-in users
- Tailwind NES theme — no changes
- Auth provider setup in `main.tsx` — no changes

---

## Open Questions / Future Decisions

- Should My Games GameCards have a save button? (Current answer: no, display only)
- Should search history be paginated? (Decide when we see how it looks with 10+ entries)
- Should delete account be reversible with a 30-day grace period? (Current answer: no)
- Should we show the user's email in full or truncate in the Navbar?
