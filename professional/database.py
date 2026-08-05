import sqlite3
import json

DB_PATH = "database.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_professional_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Table for professional profile
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS professional_profiles (
        user_id INTEGER PRIMARY KEY,
        company TEXT,
        current_role TEXT,
        experience INTEGER,
        current_salary REAL,
        skills TEXT,
        leadership_exp TEXT,
        certifications TEXT,
        career_goals TEXT,
        preferred_roles TEXT
    )
    """)

    # Table for professional skill scores
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS professional_skills (
        user_id INTEGER PRIMARY KEY,
        backend INTEGER,
        system_design INTEGER,
        cloud INTEGER,
        devops INTEGER,
        leadership INTEGER
    )
    """)

    # Table for leadership evaluation scores
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS professional_leadership (
        user_id INTEGER PRIMARY KEY,
        team_coordination INTEGER,
        mentoring INTEGER,
        decision_making INTEGER,
        conflict_resolution INTEGER,
        project_ownership INTEGER
    )
    """)

    # Table for certification tracking
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS professional_cert_status (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        cert_name TEXT,
        status TEXT,
        priority TEXT,
        UNIQUE(user_id, cert_name)
    )
    """)

    # Table for roadmap task progress
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS professional_roadmap_tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        task_key TEXT,
        completed INTEGER,
        UNIQUE(user_id, task_key)
    )
    """)

    # Table for job application tracking
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS professional_job_applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        job_role TEXT,
        company TEXT,
        applied_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, job_role, company)
    )
    """)

    conn.commit()

    # Always UPSERT demo data for user_id 3 (Professional Demo) so stale rows get fixed
    demo_ids = [3]
    demo_profile = (
        "TechCorp Solutions",
        "Software Developer",
        4,
        6.0,
        json.dumps(["Python", "Django", "REST API", "SQL", "Git"]),
        "Led 3 junior developers in core backend overhaul & API refactoring",
        json.dumps(["AWS Cloud Practitioner"]),
        "Become Senior Backend Engineer & Cloud Architect",
        json.dumps(["Senior Backend Engineer", "Backend Architect", "Cloud Engineer"])
    )
    for d_id in demo_ids:
        cursor.execute("""
        INSERT INTO professional_profiles (user_id, company, current_role, experience, current_salary, skills, leadership_exp, certifications, career_goals, preferred_roles)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            company=excluded.company,
            current_role=excluded.current_role,
            experience=excluded.experience,
            current_salary=excluded.current_salary,
            skills=excluded.skills,
            leadership_exp=excluded.leadership_exp,
            certifications=excluded.certifications,
            career_goals=excluded.career_goals,
            preferred_roles=excluded.preferred_roles
        """, (d_id,) + demo_profile)

        cursor.execute("""
        INSERT INTO professional_skills (user_id, backend, system_design, cloud, devops, leadership)
        VALUES (?, 88, 72, 55, 48, 70)
        ON CONFLICT(user_id) DO UPDATE SET
            backend=88, system_design=72, cloud=55, devops=48, leadership=70
        """, (d_id,))

        cursor.execute("""
        INSERT INTO professional_leadership (user_id, team_coordination, mentoring, decision_making, conflict_resolution, project_ownership)
        VALUES (?, 78, 72, 80, 65, 75)
        ON CONFLICT(user_id) DO UPDATE SET
            team_coordination=78, mentoring=72, decision_making=80, conflict_resolution=65, project_ownership=75
        """, (d_id,))

        default_certs = [
            ("AWS Solutions Architect", "In Progress", "High"),
            ("Docker Certified Associate", "Wishlist", "High"),
            ("Kubernetes Administrator", "Wishlist", "Medium"),
            ("System Design Fundamentals", "Completed", "Medium")
        ]
        for cname, cstat, cprio in default_certs:
            cursor.execute("""
            INSERT INTO professional_cert_status (user_id, cert_name, status, priority)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id, cert_name) DO NOTHING
            """, (d_id, cname, cstat, cprio))

    conn.commit()
    conn.close()

# Initialize tables immediately on import
init_professional_db()

