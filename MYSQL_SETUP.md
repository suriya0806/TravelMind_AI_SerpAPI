# TravelMind AI — MySQL Setup

## 1. Install MySQL
Install MySQL Server + MySQL Workbench.

## 2. Create database
Open Workbench and run:
`backend/schema.sql`

## 3. Configure backend
Copy `backend/.env.example` to `backend/.env` and update:
`DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/travelmind`

## 4. Install dependencies
`pip install -r backend/requirements.txt`

## 5. Start API
`uvicorn backend.main:app --reload --port 8000`
or from backend:
`uvicorn main:app --reload --port 8000`

## 6. Product features covered
- User authentication
- MySQL persistence
- AI trip planning
- AI chat assistant
- Multi-agent logs
- Group-trip data model
- Expense tracking
- Budget analytics
- Weather snapshots
- Live disruption events
- What-if replanning
- Saved places
- Notifications
- Offline-ready trip data model
- Safety/SOS-ready architecture

## Production API integrations
Add provider adapters for:
- Amadeus / aviation provider
- Google Maps
- OpenWeather
- Places/reviews provider
- Groq/OpenAI-compatible LLM

The current demo provider remains usable without API keys.
