from datetime import datetime
from app.database import Base
from sqlalchemy import Column,Integer,String,DateTime, Text


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    filepath = Column(String(750),nullable=False)
    filetype = Column(String(50),nullable=False)
    status = Column(String(50),default="PENDING")
    extracted_json = Column(Text)
    error_message = Column(String(1000), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)



