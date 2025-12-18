from fastapi import APIRouter,Depends,Request,Cookie
from fastapi.responses import RedirectResponse,HTMLResponse,JSONResponse

from sqlalchemy.orm import Session
from core.database import get_db
from auth.model import Token
from users.services import get_user,get_user_info
from users.schemas import ResponseUser
from fastapi.security import OAuth2PasswordRequestForm
from auth.services import authenticate_and_get_token
from users.routes import templates

router=APIRouter(tags=["Auth"],prefix="/auth")

# @router.get("/login", response_class=HTMLResponse)
# def login_page(request: Request):
#     access_token = request.cookies.get("access_token")
#     if access_token and get_user(access_token):
#         return RedirectResponse(url="/users/profile", status_code=303)
#     return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login(data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
   

    user_id,access_token,refresh_token=authenticate_and_get_token(data,db)
    
    access_token = access_token["access_token"]
    refresh_token = refresh_token["refresh_token"]
    token_=Token(user_id=user_id,token_text=refresh_token)
    db.add(token_)
    db.commit()
    response = JSONResponse(
        content={"access_token": access_token, "refresh_token": refresh_token}
    )
    response.set_cookie(
    key="access_token",
    value=access_token,
    httponly=True,
    samesite="lax",   # works locally
    secure=False
)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True,samesite="lax",  
    secure=False )
    response.set_cookie(key="user_id", value=user_id,httponly=True,samesite="lax",  
    secure=False )

          
    return response
    

@router.get("/logout")
def logout(request:Request,access_token:str=Cookie(None),db:Session=Depends(get_db)):
    access_token = request.cookies.get("access_token")
    print(access_token)
    
    response = JSONResponse(content={"message": access_token})
    
    return response
    
    
    