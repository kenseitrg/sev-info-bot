from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key = True)
    tg_id = Column(Integer)

    def __init__(self, user_id):
        self.tg_id = user_id

class MsgHash(Base):
    __tablename__ = "msgHash"
    id = Column(Integer, primary_key = True)
    msg_type = Column(String)
    msg_hash = Column(String)

    def __init__(self, msg_type, hash):
        self.msg_type = msg_type
        self.msg_hash = hash