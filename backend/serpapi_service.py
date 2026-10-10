import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

def serpapi_search(engine: str, params: dict):
    if not SERPAPI_KEY:
        raise RuntimeError("SERPAPI_KEY is not configured in backend/.env")
    query = dict(params)
    query.update({"engine": engine, "api_key": SERPAPI_KEY, "output": "json"})
    response = requests.get("https://serpapi.com/search.json", params=query, timeout=30)
    response.raise_for_status()
    return response.json()

def search_flights(origin: str, destination: str, outbound_date: str, return_date: str | None = None):
    params = {
        "departure_id": origin,
        "arrival_id": destination,
        "outbound_date": outbound_date,
        "currency": "INR",
        "hl": "en",
        "gl": "in",
    }
    if return_date:
        params["return_date"] = return_date
        params["type"] = "1"
    else:
        params["type"] = "2"
    return serpapi_search("google_flights", params)

def search_hotels(destination: str, check_in: str, check_out: str):
    return serpapi_search("google_hotels", {
        "q": destination,
        "check_in_date": check_in,
        "check_out_date": check_out,
        "currency": "INR",
        "hl": "en",
        "gl": "in",
    })

def search_places(query: str):
    return serpapi_search("google_maps", {
        "q": query,
        "hl": "en",
        "gl": "in",
    })

def search_web(query: str):
    return serpapi_search("google", {
        "q": query,
        "hl": "en",
        "gl": "in",
    })
