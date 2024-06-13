from sqlalchemy import Column, Integer, Float, String
from database import Base

class UserModel(Base):
    __tablename__="users"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String)
    username = Column(String)
    nip = Column(String)
    password = Column(String)
    level = Column(String)

