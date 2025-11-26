from database import SessionLocal, Quiz, Question
import json

def create_quiz(title, subject, duration, instructions, created_by):
    db = SessionLocal()
    quiz = Quiz(title=title, subject=subject, duration=duration, instructions=instructions, created_by=created_by)
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    db.close()
    return quiz.id

def add_question(quiz_id, question_text, question_type, options, correct_answer):
    db = SessionLocal()
    question = Question(
        quiz_id=quiz_id, 
        question_text=question_text, 
        question_type=question_type,
        options=json.dumps(options) if options else None,
        correct_answer=correct_answer
    )
    db.add(question)
    db.commit()
    db.close()
