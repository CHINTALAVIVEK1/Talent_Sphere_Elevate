import sqlite3
import datetime

DB_PATH = "database.db"

def get_db_connection():
    return sqlite3.connect(DB_PATH, timeout=30.0)

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. coding_progress: tracks streak and overall statistics
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS coding_progress (
        user_id INTEGER PRIMARY KEY,
        streak INTEGER DEFAULT 0,
        longest_streak INTEGER DEFAULT 0,
        time_spent INTEGER DEFAULT 0,
        overall_readiness INTEGER DEFAULT 0,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)
    
    # 2. leetcode_progress: tracks solved in-app sandbox problems
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leetcode_progress (
        user_id INTEGER,
        problem_id TEXT,
        status TEXT, -- 'Solved', 'Attempted', 'Pending'
        is_favorite INTEGER DEFAULT 0,
        last_solved TEXT,
        PRIMARY KEY (user_id, problem_id),
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)
    
    # 3. roadmap_progress: tracks learning roadmap subtopics
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS roadmap_progress (
        user_id INTEGER,
        topic TEXT,
        subtopic TEXT,
        completed INTEGER DEFAULT 0,
        completion_date TEXT,
        PRIMARY KEY (user_id, topic, subtopic),
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)
    
    # 4. placement_tracker: tracks job/internship applications
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS placement_tracker (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        company TEXT,
        role TEXT,
        status TEXT, -- 'Applied', 'Interviewing', 'Offered', 'Rejected'
        package TEXT,
        interview_date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)
    
    # 5. profile_reviews: caches LinkedIn and GitHub portfolio evaluations
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profile_reviews (
        user_id INTEGER PRIMARY KEY,
        github_url TEXT,
        github_review TEXT,
        github_score INTEGER,
        linkedin_url TEXT,
        linkedin_review TEXT,
        linkedin_score INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)
    
    # 6. interview_progress: tracks technical interview questions
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interview_progress (
        user_id INTEGER,
        question_id TEXT,
        completed INTEGER DEFAULT 0,
        notes TEXT DEFAULT '',
        PRIMARY KEY (user_id, question_id),
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)
    
    # 7. bookmarks: tracks bookmarked items
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookmarks (
        user_id INTEGER,
        item_type TEXT,
        item_id TEXT,
        PRIMARY KEY (user_id, item_type, item_id),
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # 8. aptitude_scores: tracks aptitude diagnostic results
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS aptitude_scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        category TEXT,
        score INTEGER,
        total INTEGER,
        date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # 9. certifications: tracks verified accomplishments
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS certifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        provider TEXT,
        completion_date TEXT,
        credential_id TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # 10. planner_tasks: checkbox planner logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS planner_tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        task_text TEXT,
        completed INTEGER DEFAULT 0,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)
    
    # 11. student_profile: tracks student profile details
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_profile (
        user_id INTEGER PRIMARY KEY,
        college_name TEXT,
        degree TEXT,
        department TEXT,
        year_of_study TEXT,
        cgpa_percentage TEXT,
        skills TEXT,
        interested_roles TEXT,
        resume_filename TEXT,
        resume_bytes BLOB,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)
    
    conn.commit()
    conn.close()

# --- Helper Queries ---

def get_coding_progress(user_id):
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM coding_progress WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            "user_id": row[0],
            "streak": row[1] or 0,
            "longest_streak": row[2] or 0,
            "time_spent": row[3] or 0,
            "overall_readiness": row[4] or 0
        }
    return {"user_id": user_id, "streak": 0, "longest_streak": 0, "time_spent": 0, "overall_readiness": 0}

