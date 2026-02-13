from sqlalchemy import Column, String, DateTime, JSON, ForeignKey,Integer
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database import Base
from sqlalchemy import Boolean


class Attempt(Base):
    __tablename__ = "attempts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    student_id = Column(String, ForeignKey("students.id"), nullable=False)
    test_id = Column(String, ForeignKey("tests.id"), nullable=False)

    answers = Column(JSON, nullable=False)
    score = Column(Integer, default=0)
    flagged = Column(Boolean, default=False)

    flagged = Column(Boolean, default=False)
    source_event_id = Column(String, nullable=True)
    started_at = Column(DateTime, nullable=True)
    submitted_at = Column(DateTime, nullable=True)

    raw_payload = Column(JSON, nullable=True)

    status = Column(String, default="INGESTED")
    created_at = Column(DateTime, default=datetime.utcnow)

    # ONLY THESE RELATIONSHIPS
    student = relationship("Student", back_populates="attempts")
    test = relationship("Test", back_populates="attempts")


