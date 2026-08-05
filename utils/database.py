import sqlite3

DB_PATH = "database.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_user_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        category TEXT
    )
    """)

    demo_users = [
        ("High School Demo", "school@demo.com", "demo123", "High School Student"),
        ("College Demo", "college@demo.com", "demo123", "College Student"),
        ("Professional Demo", "professional@demo.com", "demo123", "Working Professional"),
        ("Admin Demo", "admin@demo.com", "admin123", "Admin")
    ]

    for user in demo_users:
        try:
            cursor.execute(
                "INSERT INTO users(name,email,password,category) VALUES(?,?,?,?)",
                user
            )
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()

# Run initialization on import
init_user_db()

def authenticate_user(email, password):
    if not email or not password:
        return None
    clean_email = email.strip().lower()
    clean_password = password.strip()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, email, category FROM users WHERE LOWER(TRIM(email)) = ? AND password = ?",
        (clean_email, clean_password)
    )
    user = cursor.fetchone()
    conn.close()
    return user

def register_new_user(name, email, password, category):
    if not name or not email or not password or not category:
        return False, "Please fill in all the required fields."

    clean_name = name.strip()
    clean_email = email.strip().lower()
    clean_password = password.strip()

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users(name, email, password, category) VALUES(?, ?, ?, ?)",
            (clean_name, clean_email, clean_password, category)
        )
        conn.commit()
        conn.close()
        return True, "Account created successfully!"
    except sqlite3.IntegrityError:
        conn.close()
        return False, "This email address is already registered. Please log in or use a different email."
    except Exception as e:
        conn.close()
        return False, f"An unexpected error occurred: {e}"