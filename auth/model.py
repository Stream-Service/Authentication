from sqlalchemy import Integer,Text,Column

from core.database import Base

class Token(Base):
    __tablename__="refresh_token"
    token_id=Column(Integer,primary_key=True,autoincrement=True)
    user_id=Column(Integer,nullable=False)
    token_text=Column(Text)