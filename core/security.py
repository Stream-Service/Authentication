from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='/auth/token')

pwd_context=CryptContext(schemes=["argon2"],deprecated='auto')

def get_hash_password(password):
    return pwd_context.hash(password)

def verify(password,hash_password):
    return pwd_context.verify(password,hash_password)