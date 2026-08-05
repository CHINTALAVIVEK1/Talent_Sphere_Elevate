import streamlit as st
import json
from google.genai import types
from utils.gemini import client
from college.coding.database import get_student_profile
from college.resume.database import get_resume

def analyze_skill_gaps_ai(skills_unique, resume_text, target_role):
    """
    Calls Gemini API to evaluate student skills specifically against 5 required skill categories.
    """
    prompt = f"""
    You are an expert AI Career Coach.
    Perform a Skill Gap Analysis for a student targeting the role: '{target_role}'.
    
    Evaluate the student's skills specifically against these 5 required skill categories:
    1. 'Core Programming (Python/Java/JavaScript)'
    2. 'Data Structures & Algorithms'
    3. 'Version Control (Git/GitHub)'
    4. 'Databases (SQL/NoSQL)'
    5. 'Web Development Frameworks/Libraries'
    
    The student's current skills are: {skills_unique}
    Their resume details are:
    {resume_text}
    
    For each of the 5 categories, determine if the status is:
    - 'Available' (if they have matching programming skills/experience)
    - 'Missing' (if they don't have skills matching this category)
    
    Also, generate 3 to 5 actionable, specific AI Recommendations to bridge any gaps.
    
    You MUST return a JSON object with the following fields:
    - target_role (String)
    - skills (List of JSON objects, each with 'skill' (exact category name) and 'status' ('Available' or 'Missing'))
    - recommendations (List of Strings)
    
    Do not wrap in any markdown formatting. Return ONLY the raw JSON string.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2
            )
        )
        return json.loads(response.text.strip())
    except Exception as e:
        print(f"Error in analyze_skill_gaps_ai: {e}")
        return None

def fallback_skill_gap_analysis(skills_unique, target_role):
    """
    Provides fallback matching logic for the exact 5 categories.
    """
    skills_lower = [s.lower().strip() for s in skills_unique]
    
    categories = [
        "Core Programming (Python/Java/JavaScript)",
        "Data Structures & Algorithms",
        "Version Control (Git/GitHub)",
        "Databases (SQL/NoSQL)",
        "Web Development Frameworks/Libraries"
    ]
    
    # Define matching keywords for each category
    matching_keywords = {
        "Core Programming (Python/Java/JavaScript)": [
            "python", "java", "javascript", "js", "c++", "cpp", "c", "c#", "ruby", "go", "golang", 
            "swift", "kotlin", "rust", "typescript", "ts", "php", "programming", "coding"
        ],
        "Data Structures & Algorithms": [
            "dsa", "data structures", "algorithms", "data structure", "algorithm", 
            "problem solving", "competitive coding", "leetcode", "trees", "graphs"
        ],
        "Version Control (Git/GitHub)": [
            "git", "github", "version control", "gitlab", "bitbucket"
        ],
        "Databases (SQL/NoSQL)": [
            "sql", "nosql", "mysql", "sqlite", "mongodb", "postgresql", "postgres", 
            "oracle", "redis", "dbms", "database", "databases", "cassandra", "firebase"
        ],
        "Web Development Frameworks/Libraries": [
            "react", "angular", "vue", "django", "flask", "node", "express", "spring", 
            "asp.net", "laravel", "html", "css", "bootstrap", "tailwind", "jquery", 
            "web dev", "web development", "nextjs", "next.js"
        ]
    }
    
    skills_status = []
    for category in categories:
        keywords = matching_keywords[category]
        is_matched = False
        for user_skill in skills_lower:
            for kw in keywords:
                if kw in user_skill or user_skill in kw:
                    is_matched = True
                    break
            if is_matched:
                break
                
        status = "Available" if is_matched else "Missing"
        skills_status.append({"skill": category, "status": status})
        
    # Recommendations
    recs = []
    missing_categories = [item["skill"] for item in skills_status if item["status"] == "Missing"]
    
    if "Core Programming (Python/Java/JavaScript)" in missing_categories:
        recs.append("Learn Core Programming fundamentals (Python, Java, or JavaScript)")
    if "Data Structures & Algorithms" in missing_categories:
        recs.append("Practice Data Structures daily")
    if "Version Control (Git/GitHub)" in missing_categories:
        recs.append("Use GitHub regularly")
    if "Databases (SQL/NoSQL)" in missing_categories:
        recs.append("Learn SQL fundamentals and build database projects")
    if "Web Development Frameworks/Libraries" in missing_categories:
        recs.append("Build one full-stack web application project")
        
    # Default fallback recs if nothing is missing
    if not recs:
        recs.append("Advance your web framework skills and build larger scale apps")
        recs.append("Contribute to open-source Git repositories")
        recs.append("Optimize algorithmic complexity in mock design interviews")
        
    return {
        "target_role": target_role,
        "skills": skills_status,
        "recommendations": recs
    }

def render_skill_gap_analysis(user_id):
    st.subheader("🧠 Skill Gap Analysis")
    st.write("Evaluate your skills against your target career path and receive actionable AI recommendations.")
    
    # Target Role Selection
    if "target_role" not in st.session_state:
        st.session_state.target_role = "Software Developer"
        
    target_role = st.selectbox(
        "Target Role",
        ["Software Developer", "Data Analyst", "Frontend Developer", "Backend Developer"],
        index=["Software Developer", "Data Analyst", "Frontend Developer", "Backend Developer"].index(st.session_state.target_role),
        key="target_role_select"
    )
    
    if target_role != st.session_state.target_role:
        st.session_state.target_role = target_role
        st.rerun()
        
    # Get user skills & resume
    profile = get_student_profile(user_id)
    resume = get_resume(user_id)
    
    skills_list = []
    if profile and profile.get("skills"):
        skills_list.extend([s.strip().lower() for s in profile["skills"].split(",") if s.strip()])
    if resume and resume.get("skills"):
        skills_list.extend([s.strip().lower() for s in resume["skills"]])
        
    skills_unique = list(set(skills_list))
    
    # Get resume text for AI context
    resume_text = ""
    if resume:
        resume_text = f"Objective: {resume.get('career_objective')}\n"
        resume_text += f"Projects: {json.dumps(resume.get('projects'))}\n"
        resume_text += f"Certifications: {json.dumps(resume.get('certifications'))}\n"
        
    # Fetch/Generate Gap Analysis
    analysis = None
    
    with st.spinner("Analyzing skill gaps..."):
        analysis = analyze_skill_gaps_ai(skills_unique, resume_text, target_role)
        
    # Fallback if AI fails
    if not analysis or "skills" not in analysis or "recommendations" not in analysis:
        analysis = fallback_skill_gap_analysis(skills_unique, target_role)
        
    # Render table of skills
    table_rows = ""
    for item in analysis["skills"]:
        skill_name = item["skill"]
        status = item["status"]
        
        # Color badges
        if status == "Available":
            badge_html = '<span style="background-color: #d1fae5; color: #065f46; padding: 4px 10px; border-radius: 9999px; font-size: 13px; font-weight: 600;">Available</span>'
        else: # Missing
            badge_html = '<span style="background-color: #fee2e2; color: #991b1b; padding: 4px 10px; border-radius: 9999px; font-size: 13px; font-weight: 600;">Missing</span>'
            
        table_rows += f"""<tr style="border-bottom: 1px solid #f1f5f9;"><td style="padding: 12px 10px; font-weight: 500; color: #374151;">{skill_name}</td><td style="padding: 12px 10px;">{badge_html}</td></tr>"""
        
    table_html = f"""<div style="background-color: #ffffff; padding: 10px 15px; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 20px;"><table style="width: 100%; border-collapse: collapse; font-family: sans-serif; font-size: 14px; text-align: left;"><thead><tr style="border-bottom: 2px solid #e2e8f0; background-color: #f8fafc;"><th style="padding: 10px; font-weight: 600; color: #475569; width: 60%;">Required Skill</th><th style="padding: 10px; font-weight: 600; color: #475569;">Status</th></tr></thead><tbody>{table_rows}</tbody></table></div>"""
    st.markdown(table_html, unsafe_allow_html=True)
    
    # Render Recommendations
    st.write("##### AI Recommendation:")
    recs_list = analysis["recommendations"]
    recs_html = "".join([f"<li style='margin-bottom: 8px; color: #374151;'>{r}</li>" for r in recs_list])
    
    recs_container = f"""<div style="background-color: #f0fdf4; border-left: 4px solid #16a34a; padding: 15px 20px; border-radius: 0 12px 12px 0; font-family: sans-serif; font-size: 14px; margin-bottom: 15px;"><ul style="margin: 0; padding-left: 20px;">{recs_html}</ul></div>"""
    st.markdown(recs_container, unsafe_allow_html=True)
