from pydantic import BaseModel
from typing import List, Dict



class AttemptCreate(BaseModel):
    student_id: str
    test_id: str
    answers: List[Dict]
