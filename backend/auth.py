from passlib.context import CryptContext
from jose import jwt
from datetime import datetime,timedelta
import os
pwd=CryptContext(schemes=["bcrypt"],deprecated="auto")
SECRET=os.getenv("JWT_SECRET","travelmind-dev-secret")
ALGO="HS256"
def hash_password(p): return pwd.hash(p)
def verify_password(p,h): return pwd.verify(p,h)
def create_token(user_id):
    return jwt.encode({"sub":str(user_id),"exp":datetime.utcnow()+timedelta(days=7)},SECRET,algorithm=ALGO)
