from sqlalchemy import Column, Integer, String, Enum
from database import Base
from schemas import StateEnum

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    resume_url = Column(String)
    
    state = Column(Enum(StateEnum))
    