def save_coding_progress(user_id, stats):
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR REPLACE INTO coding_progress (user_id, streak, longest_streak, time_spent, overall_readiness)
    VALUES (?, ?, ?, ?, ?)
    """, (user_id, stats.get("streak", 0), stats.get("longest_streak", 0), stats.get("time_spent", 0), stats.get("overall_readiness", 0)))
    conn.commit()
    conn.close()

def get_leetcode_progress(user_id):
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leetcode_progress WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return {r[1]: {"status": r[2], "is_favorite": bool(r[3]), "last_solved": r[4] or ""} for r in rows}

def save_leetcode_progress(user_id, problem_id, status, is_favorite=0, last_solved=None):
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    if last_solved is None and status == "Solved":
        last_solved = datetime.date.today().isoformat()
    cursor.execute("""
    INSERT OR REPLACE INTO leetcode_progress (user_id, problem_id, status, is_favorite, last_solved)
    VALUES (?, ?, ?, ?, ?)
    """, (user_id, problem_id, status, int(is_favorite), last_solved))
    conn.commit()
    conn.close()

def get_roadmap_progress(user_id):
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT topic, subtopic, completed, completion_date FROM roadmap_progress WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    
    progress = {}
    for topic, subtopic, completed, comp_date in rows:
        if topic not in progress:
            progress[topic] = {}
        progress[topic][subtopic] = {"completed": bool(completed), "completion_date": comp_date or ""}
    return progress

def save_roadmap_progress(user_id, topic, subtopic, completed, completion_date=None):
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    if completed and not completion_date:
        completion_date = datetime.date.today().isoformat()
    cursor.execute("""
    INSERT OR REPLACE INTO roadmap_progress (user_id, topic, subtopic, completed, completion_date)
    VALUES (?, ?, ?, ?, ?)
    """, (user_id, topic, subtopic, int(completed), completion_date))
    conn.commit()
    conn.close()

def get_placements(user_id):
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, company, role, status, package, interview_date FROM placement_tracker WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "company": r[1], "role": r[2], "status": r[3], "package": r[4], "interview_date": r[5]} for r in rows]

def save_placement(user_id, company, role, status, package, interview_date, item_id=None):
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    if item_id:
        cursor.execute("""
        UPDATE placement_tracker SET company=?, role=?, status=?, package=?, interview_date=? WHERE id=? AND user_id=?
        """, (company, role, status, package, interview_date, item_id, user_id))
    else:
        cursor.execute("""
        INSERT INTO placement_tracker (user_id, company, role, status, package, interview_date)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, company, role, status, package, interview_date))
    conn.commit()
    conn.close()

def delete_placement(user_id, item_id):
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM placement_tracker WHERE id=? AND user_id=?", (item_id, user_id))
    conn.commit()
    conn.close()

def get_profile_review(user_id):
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profile_reviews WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "user_id": row[0],
            "github_url": row[1] or "",
            "github_review": row[2] or "",
            "github_score": row[3] or 0,
            "linkedin_url": row[4] or "",
            "linkedin_review": row[5] or "",
            "linkedin_score": row[6] or 0
        }
    return None

def save_profile_review(user_id, github_url, github_review, github_score, linkedin_url, linkedin_review, linkedin_score):
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR REPLACE INTO profile_reviews (user_id, github_url, github_review, github_score, linkedin_url, linkedin_review, linkedin_score)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_id, github_url, github_review, int(github_score), linkedin_url, linkedin_review, int(linkedin_score)))
    conn.commit()
    conn.close()

def get_interview_progress(user_id):
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT question_id, completed, notes FROM interview_progress WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return {r[0]: {"completed": bool(r[1]), "notes": r[2] or ""} for r in rows}

def save_interview_progress(user_id, question_id, completed, notes=""):
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR REPLACE INTO interview_progress (user_id, question_id, completed, notes)
    VALUES (?, ?, ?, ?)
    """, (user_id, question_id, int(completed), notes))
    conn.commit()
    conn.close()

def save_bookmark(user_id, item_type, item_id, bookmarked):
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    if bookmarked:
        cursor.execute("INSERT OR REPLACE INTO bookmarks (user_id, item_type, item_id) VALUES (?, ?, ?)", (user_id, item_type, item_id))
    else:
        cursor.execute("DELETE FROM bookmarks WHERE user_id = ? AND item_type = ? AND item_id = ?", (user_id, item_type, item_id))
    conn.commit()
    conn.close()

def get_bookmarks(user_id, item_type):
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT item_id FROM bookmarks WHERE user_id = ? AND item_type = ?", (user_id, item_type))
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows]

def get_aptitude_scores(user_id):
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT category, score, total, date FROM aptitude_scores WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{"category": r[0], "score": r[1], "total": r[2], "date": r[3]} for r in rows]

def save_aptitude_score(user_id, category, score, total):
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO aptitude_scores (user_id, category, score, total, date)
    VALUES (?, ?, ?, ?, ?)
    """, (user_id, category, int(score), int(total), datetime.date.today().isoformat()))
    conn.commit()
    conn.close()

