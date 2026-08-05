import streamlit as st
from professional.database import get_professional_profile, get_professional_skills, get_leadership_scores

def render_readiness_section(user_id):
    st.subheader("4. Promotion Readiness Analysis")
    st.caption("Comprehensive evaluation of key factors determining promotion readiness into senior/lead positions.")

    profile = get_professional_profile(user_id)
    skills = get_professional_skills(user_id)
    leadership = get_leadership_scores(user_id)

    exp = profile.get("experience", 0)
    backend_score = skills.get("Backend Development", 0)
    sys_design_score = skills.get("System Design", 0)
    tech_readiness = int((backend_score + sys_design_score) / 2)
    lead_readiness = int(sum(leadership.values()) / max(len(leadership), 1))
    
    if tech_readiness == 0 and lead_readiness == 0 and exp == 0:
        comm_readiness = 0
        overall_readiness = 0
    else:
        comm_readiness = 76
        overall_readiness = int((tech_readiness * 0.45) + (lead_readiness * 0.35) + (comm_readiness * 0.20))

    st.markdown("### Promotion Readiness Breakdown")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Overall Promotion Readiness", f"{overall_readiness}%")
    col2.metric("Technical Readiness", f"{tech_readiness}%")
    col3.metric("Leadership Readiness", f"{lead_readiness}%")
    col4.metric("Communication Readiness", f"{comm_readiness}%")

    st.divider()

    st.markdown("### Evaluated Promotion Criteria")

    exp_score = min(100, exp * 22)
    exp_eval = "Pass (4+ Yrs optimal for Senior tier)" if exp >= 4 else "Building experience base"

    factors = [
        {"factor": "Years of Experience", "status": f"{exp} Years", "evaluation": exp_eval, "score": exp_score},
        {"factor": "Technical Expertise", "status": f"Backend ({backend_score}%)", "evaluation": "Core programming & API architecture domain proficiency", "score": tech_readiness},
        {"factor": "Project Complexity", "status": f"System Design ({sys_design_score}%)", "evaluation": "Demonstrated full lifecycle system delivery & scalable design", "score": sys_design_score},
        {"factor": "Leadership Exposure", "status": f"Leadership Index ({lead_readiness}%)", "evaluation": profile.get("leadership_exp", "") or "No leadership history logged", "score": lead_readiness},
        {"factor": "Communication Skills", "status": "Cross-team Collaboration", "evaluation": "Effective technical presentation & architecture documentation", "score": comm_readiness},
        {"factor": "Team Contributions", "status": f"Mentoring ({leadership.get('Mentoring', 0)}%)", "evaluation": "Consistent peer mentorship and code review approvals", "score": leadership.get("Mentoring", 0)}
    ]

    for f in factors:
        with st.container(border=True):
            c1, c2 = st.columns([4, 1])
            with c1:
                st.write(f"**{f['factor']}**: `{f['status']}` — *{f['evaluation']}*")
            with c2:
                st.progress(f["score"] / 100.0)

    st.divider()
    st.markdown("### AI Promotion Preparation Advice")
    if overall_readiness >= 75:
        st.success(f"**Ready for Promotion Discussion:** You are currently at **{overall_readiness}% Promotion Readiness**. Highlight your recent system redesign project and Cloud/Kubernetes learnings in your next quarterly review.")
    elif overall_readiness > 0:
        st.warning(f"Your current readiness is **{overall_readiness}%**. Focus on improving leadership exposure and completing Cloud certifications to reach 75%+ promotion readiness.")
    else:
        st.info("Complete your Professional Profile and Skill Assessment to generate your AI promotion preparation analysis.")


