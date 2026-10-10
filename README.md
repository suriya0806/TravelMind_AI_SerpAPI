# TravelMind AI 🌍
Plan less. Explore more.

Hackathon-ready AI Travel Operating System MVP.

## Stack
- React + Vite
- Tailwind CSS
- FastAPI + Python
- Agent orchestration service with Flight, Hotel, Discovery, Route, Budget, Safety, Itinerary agents
- Demo provider layer (no API keys required)
- Optional live-provider hooks

## Run
### Backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

The frontend expects the API at http://localhost:8000.

## Full Product + MySQL
The upgraded package includes a complete MySQL schema and backend modules for:
- authentication
- trip persistence
- AI chat
- group-trip membership
- expenses
- agent logs
- live disruption events
- weather snapshots
- saved places
- notifications
- analytics

See `MYSQL_SETUP.md`.


## SerpAPI integration
This version includes SerpAPI live search endpoints for Google Flights, Google Hotels, Google Maps/Places, and Google web search.
The SerpAPI key is configured in `backend/.env` for this local package.
