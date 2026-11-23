import os
from datetime import datetime,timedelta,timezone
from jose import jwt,JWTError
from passlib.context import CryptContext
from fastapi import HTTPException,status
from fastapi.security import OAuth2PasswordBearer
pwd=CryptContext(schemes=["bcrypt"],deprecated="auto")
oauth=OAuth2PasswordBearer(tokenUrl="/auth/login")
SECRET=os.getenv("JWT_SECRET","dev-only-change-me")
ALG="HS256"
def hash_password(p): return pwd.hash(p)
def verify_password(p,h): return pwd.verify(p,h)
def make_token(user):
    exp=datetime.now(timezone.utc)+timedelta(minutes=int(os.getenv("JWT_EXPIRE_MINUTES","10080")))
    return jwt.encode({"sub":str(user.id),"role":user.role,"exp":exp},SECRET,algorithm=ALG)
def decode(token):
    try:return jwt.decode(token,SECRET,algorithms=[ALG])
    except JWTError:raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid or expired session")
