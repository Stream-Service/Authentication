from fastapi import FastAPI,HTTPException,status,Request,Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse,HTMLResponse
from users.routes import router as user_router
from users.uploads import router as upload_router
from auth.route import router as auth_router
from users.services import get_curr_user,get_user_info
from auth.utils import get_both_tokens,verify_token
from core.database import engine,get_db
from users.schemas import ResponseUser
from auth.model import Base
Base.metadata.create_all(bind=engine)
 

from fastapi.middleware.cors import CORSMiddleware


app=FastAPI()
 

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(upload_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500","http://127.0.0.1:8004", "http://localhost:8004","http://localhost:8002","http://127.0.0.1:8002","http://localhost:8003","http://127.0.0.1:8003","http://localhost:8082","http://127.0.0.1:8082",
        "http://127.0.0.1:8009","http://localhost:5500",
         
    ],  # your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 

@app.get('/')
def healthcheck():
    
    return JSONResponse("Hey whatupp",status_code=200)
    
 
 
@app.get('/health')
def healthcheck():
    
    return JSONResponse("Health is fine",status_code=200)

@app.get('/refresh')
def refresh(request:Request):
    headers = dict(request.headers)

    
    refresh_token=headers.get("authorization")
    

     
    

    payload=verify_token(refresh_token)
     
    if not payload:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    user_id,role = payload.get("user_email"),payload.get("user_role")
    if not user_id or not role:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token payload")

    return get_both_tokens(payload)

    