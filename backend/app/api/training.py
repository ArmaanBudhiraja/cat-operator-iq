import json
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.db.database import get_db
from backend.app.db.models import TrainingCourse, TrainingProgress, Operator, Recommendation
from backend.app.schemas.schemas import QuizSubmission

router = APIRouter(prefix="/api/training", tags=["Training Hub"])

@router.get("")
def get_courses(operator_id: str = "OP001", db: Session = Depends(get_db)):
    courses = db.query(TrainingCourse).all()
    progress_records = {
        p.course_id: p
        for p in db.query(TrainingProgress).filter(TrainingProgress.operator_id == operator_id).all()
    }

    results = []
    for c in courses:
        p = progress_records.get(c.course_id)
        quiz_data = json.loads(c.quiz_data) if c.quiz_data else []
        results.append({
            "course_id": c.course_id,
            "category": c.category,
            "title": c.title,
            "description": c.description,
            "difficulty": c.difficulty,
            "duration_min": c.duration_min,
            "video_url": c.video_url,
            "quiz_questions": quiz_data,
            "completion_status": p.completion_status if p else "Not Started",
            "score": p.score if p else 0.0,
            "attempts": p.attempts if p else 0
        })

    # Fetch personalized recommendations
    recs = (
        db.query(Recommendation)
        .filter(Recommendation.operator_id == operator_id, Recommendation.category == "Training")
        .all()
    )

    return {
        "courses": results,
        "recommendations": [
            {
                "title": r.title,
                "recommendation": r.recommendation,
                "reason": r.reason,
                "priority": r.priority
            }
            for r in recs
        ]
    }

@router.post("/{course_id}/quiz")
def submit_quiz(course_id: str, submission: QuizSubmission, db: Session = Depends(get_db)):
    course = db.query(TrainingCourse).filter(TrainingCourse.course_id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    quiz_questions = json.loads(course.quiz_data) if course.quiz_data else []
    if not quiz_questions:
        raise HTTPException(status_code=400, detail="No quiz defined for this course")

    # Evaluate answers
    correct_count = 0
    total = len(quiz_questions)
    for q in quiz_questions:
        q_id = q["id"]
        correct_idx = q["answer_idx"]
        user_choice = submission.answers.get(q_id)
        if user_choice == correct_idx:
            correct_count += 1

    score_pct = round((correct_count / total) * 100.0, 1)
    passed = score_pct >= 70.0

    # Upsert TrainingProgress
    prog = (
        db.query(TrainingProgress)
        .filter(
            TrainingProgress.operator_id == submission.operator_id,
            TrainingProgress.course_id == course_id
        )
        .first()
    )

    if not prog:
        prog = TrainingProgress(
            progress_id=f"PRG{uuid.uuid4().hex[:6].upper()}",
            operator_id=submission.operator_id,
            course_id=course_id,
            completion_status="Completed" if passed else "In Progress",
            score=score_pct,
            attempts=1,
            completed_at=datetime.utcnow() if passed else None
        )
        db.add(prog)
    else:
        prog.attempts += 1
        prog.score = max(prog.score, score_pct)
        if passed:
            prog.completion_status = "Completed"
            prog.completed_at = datetime.utcnow()

    # Update operator overall training score
    operator = db.query(Operator).filter(Operator.operator_id == submission.operator_id).first()
    if operator and passed:
        operator.training_score = min(100.0, round(operator.training_score + 1.5, 1))

    db.commit()

    return {
        "course_id": course_id,
        "score_pct": score_pct,
        "correct_answers": correct_count,
        "total_questions": total,
        "passed": passed,
        "status": "Completed" if passed else "In Progress",
        "message": "Congratulations! Course marked Completed." if passed else "Score below 70%. Review material and retry."
    }
