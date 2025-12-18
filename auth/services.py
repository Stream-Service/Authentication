
from fastapi import HTTPException,status,Response
from users.models import User
from core.security import get_hash_password
from auth.utils import create_access_token,create_referesh_token
from core.security import verify
from auth.model import Token



def authenticate_and_get_token(data,db):
    user=db.query(User).filter(User.email==data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    
    if not verify(data.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'Invalid Credentials')
    data1={"user_id":user.id,'user_email':user.firstname,"user_role":'admin'}
    access_token,refreh_token=create_access_token(data1),create_referesh_token(data1)
    return user.id,access_token,refreh_token



def delete_token(token,db):
    token_data=db.query(Token).filter(Token.token_text==token).first()
    if not token_data:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    
    
    db.delete(token_data)
    db.commit()
     
 