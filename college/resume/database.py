import sqlite3
import json

DB_PATH = "database.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resume (
        user_id INTEGER PRIMARY KEY,
        full_name TEXT,
        email TEXT,
        phone TEXT,
        linkedin TEXT,
        github TEXT,
        address TEXT,
        college TEXT,
        degree TEXT,
        branch TEXT,
        cgpa TEXT,
        graduation_year TEXT,
        skills TEXT,
        experience TEXT,
        projects TEXT,
        certifications TEXT,
        languages TEXT,
        career_objective TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)
    conn.commit()
    conn.close()

def get_resume(user_id):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM resume WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
        
    # Unpack row into dict
    # Table columns order: user_id, full_name, email, phone, linkedin, github, address, college, degree, branch, cgpa, graduation_year, skills, experience, projects, certifications, languages, career_objective
    data = {
        "user_id": row[0],
        "full_name": row[1] or "",
        "email": row[2] or "",
        "phone": row[3] or "",
        "linkedin": row[4] or "",
        "github": row[5] or "",
        "address": row[6] or "",
        "college": row[7] or "",
        "degree": row[8] or "",
        "branch": row[9] or "",
        "cgpa": row[10] or "",
        "graduation_year": row[11] or "",
    }
    
    # Safely load JSON structures
    try:
        data["skills"] = json.loads(row[12]) if row[12] else []
    except Exception:
        data["skills"] = []
        
    try:
        data["experience"] = json.loads(row[13]) if row[13] else []
    except Exception:
        data["experience"] = []
        
    try:
        data["projects"] = json.loads(row[14]) if row[14] else []
    except Exception:
        data["projects"] = []
        
    try:
        data["certifications"] = json.loads(row[15]) if row[15] else []
    except Exception:
        data["certifications"] = []
        
    try:
        data["languages"] = json.loads(row[16]) if row[16] else []
    except Exception:
        data["languages"] = []
        
    data["career_objective"] = row[17] or ""
    return data

def save_resume(user_id, resume_data):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    skills_json = json.dumps(resume_data.get("skills", []))
    experience_json = json.dumps(resume_data.get("experience", []))
    projects_json = json.dumps(resume_data.get("projects", []))
    certifications_json = json.dumps(resume_data.get("certifications", []))
    languages_json = json.dumps(resume_data.get("languages", []))
    
    cursor.execute("""
    INSERT OR REPLACE INTO resume (
        user_id, full_name, email, phone, linkedin, github, address,
        college, degree, branch, cgpa, graduation_year,
        skills, experience, projects, certifications, languages, career_objective
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        resume_data.get("full_name", ""),
        resume_data.get("email", ""),
        resume_data.get("phone", ""),
        resume_data.get("linkedin", ""),
        resume_data.get("github", ""),
        resume_data.get("address", ""),
        resume_data.get("college", ""),
        resume_data.get("degree", ""),
        resume_data.get("branch", ""),
        resume_data.get("cgpa", ""),
        resume_data.get("graduation_year", ""),
        skills_json,
        experience_json,
        projects_json,
        certifications_json,
        languages_json,
        resume_data.get("career_objective", "")
    ))
    
    conn.commit()
    conn.close()
