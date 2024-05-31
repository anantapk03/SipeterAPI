from sqlalchemy import Column, Integer, Float, String
from database import Base

class UserModel(Base):
    __tablename__="users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String)
    level = Column(String)
    password = Column(String)
