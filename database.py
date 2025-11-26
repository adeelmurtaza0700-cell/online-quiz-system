from supabase import create_client
from data.config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Users table: id, username, password, role
# Quizzes table: id, title
# Questions table: id, quiz_id, question, opt1, opt2, opt3, opt4, answer
# Results table: id, user_id, quiz_id, score
# Leaderboard table: user_id, total_score

def create_user(username, password, role):
    return supabase.table("users").insert({"username": username, "password": password, "role": role}).execute()

def get_user(username):
    return supabase.table("users").select("*").eq("username", username).execute()

def add_quiz(title):
    return supabase.table("quizzes").insert({"title": title}).execute()

def add_question(quiz_id, question, opt1, opt2, opt3, opt4, answer):
    return supabase.table("questions").insert({
        "quiz_id": quiz_id, "question": question, "opt1": opt1,
        "opt2": opt2, "opt3": opt3, "opt4": opt4, "answer": answer
    }).execute()

def get_quizzes():
    return supabase.table("quizzes").select("*").execute()

def get_questions(quiz_id):
    return supabase.table("questions").select("*").eq("quiz_id", quiz_id).execute()

def save_result(user_id, quiz_id, score):
    supabase.table("results").insert({"user_id": user_id, "quiz_id": quiz_id, "score": score}).execute()
    # Update leaderboard
    supabase.table("leaderboard").upsert({"user_id": user_id, "total_score": score}, on_conflict="user_id").execute()

def get_leaderboard():
    return supabase.table("leaderboard").select("*").order("total_score", desc=True).execute()
