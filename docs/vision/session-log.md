# DWISP Session Log

> Quick reference for what has been built, what was fixed, and what still needs doing.
> Update this after each work session.

---

## Last Session — 2026-03-18

### What We Did

#### Planning
- Created `docs/vision/site-spec.md` — full page-by-page spec for guest vs logged-in behavior,
  every page layout, navbar states, data storage table, and navigation map

#### Bug Fixes
- **Auth state not updating after login** — replaced the one-shot `getToken()` call in
  `useAuth.ts` with the reactive `useAuthenticate()` hook from `@neondatabase/neon-js/auth/react`.
  The Navbar and all pages now update immediately when auth state changes.
- **Guest lock not clearing on login** — `useAuth.ts` now detects the logged-out → logged-in
  transition and calls `localStorage.removeItem('guestRequestUsed')` automatically.
- **`authClient.getToken()` was wrong method** — `createAuthClient` returns only the adapter,
  which does not have `getJWTToken`. Fixed `lib/auth.ts` to use `createInternalNeonAuth` and
  export a standalone `getToken()` function wrapping `neonAuth.getJWTToken()`. This was the
  root cause of Save Game doing nothing — every token-dependent action was silently failing.

#### New Features Built
- **Navbar** — now shows `HELLO, [email]` + SAVED + SETTINGS links when logged in
- **Auth.tsx** — now redirects to `/` if already logged in, and after successful sign-in/sign-up
- **`backend/app/routers/account.py`** — `DELETE /account` endpoint, deletes all user data
  across all tables in correct FK order (recommendation_games → recommendations → saved_games
  → rate_limits → user_violations → user_preferences), returns 204
- **`src/pages/Settings.tsx`** — new page with email display and delete account flow
  (confirmation dialog before deleting)
- **`App.tsx`** — `/settings` route added

#### Files Changed
| File | Change |
|---|---|
| `frontend/src/lib/auth.ts` | Switched to `createInternalNeonAuth`, added `getToken()` export |
| `frontend/src/hooks/useAuth.ts` | Now uses `useAuthenticate()`, clears guest lock on login, exposes `email` |
| `frontend/src/components/Navbar.tsx` | Shows greeting + new nav links when logged in |
| `frontend/src/pages/Auth.tsx` | Added redirect logic on login/already logged in |
| `frontend/src/pages/Home.tsx` | `authClient.getToken()` → `getToken()` |
| `frontend/src/pages/SavedGames.tsx` | `authClient.getToken()` → `getToken()` |
| `frontend/src/pages/Settings.tsx` | New file |
| `frontend/src/App.tsx` | Added `/settings` route |
| `backend/app/routers/account.py` | New file — DELETE /account |
| `backend/app/main.py` | Registered account router |
| `docs/vision/roadmap.md` | Added Phase 11 steps, renamed old Phase 11 → Phase 12 |
| `docs/vision/site-spec.md` | New file — full site specification |

---

## What Still Needs Testing

These were just written — run the app and verify:

- [ ] Log in → Navbar immediately shows `HELLO, email` without refresh
- [ ] Guest searches → logs in → guest lock clears → can search again
- [ ] Save Game button works (was broken due to wrong token method — now fixed)
- [ ] `/settings` page loads for logged-in users, shows email
- [ ] Delete account confirmation dialog appears before any action
- [ ] Delete account actually removes DB rows and redirects to home as guest
- [ ] `/settings` shows "YOU MUST BE LOGGED IN" for guests

---

## What Still Needs Building

### Immediate (Phase 11 — mostly done, one thing left)
- [ ] **Verify** all Phase 11 steps above actually work end-to-end

### Next Up
- [ ] **My Games page** (`/my-games`) — search history table showing each prompt + its 3 games
  - Requires one backend change: `POST /games/recommend` must save to `recommendations` +
    `recommendation_games` tables when user is logged in (currently never written to)
  - Requires new backend endpoint: `GET /my-games`
  - Requires new frontend page: `src/pages/MyGames.tsx`
  - Add MY GAMES link to Navbar (currently only SAVED + SETTINGS)

### Later (Phase 12 — Polish & Deploy)
- [ ] Proper error handling throughout
- [ ] Mobile responsive layout
- [ ] Loading skeletons
- [ ] README.md with setup instructions
- [ ] Deploy backend to Railway
- [ ] Deploy frontend to Vercel
- [ ] Update CORS + env vars for production
- [ ] End-to-end production test

### Roadmap Loose Ends
- [ ] Step 9.6 — Recommendation history on profile (blocked by My Games work above)
- [ ] Step 10.3 — Show remaining daily searches in Navbar

---

## Known Quirks / Watch Out For

- `@neondatabase/neon-js` is `^0.2.0-beta.1` — beta package, API could change on update
- `authClient` (the adapter) ≠ the full neon auth object. Always use `getToken()` from
  `lib/auth.ts` for JWT tokens, never `authClient.getToken()` (that method doesn't exist)
- `useAuthenticate()` gets its client from `NeonAuthUIProvider` context — it must stay
  wrapping the entire app in `main.tsx`
- Delete account removes all DB rows but does NOT call Neon Auth to delete the auth account
  itself (the user record in Neon's system). They could technically sign back in with the
  same email and start fresh. Decide later if this matters.
- The `Profile` page (`/profile`) still exists but is no longer linked from the Navbar.
  It's reachable by direct URL. Decide if it should be kept, removed, or merged into Settings.
