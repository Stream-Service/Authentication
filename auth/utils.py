from datetime import datetime,timedelta
from core.config import Settings
from jose import jwt,JWTError
from fastapi.responses import JSONResponse

setting=Settings()
token_settings=setting.get_token_congigurations()

def get_both_tokens(data):
    cop_data=data.copy()
    expire_time=datetime.utcnow()+timedelta(minutes=token_settings['expiry_minutes'])
    cop_data.update({"expire_time": int(expire_time.timestamp())}) 

    return create_access_token(cop_data),create_referesh_token(cop_data)


def create_access_token(data):
    

    token=jwt.encode(data,token_settings["secret"],algorithm=token_settings["algorithm"])

    return {"access_token":token,"token_type":"Bearer"}

def create_referesh_token(data):
     
    ref_token=jwt.encode(data,token_settings["secret"],algorithm=token_settings["algorithm"])

    return {"refresh_token":ref_token,"token_type":"Bearer"}

from fastapi import Header, HTTPException, status

def verify_token(auth_header: str) -> str:
     
    print(auth_header)
    if not auth_header:
        raise HTTPException(status_code=404, detail="Invalid authorization header")
    return check_token(auth_header)  

def check_token(token):
    try:
        payload=jwt.decode(token,token_settings["secret"],algorithms=[token_settings["algorithm"]])
    except JWTError:
        return None
    return payload


 
    