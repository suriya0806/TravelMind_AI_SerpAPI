from sqlalchemy import create_engine, Column, BigInteger, String, Text, Date, DateTime, Integer, Numeric, Boolean, ForeignKey, JSON, Enum
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.sql import func
import os
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL=os.getenv("DATABASE_URL","mysql+pymysql://root:password@localhost:3306/travelmind")
engine=create_engine(DATABASE_URL,pool_pre_ping=True)
SessionLocal=sessionmaker(bind=engine,autocommit=False,autoflush=False)
Base=declarative_base()

class User(Base):
    __tablename__="users"
    id=Column(BigInteger,primary_key=True,autoincrement=True)
    name=Column(String(120),nullable=False)
    email=Column(String(255),unique=True,nullable=False)
    password_hash=Column(String(255),nullable=False)
    preferences=Column(JSON)
    created_at=Column(DateTime,server_default=func.now())

class Trip(Base):
    __tablename__="trips"
    id=Column(BigInteger,primary_key=True,autoincrement=True)
    user_id=Column(BigInteger,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    origin=Column(String(120),nullable=False)
    destination=Column(String(120),nullable=False)
    start_date=Column(Date,nullable=False)
    end_date=Column(Date,nullable=False)
    travellers=Column(Integer,default=1)
    budget=Column(Numeric(12,2),default=0)
    status=Column(String(30),default="draft")
    created_at=Column(DateTime,server_default=func.now())

class ChatMessage(Base):
    __tablename__="chat_messages"
    id=Column(BigInteger,primary_key=True,autoincrement=True)
    trip_id=Column(BigInteger,ForeignKey("trips.id",ondelete="CASCADE"))
    user_id=Column(BigInteger,ForeignKey("users.id",ondelete="SET NULL"))
    role=Column(String(20),nullable=False)
    message=Column(Text,nullable=False)
    created_at=Column(DateTime,server_default=func.now())

class Expense(Base):
    __tablename__="expenses"
    id=Column(BigInteger,primary_key=True,autoincrement=True)
    trip_id=Column(BigInteger,ForeignKey("trips.id",ondelete="CASCADE"),nullable=False)
    user_id=Column(BigInteger,ForeignKey("users.id",ondelete="SET NULL"))
    category=Column(String(80))
    amount=Column(Numeric(12,2))
    description=Column(String(255))
    spent_at=Column(DateTime,server_default=func.now())

class AgentLog(Base):
    __tablename__="agent_logs"
    id=Column(BigInteger,primary_key=True,autoincrement=True)
    trip_id=Column(BigInteger,ForeignKey("trips.id",ondelete="CASCADE"))
    agent_name=Column(String(100))
    status=Column(String(30),default="working")
    input_data=Column(JSON)
    output_data=Column(JSON)
    created_at=Column(DateTime,server_default=func.now())

class LiveEvent(Base):
    __tablename__="live_events"
    id=Column(BigInteger,primary_key=True,autoincrement=True)
    trip_id=Column(BigInteger,ForeignKey("trips.id",ondelete="CASCADE"),nullable=False)
    event_type=Column(String(80))
    severity=Column(String(30),default="info")
    description=Column(Text)
    old_plan=Column(JSON)
    new_plan=Column(JSON)
    resolved=Column(Boolean,default=False)
    created_at=Column(DateTime,server_default=func.now())

def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()
