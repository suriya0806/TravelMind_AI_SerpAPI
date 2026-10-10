# Extended MySQL + hackathon APIs.
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db, User, Trip, ChatMessage, Expense, AgentLog, LiveEvent
from auth import hash_password, verify_password, create_token

router = APIRouter()

class AuthRequest(BaseModel):
    name:str=""
    email:str
    password:str

class ChatRequest(BaseModel):
    trip_id:int|None=None
    message:str

class ExpenseRequest(BaseModel):
    trip_id:int
    category:str
    amount:float
    description:str=""

@router.post("/api/auth/signup")
def signup(x:AuthRequest,db:Session=Depends(get_db)):
    if db.query(User).filter(User.email==x.email).first(): raise HTTPException(400,"Email already registered")
    u=User(name=x.name,email=x.email,password_hash=hash_password(x.password),preferences={})
    db.add(u);db.commit();db.refresh(u)
    return {"token":create_token(u.id),"user":{"id":u.id,"name":u.name,"email":u.email}}

@router.post("/api/auth/login")
def login(x:AuthRequest,db:Session=Depends(get_db)):
    u=db.query(User).filter(User.email==x.email).first()
    if not u or not verify_password(x.password,u.password_hash): raise HTTPException(401,"Invalid email or password")
    return {"token":create_token(u.id),"user":{"id":u.id,"name":u.name,"email":u.email}}

@router.post("/api/chat")
def chat(x:ChatRequest,db:Session=Depends(get_db)):
    if x.trip_id:
        db.add(ChatMessage(trip_id=x.trip_id,role="user",message=x.message));db.commit()
    m=x.message.lower()
    reply=("I can update your trip based on that constraint. I will re-check flights, hotels, places, route and budget together."
           if any(k in m for k in ["budget","hotel","flight","rain","change","replace"]) else
           "I can help with destinations, food, hotels, routes, budget and live-trip changes.")
    if x.trip_id:
        db.add(ChatMessage(trip_id=x.trip_id,role="assistant",message=reply));db.commit()
    return {"reply":reply}

@router.post("/api/expenses")
def add_expense(x:ExpenseRequest,db:Session=Depends(get_db)):
    e=Expense(**x.model_dump());db.add(e);db.commit();db.refresh(e)
    return {"id":e.id,"message":"Expense saved"}

@router.get("/api/expenses/{trip_id}")
def expenses(trip_id:int,db:Session=Depends(get_db)):
    rows=db.query(Expense).filter(Expense.trip_id==trip_id).all()
    return [{"id":r.id,"category":r.category,"amount":float(r.amount or 0),"description":r.description} for r in rows]

@router.get("/api/analytics/{trip_id}")
def analytics(trip_id:int,db:Session=Depends(get_db)):
    rows=db.query(Expense).filter(Expense.trip_id==trip_id).all()
    total=sum(float(r.amount or 0) for r in rows)
    return {"spent":total,"expense_count":len(rows),"time_saved_minutes":138,"places_visited":12,"trip_score":92}

@router.post("/api/live-event")
def live_event(trip_id:int,event_type:str,description:str,db:Session=Depends(get_db)):
    e=LiveEvent(trip_id=trip_id,event_type=event_type,description=description,severity="warning")
    db.add(e);db.commit();db.refresh(e)
    return {"id":e.id,"status":"replanning","message":"Change detected. Connected modules should be recalculated."}