def seed_default_profile(user_id):
    if not user_id:
        user_id = 0
    save_professional_profile(user_id, {
        "company": "TechCorp Solutions",
        "current_role": "Software Developer",
        "experience": 4,
        "current_salary": 6.0,
        "skills": ["Python", "Django", "REST API", "SQL", "Git"],
        "leadership_exp": "Led 3 junior developers in core backend overhaul & API refactoring",
        "certifications": ["AWS Cloud Practitioner"],
        "career_goals": "Become Senior Backend Engineer & Cloud Architect",
        "preferred_roles": ["Senior Backend Engineer", "Backend Architect", "Cloud Engineer"]
    })
    save_professional_skills(user_id, {
        "Backend Development": 88,
        "System Design": 72,
        "Cloud Computing": 55,
        "DevOps": 48,
        "Leadership": 70
    })
    save_leadership_scores(user_id, {
        "Team Coordination": 78,
        "Mentoring": 72,
        "Decision Making": 80,
        "Conflict Resolution": 65,
        "Project Ownership": 75
    })
    update_cert_status(user_id, "AWS Solutions Architect", "In Progress", "High")
    update_cert_status(user_id, "Docker Certified Associate", "Wishlist", "High")
    update_cert_status(user_id, "Kubernetes Administrator", "Wishlist", "Medium")
    update_cert_status(user_id, "System Design Fundamentals", "Completed", "Medium")


def get_professional_profile(user_id):
    if not user_id:
        user_id = 0
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM professional_profiles WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "company": row["company"] or "",
            "current_role": row["current_role"] or "Not Set",
            "experience": row["experience"] or 0,
            "current_salary": row["current_salary"] or 0.0,
            "skills": json.loads(row["skills"]) if row["skills"] else [],
            "leadership_exp": row["leadership_exp"] or "",
            "certifications": json.loads(row["certifications"]) if row["certifications"] else [],
            "career_goals": row["career_goals"] or "",
            "preferred_roles": json.loads(row["preferred_roles"]) if row["preferred_roles"] else []
        }
    else:
        # Default fresh profile starting at 0
        return {
            "company": "",
            "current_role": "Not Set",
            "experience": 0,
            "current_salary": 0.0,
            "skills": [],
            "leadership_exp": "",
            "certifications": [],
            "career_goals": "",
            "preferred_roles": []
        }

def save_professional_profile(user_id, profile_dict):
    if not user_id:
        user_id = 0
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO professional_profiles (user_id, company, current_role, experience, current_salary, skills, leadership_exp, certifications, career_goals, preferred_roles)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(user_id) DO UPDATE SET
        company=excluded.company,
        current_role=excluded.current_role,
        experience=excluded.experience,
        current_salary=excluded.current_salary,
        skills=excluded.skills,
        leadership_exp=excluded.leadership_exp,
        certifications=excluded.certifications,
        career_goals=excluded.career_goals,
        preferred_roles=excluded.preferred_roles
    """, (
        user_id,
        profile_dict["company"],
        profile_dict["current_role"],
        profile_dict["experience"],
        profile_dict.get("current_salary", 0.0),
        json.dumps(profile_dict["skills"]),
        profile_dict["leadership_exp"],
        json.dumps(profile_dict["certifications"]),
        profile_dict["career_goals"],
        json.dumps(profile_dict["preferred_roles"])
    ))
    conn.commit()
    conn.close()

def get_professional_skills(user_id):
    if not user_id:
        user_id = 0
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM professional_skills WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "Backend Development": row["backend"] or 0,
            "System Design": row["system_design"] or 0,
            "Cloud Computing": row["cloud"] or 0,
            "DevOps": row["devops"] or 0,
            "Leadership": row["leadership"] or 0
        }
    else:
        # Default fresh skill scores starting at 0
        return {
            "Backend Development": 0,
            "System Design": 0,
            "Cloud Computing": 0,
            "DevOps": 0,
            "Leadership": 0
        }

def save_professional_skills(user_id, skills_dict):
    if not user_id:
        user_id = 0
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO professional_skills (user_id, backend, system_design, cloud, devops, leadership)
    VALUES (?, ?, ?, ?, ?, ?)
    ON CONFLICT(user_id) DO UPDATE SET
        backend=excluded.backend,
        system_design=excluded.system_design,
        cloud=excluded.cloud,
        devops=excluded.devops,
        leadership=excluded.leadership
    """, (
        user_id,
        skills_dict.get("Backend Development", 0),
        skills_dict.get("System Design", 0),
        skills_dict.get("Cloud Computing", 0),
        skills_dict.get("DevOps", 0),
        skills_dict.get("Leadership", 0)
    ))
    conn.commit()
    conn.close()

