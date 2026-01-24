from sqlalchemy import Column, Integer, String
from db import Base

class Engineer(Base):
    __tablename__ = "engineers"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    ward = Column(String, nullable=False)