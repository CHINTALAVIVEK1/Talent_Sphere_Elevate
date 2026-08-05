import streamlit as st
import datetime
from college.resume.resume_builder import resume_builder
from college.coding.coding_hub import coding_hub
from college.aptitude.aptitude import aptitude_practice
from college.interview.interview import mock_interview
from college.certifications.certifications import certifications_track
from college.planner.planner import daily_planner
from college.mentor.mentor import career_mentor
from college.profile.profile import student_profile_tab
from college.profile.gap_analysis import render_skill_gap_analysis
from utils.report import generate_college_report

from college.coding.database import (
    get_coding_progress,
    get_leetcode_progress,
    get_interview_progress,
    get_planner_tasks,
    toggle_planner_task,
    get_certifications,
    get_aptitude_scores
)
from college.coding.roadmap import get_resume_skill_gaps, get_roadmap_status
from college.resume.database import get_resume
from college.coding.leetcode import CHALLENGES
from college.coding.interview_bank import INTERVIEW_QUESTIONS

st.set_page_config(page_title="College Dashboard", layout="wide")

st.markdown("""
<style>
[data-testid="stSidebarNav"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

if not st.session_state.get("logged_in"):
    st.warning("Please login first.")
    if st.button("Go to Login Page"):
        st.switch_page("pages/Login.py")
    st.stop()

user = st.session_state.get("user_name", "Student")
user_id = st.session_state.get("user_id")

college_modules = [
    "home",
    "gap_analysis",
    "resume",
    "coding",
    "aptitude",
    "interview",
    "certifications",
    "planner",
    "mentor"
]

if (
    "module" not in st.session_state
    or st.session_state.module not in college_modules
):
    st.session_state.module = "home"
    
with st.sidebar:
    st.image("assets/logo.png", width=70)
    st.markdown("## College")
    st.divider()
    buttons = [
        (" Dashboard", "home"),
        (" Resume Builder", "resume"),
        (" Skill Gap Analysis", "gap_analysis"),
        (" Coding Hub", "coding"),
        (" Aptitude Practice", "aptitude"),
        (" Mock Interview", "interview"),
        (" Certifications", "certifications"),
        (" Daily Planner", "planner"),
        (" Mentor", "mentor"),
    ]
    for t, k in buttons:
        if st.button(t, use_container_width=True):
            st.session_state.module = k
            st.rerun()
    st.divider()
    if st.button("Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("app.py")

c1, c2 = st.columns([1, 6])
with c1:
    st.image("assets/logo.png", width=90)
with c2:
    st.title("TalentSphere Elevate")
    st.caption("College Student Dashboard")

st.divider()

if st.session_state.module == "home":
    # Pre-load planner tasks and certs for report variables
    tasks = get_planner_tasks(user_id)
    certs = get_certifications(user_id)
    gaps = get_resume_skill_gaps(user_id)
    resume = get_resume(user_id)
    project_count = len(resume.get("projects", [])) if resume else 0
    
    resume_score = st.session_state.get("ats_analysis", {}).get("overall_score")
    if resume_score is None:
        resume_score = gaps["completeness_score"]
        
    local_leetcode = get_leetcode_progress(user_id)
    solved_count = sum(1 for p in local_leetcode.values() if p["status"] == "Solved")
    total_challenges = len(CHALLENGES)
    coding_pct = int((solved_count / total_challenges) * 100) if total_challenges > 0 else 0
    
    int_qs = get_interview_progress(user_id)
    completed_int = sum(1 for status in int_qs.values() if status["completed"])
    total_int = len(INTERVIEW_QUESTIONS)
    int_pct = int((completed_int / total_int) * 100) if total_int > 0 else 0
    
    roadmap_status = get_roadmap_status(user_id)
    roadmap_comp_pct = roadmap_status["completion_percentage"]
    
    coding_readiness_val = min(100, int((coding_pct * 0.7) + (roadmap_comp_pct * 0.3)))
    interview_readiness_val = min(100, int((int_pct * 0.6) + (coding_readiness_val * 0.4)))
    career_readiness_val = min(100, int((resume_score * 0.4) + (coding_readiness_val * 0.4) + (interview_readiness_val * 0.2)))

    col_welcome, col_download = st.columns([4, 2], vertical_alignment="center")
    with col_welcome:
        st.subheader(f"Welcome, {user}")
    with col_download:
        completed_tasks = sum(1 for t in tasks if t["completed"])
        cert_count = len(certs)
        try:
            report_file = generate_college_report(
                user_name=user,
                career_readiness=career_readiness_val,
                coding_progress=coding_readiness_val,
                resume_score=resume_score,
                project_count=project_count,
                missing_skills=gaps["missing_skills"],
                completed_tasks_count=completed_tasks,
                cert_count=cert_count
            )
            with open(report_file, "rb") as f:
                pdf_data = f.read()
            st.download_button(
                label="Download Performance Sheet",
                data=pdf_data,
                file_name=f"{user}_College_Performance_Report.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.error("Could not compile performance report sheet.")
    
    a, b, c, d = st.columns(4)
    a.metric("Career Readiness", f"{career_readiness_val}%")
    b.metric("Coding Progress", f"{coding_readiness_val}%")
    c.metric("Resume Score", f"{resume_score}")
    d.metric("Projects", f"{project_count}")
    
    st.divider()
    
    # Render Student Profile form directly on the main dashboard home page
    student_profile_tab()
    
    st.divider()
    
    # Active Planner checklist tasks
    st.subheader("Today's Tasks")
    tasks = get_planner_tasks(user_id)
    if not tasks:
        # Save standard defaults
        default_tasks = [
            "Complete 2 LeetCode practice problems",
            "Update Resume skill tags inside Resume Builder",
            "Take 1 Aptitude Logical Reasoning quiz"
        ]
        for t in default_tasks:
            from college.coding.database import save_planner_task
            save_planner_task(user_id, t)
        tasks = get_planner_tasks(user_id)
        
    for task in tasks:
        t_id = task["id"]
        checked = st.checkbox(task["task_text"], value=task["completed"], key=f"home_task_{t_id}")
        if checked != task["completed"]:
            toggle_planner_task(user_id, t_id, checked)
            st.rerun()
            
    st.divider()
    
    # Recommendations
    st.subheader("Career Recommendation")
    if gaps["missing_skills"]:
        missing_skills_str = ", ".join(gaps["missing_skills"])
        st.info(f"Recommended Next Target: Address Gaps in {gaps['missing_skills'][0]}\n\nRequired Skills to study:\n• {missing_skills_str.replace(', ', chr(10) + '• ')}")
    else:
        st.success("Recommended Target: Full Stack Developer\n\nAll core skills met. Start preparing for mock system design interviews.")
        
    st.divider()
    
    # Recent Activities
    st.subheader("Recent Activities")
    activities = []
    
    # Add logged certifications
    certs = get_certifications(user_id)
    for cert in certs[:2]:
        activities.append(f"Completed and logged {cert['name']} from {cert['provider']}")
        
    # Add logged aptitude scores
    apt_scores = get_aptitude_scores(user_id)
    for s in apt_scores[:2]:
        activities.append(f"Attempted {s['category']} quiz (Score: {s['score']}/{s['total']})")
        
    # Standard fallbacks
    if not activities:
        activities = ["Profile Created", "Dashboard Initialized", "Career Planner Ready"]
        
    for act in activities:
        st.write("•", act)

# Profile is rendered directly on dashboard home, no extra dispatch needed
elif st.session_state.module == "gap_analysis":
    render_skill_gap_analysis(user_id)
elif st.session_state.module == "resume":
    resume_builder()
elif st.session_state.module == "coding":
    coding_hub()
elif st.session_state.module == "aptitude":
    aptitude_practice()
elif st.session_state.module == "interview":
    mock_interview()
elif st.session_state.module == "certifications":
    certifications_track()
elif st.session_state.module == "planner":
    daily_planner()
elif st.session_state.module == "mentor":
    career_mentor()