def get_leadership_scores(user_id):
    if not user_id:
        user_id = 0
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM professional_leadership WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "Team Coordination": row["team_coordination"] or 0,
            "Mentoring": row["mentoring"] or 0,
            "Decision Making": row["decision_making"] or 0,
            "Conflict Resolution": row["conflict_resolution"] or 0,
            "Project Ownership": row["project_ownership"] or 0
        }
    else:
        # Default fresh leadership scores starting at 0
        return {
            "Team Coordination": 0,
            "Mentoring": 0,
            "Decision Making": 0,
            "Conflict Resolution": 0,
            "Project Ownership": 0
        }

def save_leadership_scores(user_id, scores_dict):
    if not user_id:
        user_id = 0
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO professional_leadership (user_id, team_coordination, mentoring, decision_making, conflict_resolution, project_ownership)
    VALUES (?, ?, ?, ?, ?, ?)
    ON CONFLICT(user_id) DO UPDATE SET
        team_coordination=excluded.team_coordination,
        mentoring=excluded.mentoring,
        decision_making=excluded.decision_making,
        conflict_resolution=excluded.conflict_resolution,
        project_ownership=excluded.project_ownership
    """, (
        user_id,
        scores_dict.get("Team Coordination", 0),
        scores_dict.get("Mentoring", 0),
        scores_dict.get("Decision Making", 0),
        scores_dict.get("Conflict Resolution", 0),
        scores_dict.get("Project Ownership", 0)
    ))
    conn.commit()
    conn.close()

def get_certification_status(user_id):
    if not user_id:
        user_id = 0
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT cert_name, status, priority FROM professional_cert_status WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()

    default_certs = [
        {"cert_name": "AWS Solutions Architect", "status": "Not Started", "priority": "High"},
        {"cert_name": "Docker Certified Associate", "status": "Not Started", "priority": "High"},
        {"cert_name": "Kubernetes Administrator", "status": "Not Started", "priority": "Medium"},
        {"cert_name": "System Design Fundamentals", "status": "Not Started", "priority": "Medium"}
    ]

    if not rows:
        return default_certs

    db_map = {row["cert_name"]: {"status": row["status"], "priority": row["priority"]} for row in rows}
    result = []
    for default in default_certs:
        cname = default["cert_name"]
        if cname in db_map:
            result.append({"cert_name": cname, "status": db_map[cname]["status"], "priority": db_map[cname]["priority"]})
        else:
            result.append(default)
    return result


def update_cert_status(user_id, cert_name, status, priority="High"):
    if not user_id:
        user_id = 0
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO professional_cert_status (user_id, cert_name, status, priority)
    VALUES (?, ?, ?, ?)
    ON CONFLICT(user_id, cert_name) DO UPDATE SET status=excluded.status
    """, (user_id, cert_name, status, priority))
    conn.commit()
    conn.close()

def get_roadmap_tasks_status(user_id):
    if not user_id:
        user_id = 0
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT task_key, completed FROM professional_roadmap_tasks WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return {row["task_key"]: bool(row["completed"]) for row in rows}

def update_roadmap_task_status(user_id, task_key, completed):
    if not user_id:
        user_id = 0
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO professional_roadmap_tasks (user_id, task_key, completed)
    VALUES (?, ?, ?)
    ON CONFLICT(user_id, task_key) DO UPDATE SET completed=excluded.completed
    """, (user_id, task_key, 1 if completed else 0))
    conn.commit()
    conn.close()

def get_applied_jobs(user_id):
    if not user_id:
        user_id = 0
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT job_role, company FROM professional_job_applications WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [f"{row['job_role']}@{row['company']}" for row in rows]

def apply_to_job(user_id, job_role, company):
    if not user_id:
        user_id = 0
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO professional_job_applications (user_id, job_role, company)
    VALUES (?, ?, ?)
    ON CONFLICT(user_id, job_role, company) DO NOTHING
    """, (user_id, job_role, company))
    conn.commit()
    conn.close()

