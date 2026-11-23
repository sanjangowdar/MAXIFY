# MAXIFY — Personal Fitness & Lifestyle Tracker

A GitHub-ready starter implementation with a React + Vite + TypeScript frontend and Python FastAPI backend. The app is designed to work locally in **guest mode without the backend**; guest data persists in browser localStorage. When the API is configured, the backend provides health checks, account registration/login, profile storage, and a demo-safe AI endpoint.

## Features
- Welcome screen with Login, Create account, and Continue as Guest.
- Guest mode survives refresh and never requires authentication.
- Optional onboarding with fitness, lifestyle, nutrition, and grooming preferences.
- Dashboard with live values derived from logged activity.
- Workouts, nutrition, water, habits, sleep, progress, looksmaxxing, MAXIFY AI, profile/settings.
- Add, complete, and remove entries; local-first persistence.
- Responsive dark interface with animated accents and charts.
- FastAPI backend with password hashing, JWT sessions, SQLite local DB (PostgreSQL-ready URL), and environment-based secrets.

> This is a working foundation, not a medical device. Nutrition estimates are approximate; consult qualified professionals for medical needs. The AI fallback is explicitly labelled demo mode.

## Run locally

### 1. Frontend
```bash
cd frontend
npm install
npm run dev
```
Open http://localhost:5173. Select **Continue as Guest** to enter immediately.

### 2. Backend (optional for guest mode)
```bash
cd backend
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```
API: http://localhost:8000 — docs: http://localhost:8000/docs

Set `VITE_API_URL=http://localhost:8000` in `frontend/.env` if needed.

## Environment
See `backend/.env.example` and `frontend/.env.example`. Never commit real secrets.

## Production notes
- Frontend: deploy `frontend` to Vercel; set `VITE_API_URL` to the deployed API URL.
- Backend: deploy `backend` to Render or another ASGI host; start command:
  `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Database: set `DATABASE_URL` to a PostgreSQL SQLAlchemy URL in production.
- Set a strong `JWT_SECRET`, `CORS_ORIGINS`, and optional `OPENAI_API_KEY`.
- For production, use HTTPS, managed PostgreSQL, backups, rate limiting, email verification, and a formal privacy policy.

## Current implementation boundaries
- Guest/local-first functionality works without a backend.
- Backend account endpoints are implemented; frontend account forms use local demo mode if API is unreachable and clearly label the session as local demo.
- Admin route is protected and returns no admin access unless an authenticated token has the configured admin role. No public default admin password is included.
- Wearable integrations, push notifications, image-based food recognition, and cloud guest-data transfer require provider credentials/services and are not represented as already connected.
