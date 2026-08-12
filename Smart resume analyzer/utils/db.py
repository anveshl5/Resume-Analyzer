import sqlite3
import os
import hashlib
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "resume_analyzer.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Analysis History Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            target_role TEXT,
            ats_score REAL,
            present_skills_count INTEGER,
            missing_skills_count INTEGER,
            analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Saved Resumes Builder Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saved_resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            email TEXT,
            target_role TEXT,
            theme TEXT,
            resume_data_json TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Feedback Submissions Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback_submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            user_role TEXT,
            rating INTEGER,
            feedback_text TEXT,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Admin Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Seed Admin User if not exists
    cursor.execute("SELECT * FROM admin_users WHERE username = ?", ("admin@example.com",))
    if not cursor.fetchone():
        admin_pass_hash = hash_password("admin123")
        cursor.execute("INSERT INTO admin_users (username, password_hash) VALUES (?, ?)", ("admin@example.com", admin_pass_hash))

    # Seed initial mock analysis history if empty so dashboard looks great immediately
    cursor.execute("SELECT COUNT(*) FROM analysis_history")
    count = cursor.fetchone()[0]
    if count == 0:
        sample_runs = [
            ("john_doe_resume.pdf", "Data Scientist", 82.5, 14, 4, "2026-08-01 10:15:00"),
            ("john_doe_resume_v2.pdf", "Data Scientist", 88.0, 16, 2, "2026-08-05 14:30:00"),
            ("jane_smith_resume.docx", "Full Stack Developer", 74.0, 11, 6, "2026-08-08 09:45:00"),
            ("alex_dev.pdf", "DevOps Engineer", 91.0, 18, 1, "2026-08-10 16:20:00"),
            ("sample_resume.pdf", "AI / ML Engineer", 85.0, 15, 3, "2026-08-11 11:00:00")
        ]
        for item in sample_runs:
            cursor.execute("""
                INSERT INTO analysis_history (filename, target_role, ats_score, present_skills_count, missing_skills_count, analyzed_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, item)

    # Seed sample feedback if empty
    cursor.execute("SELECT COUNT(*) FROM feedback_submissions")
    fb_count = cursor.fetchone()[0]
    if fb_count == 0:
        sample_fb = [
            ("Sarah Connor", "sarah@example.com", "Job Seeker", 5, "Amazing tool! Loved the ATS keyword breakdown and course recommendations.", "2026-08-02 12:00:00"),
            ("Michael Scott", "michael@dundermifflin.com", "Recruiter", 5, "Super clean interface. The resume templates generated pristine PDFs.", "2026-08-09 15:10:00")
        ]
        for fb in sample_fb:
            cursor.execute("""
                INSERT INTO feedback_submissions (name, email, user_role, rating, feedback_text, submitted_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, fb)

    conn.commit()
    conn.close()

def save_analysis(filename: str, target_role: str, ats_score: float, present_skills_count: int, missing_skills_count: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO analysis_history (filename, target_role, ats_score, present_skills_count, missing_skills_count)
        VALUES (?, ?, ?, ?, ?)
    """, (filename, target_role, ats_score, present_skills_count, missing_skills_count))
    conn.commit()
    conn.close()

def get_all_analyses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM analysis_history ORDER BY analyzed_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def save_feedback(name: str, email: str, user_role: str, rating: int, feedback_text: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO feedback_submissions (name, email, user_role, rating, feedback_text)
        VALUES (?, ?, ?, ?, ?)
    """, (name, email, user_role, rating, feedback_text))
    conn.commit()
    conn.close()

def get_all_feedback():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM feedback_submissions ORDER BY submitted_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def verify_admin(username: str, password_raw: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    pass_hash = hash_password(password_raw)
    cursor.execute("SELECT * FROM admin_users WHERE username = ? AND password_hash = ?", (username, pass_hash))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def get_admin_metrics():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM analysis_history")
    total_analyzed = cursor.fetchone()[0]
    
    cursor.execute("SELECT AVG(ats_score) FROM analysis_history")
    avg_score = cursor.fetchone()[0] or 0.0
    
    cursor.execute("SELECT COUNT(*) FROM feedback_submissions")
    total_feedback = cursor.fetchone()[0]

    cursor.execute("SELECT target_role, COUNT(*) as count FROM analysis_history GROUP BY target_role ORDER BY count DESC")
    top_roles = cursor.fetchall()

    conn.close()
    return {
        "total_analyzed": total_analyzed,
        "avg_score": round(avg_score, 1),
        "total_feedback": total_feedback,
        "top_roles": [dict(r) for r in top_roles]
    }
