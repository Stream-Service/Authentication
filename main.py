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
templates = Jinja2Templates(directory="templates")

from fastapi.middleware.cors import CORSMiddleware


app=FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

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

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/upload")
def show_upload_page(request: Request,curr_user: str = Depends(get_curr_user), db: Session = Depends(get_db)):

    user = get_user_info(curr_user, db)
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    user_data = ResponseUser.from_orm(user).dict()

    return templates.TemplateResponse("upload_file.html", {
        "request": request,
        "access": access_token,
        "refresh": refresh_token,
        "user_info": user_data,
        "user_id": curr_user,
         
    })
     

@app.get("/videos")
def show_upload_page(request: Request,curr_user: str = Depends(get_curr_user), db: Session = Depends(get_db)):

    user = get_user_info(curr_user, db)
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    user_data = ResponseUser.from_orm(user).dict()

    return templates.TemplateResponse("stream_video.html", {
        "request": request,
        "access": access_token,
        "refresh": refresh_token,
        "user_info": user_data,
        "crush_id": curr_user,
         
    })

@app.get("/pop/{crush_id}")
def show_post_page(request: Request,crush_id:int,db: Session = Depends(get_db)):
    user_data = {}  # or skip user info entirely
    return templates.TemplateResponse("popup.html", {"request": request, "crush_id": crush_id})


@app.get("/new")
def show_post_page(request: Request, db: Session = Depends(get_db)):
    user_data = {}  # or skip user info entirely
    return templates.TemplateResponse("newnew.html", {"request": request, "user_info": user_data})

@app.get("/post")
def show_post_page(request: Request, db: Session = Depends(get_db)):
    user_data = {}  # or skip user info entirely
    return templates.TemplateResponse("posts.html", {"request": request, "user_info": user_data})

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

    