from pydantic import BaseModel,EmailStr
from typing import Optional

class DescriptionUpdate(BaseModel):
    description: str
class RequestUser(BaseModel):
     
    firstname:str
    lastname:str
    email:EmailStr
    password:str


class UserinfoCreate(BaseModel):
     
    role: Optional[str]
    job: Optional[str]
    about: Optional[str]
    location: Optional[str]
    phone_no: Optional[str]
    created_at: Optional[str]

class UserinfoUpdate(BaseModel):
    role: Optional[str]
    job: Optional[str]
    about: Optional[str]
    location: Optional[str]
    phone_no: Optional[str]
    created_at: Optional[str]



class ResponseUser(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    # role: str

    class Config:
        from_attributes = True



