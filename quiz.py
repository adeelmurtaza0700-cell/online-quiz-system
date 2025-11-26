from database import SessionLocal, Quiz, Question, Result
import json
import random

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

def get_quizzes():
    db = SessionLocal()
    quizzes = db.query(Quiz).all()
    db.close()
    return quizzes

def get_questions(quiz_id):
    db = SessionLocal()
    questions = db.query(Question).filter(Question.quiz_id==quiz_id).all()
    db.close()
    random.shuffle(questions)
    return questions

def grade_quiz(user_id, quiz_id, answers):
    db = SessionLocal()
    questions = db.query(Question).filter(Question.quiz_id==quiz_id).all()
    score = 0
    for q in questions:
        if answers.get(str(q.id)) == q.correct_answer:
            score += 1
    result = Result(user_id=user_id, quiz_id=quiz_id, score=score)
    db.add(result)
    db.commit()
    db.close()
    return score

def get_results(quiz_id):
    db = SessionLocal()
    results = db.query(Result).filter(Result.quiz_id==quiz_id).order_by(Result.score.desc()).all()
    db.close()
    return results
