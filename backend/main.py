from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import date

app = FastAPI(title="TravelMind AI API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:5174", "http://127.0.0.1:5174", "http://localhost:3000"],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

class TripRequest(BaseModel):
    origin: str = "Chennai"
    destination: str = "Goa"
    start_date: str = "2026-10-12"
    end_date: str = "2026-10-15"
    travellers: int = 2
    budget: float = 25000
    interests: List[str] = ["Food", "Photography", "Culture"]

class WhatIfRequest(BaseModel):
    trip: TripRequest
    scenario: str
    value: Optional[float] = None

class Agent:
    name = "Agent"
    def run(self, ctx): return {}

class FlightAgent(Agent):
    name="Flight Agent"
    def run(self, ctx):
        return {"flights":[
            {"id":"AI-6240","airline":"Air India","from":"Chennai","to":"Goa","depart":"08:30","arrive":"10:55","duration":"2h 25m","price":6240,"tag":"Best Value"},
            {"id":"6E-5850","airline":"IndiGo","from":"Chennai","to":"Goa","depart":"06:20","arrive":"08:45","duration":"2h 25m","price":5850,"tag":"Cheapest"},
            {"id":"UK-7100","airline":"Vistara","from":"Chennai","to":"Goa","depart":"11:15","arrive":"13:35","duration":"2h 20m","price":7100,"tag":"Fastest"}]}

class HotelAgent(Agent):
    name="Hotel Agent"
    def run(self, ctx):
        return {"hotels":[
            {"id":"ocean","name":"Ocean View Resort","rating":4.5,"night":2100,"distance":"1.2 km","amenities":["Breakfast","Wi-Fi","Pool"],"reason":"Balances price, rating and proximity to your planned attractions."},
            {"id":"heritage","name":"Heritage Bay Hotel","rating":4.7,"night":2600,"distance":"1.8 km","amenities":["Breakfast","Wi-Fi","Gym"],"reason":"Highest-rated option with a premium location."},
            {"id":"budget","name":"Palm Grove Stay","rating":4.2,"night":1700,"distance":"2.9 km","amenities":["Wi-Fi","AC"],"reason":"Lowest-cost option for tighter budgets."}]}

class DiscoveryAgent(Agent):
    name="Discovery Agent"
    def run(self, ctx):
        return {"places":[
            {"name":"Fontainhas","rating":4.6,"category":"Photography","time":"12 min","type":"hidden"},
            {"name":"Basilica of Bom Jesus","rating":4.7,"category":"Culture","time":"18 min","type":"popular"},
            {"name":"Miramar Beach","rating":4.5,"category":"Beaches","time":"15 min","type":"popular"},
            {"name":"Local Art Gallery","rating":4.7,"category":"Culture","time":"8 min","type":"hidden"},
            {"name":"Panaji Food Street","rating":4.6,"category":"Food","time":"10 min","type":"hidden"}]}

class RouteAgent(Agent):
    name="Route Agent"
    def run(self, ctx):
        return {"route":{"travel_minutes":42,"transport_cost":380,"saved_minutes":24,"optimized":True}}

class BudgetAgent(Agent):
    name="Budget Agent"
    def run(self, ctx):
        t=ctx["request"]
        travellers = t["travellers"] if isinstance(t, dict) else t.travellers
        budget = t["budget"] if isinstance(t, dict) else t.budget
        hotel = 6300 if travellers == 2 else 8200
        total = 6240 + hotel + 2100 + 3500 + 2700
        return {"budget": {"total": total, "remaining": round(budget - total), "breakdown": {
            "Flights": 6240, "Hotel": hotel, "Transport": 2100, "Food": 3500, "Activities": 2700}}}

class SafetyAgent(Agent):
    name="Safety Agent"
    def run(self, ctx):
        return {"safety":{"status":"clear","notes":["No active travel disruption in demo mode.","Keep local emergency contacts available."]}}

