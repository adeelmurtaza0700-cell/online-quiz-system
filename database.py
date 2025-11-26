import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor

conn = psycopg2.connect(
    host=st.secrets["DB_HOST"],
    database=st.secrets["DB_NAME"],
    user=st.secrets["DB_USER"],
    password=st.secrets["DB_PASS"]
)

def execute_query(query, params=None):
    with conn.cursor() as cur:
        cur.execute(query, params)
        conn.commit()

def fetch_one(query, params=None):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(query, params)
        return cur.fetchone()

def fetch_all(query, params=None):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(query, params)
        return cur.fetchall()
