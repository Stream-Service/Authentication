from core.database import Base
from sqlalchemy import Column,Integer,String,Boolean,Text,ForeignKey,DateTime
from datetime import datetime, timezone
class User(Base):
    __tablename__ = "users"
    id          = Column(Integer, primary_key=True, autoincrement=True)
    firstname   = Column(String(255), nullable=False)
    lastname    = Column(String(255), nullable=False)
    email       = Column(String(255), nullable=False, unique=True)
    password    = Column(String(2555), nullable=False)
    created_at  = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class Userinfo(Base):
    __tablename__ = "usersinfo"
    id          = Column(Integer, primary_key=True, autoincrement=True)
    user_id     = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    about       = Column(Text, nullable=True)        # ✅ kept — description
    location    = Column(String(255), nullable=True) # ✅ kept — useful
    phone_no    = Column(String(20), nullable=True)  # ✅ kept — useful
     