class ItineraryAgent(Agent):
    name="Itinerary Agent"
    def run(self, ctx):
        return {"itinerary":[
            {"day":"Day 1","title":"Explore","items":[
                ["08:30","Flight arrival"],["10:00","Hotel check-in"],["12:00","Local lunch"],["14:00","Heritage walk"],["17:30","Photography at Fontainhas"],["20:00","Dinner"]]},
            {"day":"Day 2","title":"Experience","items":[
                ["09:00","Basilica of Bom Jesus"],["11:30","Panaji food trail"],["14:30","Miramar Beach"],["17:30","Sunset photography"],["20:00","Goan dinner"]]},
            {"day":"Day 3","title":"Relax","items":[
                ["09:00","Slow breakfast"],["10:30","Local Art Gallery"],["13:00","Lunch"],["15:00","Souvenir shopping"],["17:00","Airport transfer"]]}
        ]}

AGENTS=[FlightAgent(),HotelAgent(),DiscoveryAgent(),RouteAgent(),BudgetAgent(),SafetyAgent(),ItineraryAgent()]

def plan(req):
    ctx={"request":req.model_dump(),"agent_activity":[]}
    for a in AGENTS:
        ctx["agent_activity"].append({"name":a.name,"status":"done"})
        ctx.update(a.run(ctx))
    ctx["recommendation"]="The ₹6,240 flight is recommended because it arrives early enough to preserve more of Day 1."
    return ctx

@app.get("/api/health")
def health(): return {"status":"ok","service":"TravelMind AI"}

@app.post("/api/plan")
def create_plan(req: TripRequest):
    return plan(req)

@app.post("/api/what-if")
def what_if(body: WhatIfRequest):
    req=body.trip.model_copy(deep=True)
    scenario=body.scenario.lower()
    if "budget" in scenario:
        target=body.value or 18000
        req.budget=target
        result=plan(req)
        result["what_if"]={"scenario":f"Budget changed to ₹{target:,.0f}","changes":[
            "Cheaper hotel selected","Lower-cost transport selected","One premium activity replaced","Flight alternatives rechecked"],
            "new_total":17850 if target<=18000 else result["budget"]["total"]}
        return result
    if "rain" in scenario or "weather" in scenario:
        result=plan(req)
        result["what_if"]={"scenario":"Rain expected tomorrow","changes":["Outdoor beach block moved","Local Art Gallery added","Map route recalculated","Budget impact: -₹50"]}
        result["itinerary"][1]["items"]=[
            ["09:00","Indoor museum / heritage visit"],["11:30","Panaji food trail"],["14:30","Local Art Gallery"],["17:30","Café + photography"],["20:00","Goan dinner"]]
        return result
    result=plan(req)
    result["what_if"]={"scenario":body.scenario,"changes":["Rechecking flights, hotel, route and activities","A new itinerary will be generated from the updated constraint"]}
    return result

# MySQL / full-product API extensions
try:
    from extended_api import router as extended_router
    app.include_router(extended_router)
except Exception as e:
    print("Extended API not loaded:", e)


# ---------------- SerpAPI live travel search ----------------
try:
    from serpapi_service import search_flights, search_hotels, search_places, search_web
    from pydantic import BaseModel

    class FlightSearchRequest(BaseModel):
        origin: str
        destination: str
        outbound_date: str
        return_date: str | None = None

    class HotelSearchRequest(BaseModel):
        destination: str
        check_in: str
        check_out: str

    class PlacesSearchRequest(BaseModel):
        query: str

    @app.post("/api/serpapi/flights")
    def serpapi_flights(req: FlightSearchRequest):
        return search_flights(req.origin, req.destination, req.outbound_date, req.return_date)

    @app.post("/api/serpapi/hotels")
    def serpapi_hotels(req: HotelSearchRequest):
        return search_hotels(req.destination, req.check_in, req.check_out)

    @app.post("/api/serpapi/places")
    def serpapi_places(req: PlacesSearchRequest):
        return search_places(req.query)

    @app.post("/api/serpapi/web")
    def serpapi_web(req: PlacesSearchRequest):
        return search_web(req.query)

except Exception as e:
    print("SerpAPI integration not loaded:", e)
