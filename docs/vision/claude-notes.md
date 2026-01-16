# Claude's Thoughts - DWISP Project

## Project Overview
**DWISP** - Dude What Should I Play?

A full-stack web application that uses AI to recommend games based on user prompts.

---

## Application Flow

```
User Prompt → OpenAI → JSON filters → Gaming API (RAWG/IGDB) → Results
                                                                  ↓
                                         Your DB ← User saves/likes games
```

1. User enters a prompt describing what they feel like playing
2. OpenAI processes the prompt and returns a JSON with game filters/preferences
3. JSON is used to query a gaming database API (RAWG or IGDB)
4. Results are displayed to the user
5. User can save/like games from the recommendations
6. User data, recommendations, and likes are stored in the database

---

## Key Considerations

### Gaming API Choice
- **RAWG** - Has a free tier, simpler to set up
- **IGDB** - Requires Twitch authentication, more complex

### OpenAI Error Handling
- Build validation for malformed JSON responses
- Consider a fallback mechanism

### Caching Strategy
- Cache similar prompts to save on OpenAI API costs
- Consider Redis or in-memory caching for frequently requested data

### Authentication
- Use NextAuth.js or Clerk - don't roll your own auth
- Battle-tested solutions are better for portfolio projects

---

## Database Schema (Initial Design)

```sql
users
├── id (primary key)
├── email
├── password_hash
└── created_at

recommendations
├── id (primary key)
├── user_id (foreign key → users)
├── prompt
└── created_at

games
├── id (primary key)
├── external_api_id
├── title
└── metadata (JSON)

user_saved_games
├── user_id (foreign key → users)
├── game_id (foreign key → games)
├── liked (boolean)
└── created_at
```

---

## What Makes This "Professional"

- Clean error handling
- Environment variable management (never hardcode API keys)
- Proper README with setup instructions
- Input validation and sanitization
- Consistent code style
- Git commit history that tells a story

---

## Questions to Answer Later

1. What specific fields should the OpenAI JSON response contain?
2. Which gaming API will you use? (RAWG recommended for simplicity)
3. Do you want social features (share recommendations, follow friends)?
4. Mobile-responsive or desktop-first?

---

*Last updated: January 2026*
