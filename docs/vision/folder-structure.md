# DWISP Folder Structure Reference

## Complete Project Structure

```
dwsip/
├── docs/
│   ├── claude-notes.md
│   ├── tech-stack.md
│   ├── roadmap.md
│   └── folder-structure.md
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI app entry
│   │   ├── config.py         # Environment variables
│   │   ├── database.py       # Database connection
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── routers/          # API routes
│   │   └── services/         # Business logic
│   ├── alembic/              # Database migrations
│   ├── venv/                 # Python virtual environment
│   ├── requirements.txt
│   └── .env                  # Backend environment variables
├── frontend/
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/            # Route pages
│   │   ├── services/         # API calls
│   │   ├── hooks/            # Custom React hooks
│   │   ├── context/          # Auth context
│   │   ├── types/            # TypeScript types
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── node_modules/         # JS packages (created by npm)
│   ├── package.json
│   └── .env                  # Frontend environment variables
└── .gitignore
```

## Environment Files

You need **TWO** separate `.env` files:

### backend/.env
```
DATABASE_URL=
OPENAI_API_KEY=
RAWG_API_KEY=
```

### frontend/.env
```
VITE_API_URL=http://localhost:8000
VITE_NEON_AUTH_URL=
```

## Quick Reference

| Folder | Purpose |
|--------|---------|
| `backend/venv/` | Python packages (FastAPI, etc.) - managed by pip |
| `frontend/node_modules/` | JavaScript packages (React, etc.) - managed by npm |
| `backend/.env` | API keys, database URL, secrets |
| `frontend/.env` | Frontend config (API URL) |
