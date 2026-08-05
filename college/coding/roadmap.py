from college.coding.database import get_roadmap_progress, save_roadmap_progress
from college.resume.database import get_resume

ROADMAP_STRUCTURE = {
    "Python": {
        "subtopics": ["Variables", "Loops", "Functions", "OOP", "File Handling", "Exception Handling", "Modules", "Libraries"],
        "hours_per_topic": 2
    },
    "DSA": {
        "subtopics": [
            "Arrays", "Strings", "Hashing", "Linked List", "Stack", "Queue", 
            "Tree", "BST", "Heap", "Graph", "Trie", "Dynamic Programming", 
            "Greedy", "Backtracking", "Bit Manipulation"
        ],
        "hours_per_topic": 4
    },
    "SQL": {
        "subtopics": ["Basics", "Joins", "Subqueries", "Normalization", "Indexes", "Transactions"],
        "hours_per_topic": 3
    },
    "Core CS": {
        "subtopics": ["DBMS", "Operating System", "Computer Networks", "OOP Concepts", "System Design Basics"],
        "hours_per_topic": 3
    }
}

CORE_PLACEMENT_SKILLS = [
    "Python",
    "SQL",
    "Git",
    "OOP Concepts",
    "Data Structures",
    "Algorithms",
    "APIs"
]

def get_resume_skill_gaps(user_id):
    """
    Fetches the user's resume and compares their listed skills against CORE_PLACEMENT_SKILLS.
    Returns a dictionary with current_skills, missing_skills, and completeness_score.
    """
    resume = get_resume(user_id)
    if not resume:
        return {
            "current_skills": [],
            "missing_skills": CORE_PLACEMENT_SKILLS,
            "completeness_score": 0,
            "project_count": 0
        }
        
    current_skills = resume.get("skills", [])
    # Case-insensitive comparison
    current_lower = [s.lower().strip() for s in current_skills]
    
    missing_skills = []
    for skill in CORE_PLACEMENT_SKILLS:
        # Match base names
        matched = False
        for s in current_lower:
            if s in skill.lower() or skill.lower() in s:
                matched = True
                break
        if not matched:
            missing_skills.append(skill)
            
    # Calculate completeness score based on filled fields in resume
    # Max possible fields = 8
    score_components = 0
    if resume.get("full_name"): score_components += 1
    if resume.get("email") or resume.get("phone"): score_components += 1
    if resume.get("college") or resume.get("degree"): score_components += 1
    if current_skills: score_components += 1
    if resume.get("experience"): score_components += 1
    if resume.get("projects"): score_components += 1
    if resume.get("certifications"): score_components += 1
    if resume.get("career_objective"): score_components += 1
    
    completeness_score = int((score_components / 8.0) * 100)
    project_count = len(resume.get("projects", []))
    
    return {
        "current_skills": current_skills,
        "missing_skills": missing_skills,
        "completeness_score": completeness_score,
        "project_count": project_count
    }

def get_roadmap_status(user_id):
    """
    Retrieves the roadmap subtopics list and determines if they are Locked, Unlocked, or Completed.
    Calculates estimated remaining times and overall completion percentage.
    """
    db_progress = get_roadmap_progress(user_id)
    status_map = {}
    
    total_subtopics = 0
    completed_subtopics = 0
    remaining_minutes = 0
    
    recommended_topics = []
    
    for category, cat_data in ROADMAP_STRUCTURE.items():
        subtopics = cat_data["subtopics"]
        hours = cat_data["hours_per_topic"]
        
        status_map[category] = []
        
        # In each category, sequential unlock logic is applied:
        # The first subtopic is always unlocked.
        # Subsequent subtopics are unlocked if the preceding one is completed.
        unlocked_found_for_cat = False
        
        for idx, sub in enumerate(subtopics):
            total_subtopics += 1
            is_completed = db_progress.get(category, {}).get(sub, {}).get("completed", False)
            
            if is_completed:
                status = "Completed"
                completed_subtopics += 1
            else:
                if idx == 0:
                    status = "Unlocked"
                else:
                    prev_sub = subtopics[idx - 1]
                    prev_completed = db_progress.get(category, {}).get(prev_sub, {}).get("completed", False)
                    if prev_completed:
                        status = "Unlocked"
                    else:
                        status = "Locked"
                
                remaining_minutes += hours * 60
                
                if status == "Unlocked" and not unlocked_found_for_cat:
                    recommended_topics.append({
                        "category": category,
                        "subtopic": sub,
                        "hours": hours
                    })
                    unlocked_found_for_cat = True
            
            status_map[category].append({
                "subtopic": sub,
                "status": status,
                "hours": hours,
                "completion_date": db_progress.get(category, {}).get(sub, {}).get("completion_date", "")
            })
            
    completion_pct = int((completed_subtopics / total_subtopics) * 100) if total_subtopics > 0 else 0
    
    return {
        "status_map": status_map,
        "completion_percentage": completion_pct,
        "completed_count": completed_subtopics,
        "total_count": total_subtopics,
        "remaining_minutes": remaining_minutes,
        "recommended_topics": recommended_topics
    }

def mark_subtopic_completed(user_id, category, subtopic, completed=True):
    """
    Saves a roadmap progress update to SQLite.
    """
    save_roadmap_progress(user_id, category, subtopic, completed)
