import streamlit as st
from professional.database import get_professional_profile, get_professional_skills, get_leadership_scores, get_applied_jobs, apply_to_job

def render_job_matching_section(user_id):
    st.subheader("9. Advanced Job Matching")
    st.caption("AI job matching algorithm aligning your experience, technical skills, leadership rating, domain, and salary expectations.")

    profile = get_professional_profile(user_id)
    skills = get_professional_skills(user_id)
    leadership = get_leadership_scores(user_id)
    applied_list = get_applied_jobs(user_id)

    lead_avg = int(sum(leadership.values()) / max(len(leadership), 1))

    user_skills_list = profile.get('skills', [])
    user_certs_list = profile.get('certifications', [])
    user_exp = profile.get('experience', 0)
    current_sal = float(profile.get('current_salary', 0.0))

    st.markdown("### Matching Factors Analyzed")
    st.markdown(f"""
    - **Experience Level:** {user_exp} Years  
    - **Technical Skills:** {', '.join(user_skills_list) if user_skills_list else 'None specified'}  
    - **Leadership Ability:** {lead_avg}% Index  
    - **Certifications:** {', '.join(user_certs_list) if user_certs_list else 'None specified'}  
    - **Salary Baseline:** ₹{current_sal:.1f} LPA
    """)

    st.divider()

    st.markdown("### Tailored Experienced Job Opportunities")

    # Calculate dynamic matches based on user skill scores starting at 0
    backend_score = skills.get('Backend Development', 0)
    sys_design_score = skills.get('System Design', 0)
    cloud_score = skills.get('Cloud Computing', 0)
    devops_score = skills.get('DevOps', 0)

    jobs = [
        {
            "role": "Senior Backend Engineer",
            "company": "CloudScale Systems",
            "match": min(99, int((backend_score * 0.6) + (sys_design_score * 0.3) + (min(user_exp, 5) * 2))),
            "location": "Remote / Bengaluru",
            "salary": "₹10 - ₹13 LPA",
            "skills": ["Python", "Django", "PostgreSQL", "REST APIs", "AWS"],
            "description": "Looking for experienced Python backend developer to build high-concurrency cloud endpoints."
        },
        {
            "role": "Backend Architect",
            "company": "FinTech Innovations",
            "match": min(99, int((sys_design_score * 0.7) + (backend_score * 0.2) + (min(user_exp, 5) * 2))),
            "location": "Hybrid (Mumbai / Remote)",
            "salary": "₹14 - ₹18 LPA",
            "skills": ["Python / Go", "System Design", "Kafka", "Microservices"],
            "description": "Architect scalable payment services with high uptime and distributed systems."
        },
        {
            "role": "Cloud Engineer",
            "company": "DevOps Solutions Corp",
            "match": min(99, int((cloud_score * 0.5) + (devops_score * 0.4) + (min(user_exp, 5) * 2))),
            "location": "Hyderabad / Remote",
            "salary": "₹11 - ₹15 LPA",
            "skills": ["AWS", "Docker", "Kubernetes", "CI/CD Pipelines"],
            "description": "Build automated infrastructure pipelines and manage container orchestration."
        },
        {
            "role": "Engineering Lead",
            "company": "Enterprise Tech Partners",
            "match": min(99, int((lead_avg * 0.6) + (sys_design_score * 0.3) + (min(user_exp, 5) * 2))),
            "location": "Bengaluru",
            "salary": "₹16 - ₹20 LPA",
            "skills": ["Team Leadership", "Backend Architecture", "Agile", "Mentorship"],
            "description": "Lead a squad of 6 engineers driving product innovation and backend reliability."
        }
    ]

    filter_match = st.slider("Filter by Minimum Match %", 0, 100, 0, step=5)


    for j in jobs:
        if j["match"] >= filter_match:
            job_key = f"{j['role']}@{j['company']}"
            is_applied = job_key in applied_list

            with st.container(border=True):
                c1, c2 = st.columns([3, 1], vertical_alignment="center")
                with c1:
                    st.markdown(f"#### {j['role']} -- *{j['company']}*")
                    st.caption(f"Location: {j['location']} | Salary: {j['salary']}")
                    st.write(j["description"])
                    st.write(f"**Required Tags:** {', '.join(j['skills'])}")
                with c2:
                    st.metric("Match Score", f"{j['match']}%")
                    if is_applied:
                        st.info("Application Submitted", icon="✔")
                    else:
                        if st.button("Apply Now", key=f"job_apply_{j['role']}_{j['company']}", use_container_width=True):
                            apply_to_job(user_id, j['role'], j['company'])
                            st.balloons()
                            st.success(f"Application sent for {j['role']} at {j['company']}!")
                            st.rerun()

