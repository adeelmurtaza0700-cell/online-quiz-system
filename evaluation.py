from database import SessionLocal, Result, Question
import json

def grade_quiz(user_id, quiz_id, answers):
    db = SessionLocal()
    questions = db.query(Question).filter(Question.quiz_id==quiz_id).all()
    score = 0
    for q in questions:
        correct = q.correct_answer
        if answers.get(str(q.id)) == correct:
            score += 1
    result = Result(user_id=user_id, quiz_id=quiz_id, score=score)
    db.add(result)
    db.commit()
    db.close()
    return score
