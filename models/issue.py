from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql import func
from db import Base

class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    ward = Column(String, nullable=False)
    status = Column(String, default="open")
    image_path = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    category = Column(String, nullable=True)
    confidence = Column(Float, nullable=True)
    severity = Column(Float, nullable=True)
    priority = Column(String, nullable=True)
    latitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)
    before_image = Column(String, nullable=True)
    after_image = Column(String, nullable=True)