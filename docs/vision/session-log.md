# DWISP Session Log

> Quick reference for what has been built, what was fixed, and what still needs doing.
> Update this after each work session.

---

## Last Session — 2026-03-19 (continued, second half)

### What We Did

#### Attempted (caused new bug — currently broken)
- **Logout button** — added `LOGOUT` button to Navbar calling `authClient.signOut()`. Removed
  while debugging the loop below. Needs to be re-added once loop is resolved.
- **Auto-logout timer** — attempted to add `setTimeout` in `useAuth.ts` to call `signOut()`
  when JWT `exp` expires. Multiple iterations written, all reverted due to triggering the loop.

#### New Bug Introduced — App Infinite Render Loop
The app now refreshes/loops on every page, including in incognito on fresh browsers.
Confirmed this is **not** browser state — it reproduces on Chrome, Edge, and incognito.

**Root cause (best theory):** `useAuth.ts` stores a `token` state and calls `getToken()` inside
a `useEffect`. Now that `getToken()` actually returns a real JWT (it was broken/returning null
before the save-game fix), each call may return a slightly different token string (new `iat`
claim). `setToken(newJWT)` sees a new value → triggers re-render → effect fires → `getToken()`
again → new token string → loop.

**What was tried:**
1. Changed `[user, isPending]` deps to `[isLoggedIn, isPending]` (boolean) — still looped
2. Fully reverted `useAuth.ts` to original — still looped
3. Reverted `Navbar.tsx` — still looped
4. Cleared browser site data — still looped
5. Deleted Vite cache (`node_modules/.vite`) — still looped
6. Tried incognito + different browser — still looped

**Current state of `useAuth.ts`:** Removed `token` state and `getToken()` call entirely.
No more `setToken()` in the render cycle. This is the right direction but the loop persists,
suggesting there may be another source of rapid re-renders (possibly `useAuthenticate()`
returning a new `user` object reference every render, or the Neon Auth SDK itself).

#### Files Changed This Half
| File | Change |
|---|---|
| `frontend/src/hooks/useAuth.ts` | Removed `token` state + `getToken()` call entirely, no longer exports `token` |
| `frontend/src/pages/Settings.tsx` | Removed `token` from useAuth destructure, `token ?? await getToken()` → `await getToken()` |
| `frontend/src/components/Navbar.tsx` | Logout button added then removed (pending loop fix) |

---

### What Needs to Happen Next Session

#### Priority 1 — Fix the loop
- Open browser DevTools → **Network tab** while the app loops. Identify which request
  is repeating. This will pinpoint whether the loop is a React re-render loop or an actual
  HTTP redirect loop.
- Check browser console for any rapid error messages.
- Look at whether `useAuthenticate()` from `@neondatabase/neon-js/auth/react` is the source —
  it might return a new `user` object reference on every render if not memoized internally.
- Consider wrapping `isLoggedIn` in `useMemo` or comparing `user?.email` instead of `user`
  in the dependency array.
- If the loop is from `AuthView` (the Neon Auth sign-in UI component), consider whether the
  `emailOTP` prop on `NeonAuthUIProvider` is causing unexpected redirect behavior.

#### Priority 2 — Add logout button back (after loop fixed)
- Use `authClient.signOut()` from `lib/auth.ts` in Navbar
- BetterAuth's `signOut()` does `window.location.href = callbackURL ?? "/"` — consider
  passing `callbackURL: '/'` explicitly to control where it lands

#### Priority 3 — Auto-logout timer (after logout button works)
- Decode JWT `exp` claim from `getToken()` result
- `setTimeout` → `authClient.signOut()` when token expires
- Do NOT store the JWT in React state — call `getToken()` once just to read the expiry,
  then discard the result

---

## Last Session — 2026-03-19

### What We Did

#### Bug Fixes
- **Save Game returning 401 (stale token)** — `Home.tsx` was using `token ?? await getToken()`
  where `token` came from `useAuth` state (set once on mount, never refreshed). When that cached
  token expired, the `??` prevented a fresh call to `getToken()`. Fixed by removing `token ??`
  and always calling `await getToken()` directly. Also removed the now-unused `token` destructure
  from `useAuth` in `Home.tsx`.
- **Save Game returning 401 (wrong algorithm)** — Neon Auth signs JWTs with **EdDSA (Ed25519)**,
  but the backend was calling `jwt.decode(..., algorithms=["RS256"])`. `python-jose` doesn't
  support EdDSA at all (raises `JWKError: Unable to find an algorithm for key`).
  Fixed by replacing `python-jose` with `PyJWT[crypto]` and rewriting `auth.py` to:
  1. Parse the JWT header to extract `kid`
  2. Look up the matching key in the JWKS by `kid`
  3. Construct an `Ed25519PublicKey` from the key's `x` field (base64url-decoded)
  4. Decode the token with `pyjwt.decode(..., algorithms=["EdDSA"])`

#### Files Changed
| File | Change |
|---|---|
| `frontend/src/pages/Home.tsx` | `token ?? await getToken()` → `await getToken()`, removed `token` from useAuth destructure |
| `backend/app/services/auth.py` | Replaced python-jose with PyJWT, rewrote verify_token for EdDSA/JWKS |
| `backend/requirements.txt` | `python-jose[cryptography]` → `PyJWT[crypto]` |

---

## What Still Needs Building

### Next Up
- [ ] **Auto-logout timer** — decode JWT `exp` claim, `setTimeout` to call `authClient.signOut()`
  when token expires (discussed but not built yet)
- [ ] **My Games page** (`/my-games`) — search history table showing each prompt + its 3 games
  - Backend: update `POST /games/recommend` to write to `recommendations` + `recommendation_games` when logged in
  - Backend: new `GET /my-games` endpoint
  - Frontend: `src/pages/MyGames.tsx`
  - Navbar: add MY GAMES link

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
- **Neon Auth uses EdDSA (Ed25519), not RS256.** `python-jose` does not support EdDSA.
  The backend uses `PyJWT[crypto]` + `cryptography` to verify tokens. Never switch back to
  `python-jose` for JWT verification in this project.
- Always call `await getToken()` fresh when making authenticated API calls — never cache
  the token in React state and reuse it. Cached tokens go stale and cause 401s.
- Delete account removes all DB rows but does NOT call Neon Auth to delete the auth account
  itself (the user record in Neon's system). They could technically sign back in with the
  same email and start fresh. Decide later if this matters.
- The `Profile` page (`/profile`) still exists but is no longer linked from the Navbar.
  It's reachable by direct URL. Decide if it should be kept, removed, or merged into Settings.
