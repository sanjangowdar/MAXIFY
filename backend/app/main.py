import os,json
from fastapi import FastAPI,Depends,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import Base,engine,get_db
from .models import User,Profile
from .schemas import Credentials,ProfileIn,ChatIn
from .security import hash_password,verify_password,make_token,oauth,decode
Base.metadata.create_all(bind=engine)
app=FastAPI(title="MAXIFY API",version="1.0.0")
origins=os.getenv("CORS_ORIGINS","http://localhost:5173").split(",")
app.add_middleware(CORSMiddleware,allow_origins=[x.strip() for x in origins],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
def current_user(token:str=Depends(oauth),db:Session=Depends(get_db)):
    claims=decode(token);user=db.get(User,int(claims["sub"]))
    if not user:raise HTTPException(401,"User not found")
    return user
@app.get("/health")
def health():return {"status":"ok","service":"MAXIFY API"}
@app.post("/auth/register")
def register(body:Credentials,db:Session=Depends(get_db)):
    if db.query(User).filter_by(email=body.email.lower()).first():raise HTTPException(409,"An account with this email already exists")
    user=User(email=body.email.lower(),password_hash=hash_password(body.password))
    db.add(user);db.commit();db.refresh(user)
    return {"access_token":make_token(user),"token_type":"bearer","user":{"id":user.id,"email":user.email,"role":user.role}}
@app.post("/auth/login")
def login(body:Credentials,db:Session=Depends(get_db)):
    user=db.query(User).filter_by(email=body.email.lower()).first()
    if not user or not verify_password(body.password,user.password_hash):raise HTTPException(401,"Incorrect email or password")
    return {"access_token":make_token(user),"token_type":"bearer","user":{"id":user.id,"email":user.email,"role":user.role}}
@app.get("/me")
def me(user:User=Depends(current_user)):return {"id":user.id,"email":user.email,"role":user.role}
@app.get("/profile")
def get_profile(user:User=Depends(current_user),db:Session=Depends(get_db)):
    p=db.query(Profile).filter_by(user_id=user.id).first()
    return {"display_name":p.display_name,"data":json.loads(p.data_json)} if p else {"display_name":"","data":{}}
@app.put("/profile")
def put_profile(body:ProfileIn,user:User=Depends(current_user),db:Session=Depends(get_db)):
    p=db.query(Profile).filter_by(user_id=user.id).first()
    if not p:p=Profile(user_id=user.id);db.add(p)
    p.display_name=body.display_name;p.data_json=json.dumps(body.data);db.commit()
    return {"saved":True}
@app.post("/ai/chat")
def chat(body:ChatIn,user:User=Depends(current_user)):
    if not os.getenv("OPENAI_API_KEY"):
        return {"mode":"demo","answer":"Demo assistant: start with one manageable action, track it consistently, and adjust to your own ability and preferences. For medical or nutrition conditions, consult a qualified professional."}
    # Keep provider calls server-side; connect your chosen model provider here before enabling live AI.
    return {"mode":"configured-not-connected","answer":"An AI key is present, but no provider adapter has been configured yet. Add a server-side provider integration before using live responses."}
@app.get("/admin/overview")
def admin_overview(user:User=Depends(current_user),db:Session=Depends(get_db)):
    configured=os.getenv("ADMIN_EMAIL","").lower()
    if user.role!="admin" or not configured or user.email!=configured:raise HTTPException(403,"Admin access required")
    return {"registered_users":db.query(User).count(),"status":"operational"}
