from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    prediction = Column(String)
    confidence = Column(String) # Storing as string "98.5%" for simplicity
    timestamp = Column(DateTime, default=datetime.utcnow)
