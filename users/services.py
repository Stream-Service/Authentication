from fastapi import HTTPException,status,Request,Depends
from fastapi.responses import JSONResponse
from users.models import User,Userinfo
from core.security import get_hash_password
from core.database import get_db
from auth.utils import check_token,verify_token
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session


oauth2scheme=OAuth2PasswordBearer(tokenUrl='auth/login')


def insert_user(data,db):
    user=db.query(User).filter(User.email==data.email).first()
     
    if user:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,detail="Email is already registered")
    
    new_user=User(firstname=data.firstname,lastname=data.lastname,email=data.email,password=get_hash_password(data.password))
    db.add(new_user)
    db.flush()

    user_info=Userinfo(user_id=new_user.id)
    db.add(user_info)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_data(data:int, db: Session):
    user = db.query(User).filter(User.id == data).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    userinfo = db.query(Userinfo).filter(Userinfo.user_id == data).first()
    if not userinfo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Userinfo not found"
        )
    return userinfo


def get_user(token):
    payload=check_token(token)
    return payload

def get_user_info(user_id,db):
    user=db.query(User).filter(User.id==user_id).first()
     
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="USERNAME OR PASSWOED IS WRONG")
     
    return user

def get_curr_user_id(request:Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing access token")
    
    user_data = get_user(access_token)
    if not user_data:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")
    
    return user_data['user_id']  # or return full user_data if needed

def get_curr_user(token:str= Depends(oauth2scheme),db: Session=Depends(get_db)):
    exception_name=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"could not validate credientials",headers={"WWW-Authenticate":"Bearer"})
    token_data=verify_token(token)

    user=db.query(User).filter(User.id==token_data["user_id"]).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")
    
    return user.id

# def get_curr_user(request:Request):
#     access_token = request.cookies.get("access_token")
#     if not access_token:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing access token")
    
#     user_data = get_user(access_token)
#     if not user_data:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")
    
#     return user_data['user_id'] 


def delete_user(data,db):
    old_user=db.query(User).filter(User.email==data.email).first()
    if not old_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="USER NOT FOUND")
    
     
    db.delete(old_user)
    db.commit()
     
    return 


def insert_data(data,db):
    old_user=db.query(User).filter(User.email==data.email).first()
    if not old_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="USER NOT FOUND")
    
     
    new_user=User(firstname=data.firstname,lastname=data.lastname,email=data.email,password=get_hash_password(data.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def create_userinfo(data,db):
    print(data)
    userinfo = Userinfo(**data.dict())
    db.add(userinfo)
    db.commit()
    db.refresh(userinfo)
    return userinfo

def update_userinfo(data,db,curr_user ):
    userinfo = db.query(User).filter(User.id == curr_user).first()
    if not userinfo:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(userinfo, key, value)
    db.commit()
    db.refresh(userinfo)
    return userinfo