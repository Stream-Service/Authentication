from core.database import Base
from sqlalchemy import Column,Integer,String,Boolean,Text,ForeignKey


class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname=Column(String(255),nullable=False)
    lastname=Column(String(255),nullable=False)
    email=Column(String(255),nullable=False,unique=True)
    password=Column(String(2555),nullable=False)


 
 


class Userinfo(Base):
    __tablename__ = "usersinfo"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String(50))
    job = Column(String(255))
    about = Column(String(255))
    location = Column(String(255))
    phone_no = Column(String(255))
    created_at = Column(String(255))