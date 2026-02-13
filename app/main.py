from sqlalchemy import func

from app.database import Base, engine
from app.models import student, test, attempt

from fastapi import FastAPI

app = FastAPI(
    title="Assessment Ops Mini Platform",
    version="1.0.0"
)
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Assessment Ops API Running"}
from app.schemas.attempt import AttemptCreate
from app.database import SessionLocal
from app.models.attempt import Attempt
from fastapi import FastAPI
app = FastAPI()
@app.post("/attempts")
def create_attempt(attempt_data: AttemptCreate):

    db = SessionLocal()

    try:
        # ✅ Deduplication check
        existing_attempt = (
            db.query(Attempt)
            .filter(
                Attempt.student_id == attempt_data.student_id,
                Attempt.test_id == attempt_data.test_id
            )
            .first()
        )

        if existing_attempt:
            return {
                "message": "Duplicate attempt detected"
            }

        # ✅ Score calculation
        score = 0
        for ans in attempt_data.answers:
            if ans.get("selected") == ans.get("correct"):
                score += 1

        # ✅ Save attempt
        new_attempt = Attempt(
            student_id=attempt_data.student_id,
            test_id=attempt_data.test_id,
            answers=attempt_data.answers,
            score=score
        )

        db.add(new_attempt)
        db.commit()
        db.refresh(new_attempt)

        return {
            "id": new_attempt.id,
            "score": score,
            "message": "Attempt saved successfully"
        }

    finally:
        db.close()
@app.post("/attempts/{attempt_id}/recompute")
def recompute_score(attempt_id: str):
    db = SessionLocal()

    try:
        attempt = db.query(Attempt).filter(
            Attempt.id == attempt_id
        ).first()

        if not attempt:
            return {"message": "Attempt not found"}

        score = 0
        for ans in attempt.answers:
            if ans.get("selected") == ans.get("correct"):
                score += 1

        attempt.score = score
        db.commit()

        return {
            "id": attempt.id,
            "score": score,
            "message": "Score recomputed"
        }

    finally:
        db.close()


@app.get("/attempts")
def get_attempts():

    db = SessionLocal()

    try:
        attempts = db.query(Attempt).all()

        result = []
        for a in attempts:
            result.append({
                "id": a.id,
                "student_id": a.student_id,
                "test_id": a.test_id,
                "score": a.score
            })

        return result

    finally:
        db.close()
        
@app.get("/leaderboard")
def leaderboard():
    db = SessionLocal()
    try:
        results = (
            db.query(
                Attempt.student_id,
                func.sum(Attempt.score).label("total_score")
            )
            .group_by(Attempt.student_id)
            .order_by(func.sum(Attempt.score).desc())
            .all()
        )

        return [
            {
                "student_id": r.student_id,
                "total_score": r.total_score
            }
            for r in results
        ]

    finally:
        db.close()


@app.post("/attempts/{attempt_id}/flag")
def flag_attempt(attempt_id: str):
    db = SessionLocal()

    try:
        attempt = db.query(Attempt).filter(
            Attempt.id == attempt_id
        ).first()

        if not attempt:
            return {"message": "Attempt not found"}

        attempt.flagged = True
        db.commit()

        return {
            "id": attempt.id,
            "message": "Attempt flagged successfully"
        }

    finally:
        db.close()