def get_certifications(user_id):
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, provider, completion_date, credential_id FROM certifications WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "provider": r[2], "completion_date": r[3], "credential_id": r[4]} for r in rows]

def save_certification(user_id, name, provider, completion_date, credential_id):
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO certifications (user_id, name, provider, completion_date, credential_id)
    VALUES (?, ?, ?, ?, ?)
    """, (user_id, name, provider, completion_date, credential_id))
    conn.commit()
    conn.close()

def delete_certification(user_id, item_id):
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM certifications WHERE id=? AND user_id=?", (item_id, user_id))
    conn.commit()
    conn.close()

def get_planner_tasks(user_id):
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, task_text, completed FROM planner_tasks WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "task_text": r[1], "completed": bool(r[2])} for r in rows]

def save_planner_task(user_id, task_text):
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO planner_tasks (user_id, task_text, completed) VALUES (?, ?, 0)", (user_id, task_text))
    conn.commit()
    conn.close()

def delete_planner_task(user_id, item_id):
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM planner_tasks WHERE id=? AND user_id=?", (item_id, user_id))
    conn.commit()
    conn.close()

def toggle_planner_task(user_id, item_id, completed):
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE planner_tasks SET completed=? WHERE id=? AND user_id=?", (int(completed), item_id, user_id))
    conn.commit()
    conn.close()

def get_student_profile(user_id):
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    # First, get registration name
    cursor.execute("SELECT name FROM users WHERE id = ?", (user_id,))
    user_row = cursor.fetchone()
    name = user_row[0] if user_row else "Student"
    
    cursor.execute("SELECT college_name, degree, department, year_of_study, cgpa_percentage, skills, interested_roles, resume_filename, resume_bytes FROM student_profile WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            "user_id": user_id,
            "name": name,
            "college_name": row[0] or "",
            "degree": row[1] or "",
            "department": row[2] or "",
            "year_of_study": row[3] or "",
            "cgpa_percentage": row[4] or "",
            "skills": row[5] or "",
            "interested_roles": row[6] or "",
            "resume_filename": row[7] or "",
            "resume_bytes": row[8]
        }
    else:
        return {
            "user_id": user_id,
            "name": name,
            "college_name": "",
            "degree": "",
            "department": "",
            "year_of_study": "",
            "cgpa_percentage": "",
            "skills": "",
            "interested_roles": "",
            "resume_filename": "",
            "resume_bytes": None
        }

def save_student_profile(user_id, college_name, degree, department, year_of_study, cgpa_percentage, skills, interested_roles, resume_filename=None, resume_bytes=None):
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    if resume_filename is not None:
        cursor.execute("""
        INSERT OR REPLACE INTO student_profile (user_id, college_name, degree, department, year_of_study, cgpa_percentage, skills, interested_roles, resume_filename, resume_bytes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, college_name, degree, department, year_of_study, cgpa_percentage, skills, interested_roles, resume_filename, resume_bytes))
    else:
        # If resume is not uploaded/provided, keep the existing one in the DB (or don't overwrite if it was already uploaded)
        cursor.execute("SELECT resume_filename, resume_bytes FROM student_profile WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        existing_filename = row[0] if row else None
        existing_bytes = row[1] if row else None
        
        cursor.execute("""
        INSERT OR REPLACE INTO student_profile (user_id, college_name, degree, department, year_of_study, cgpa_percentage, skills, interested_roles, resume_filename, resume_bytes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, college_name, degree, department, year_of_study, cgpa_percentage, skills, interested_roles, existing_filename, existing_bytes))
    conn.commit()
    conn.close()

def delete_student_resume(user_id):
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE student_profile SET resume_filename = NULL, resume_bytes = NULL WHERE user_id = ?
    """, (user_id,))
    conn.commit()
    conn.close()
