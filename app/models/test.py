from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database import Base


class Test(Base):
    __tablename__ = "tests"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    # IMPORTANT RELATIONSHIP
    attempts = relationship("Attempt", back_populates="test")

   