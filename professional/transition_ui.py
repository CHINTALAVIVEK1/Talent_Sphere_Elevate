import streamlit as st
from professional.database import get_professional_profile, get_professional_skills

def render_transition_section(user_id):
    st.subheader("3. AI Career Transition Suggestions")
    st.caption("Based on your experience level and technical skills, the AI recommends next-level career trajectories.")

    profile = get_professional_profile(user_id)
    skills = get_professional_skills(user_id)

    exp = profile.get('experience', 0)
    backend_score = skills.get('Backend Development', 0)
    sys_design_score = skills.get('System Design', 0)
    cloud_score = skills.get('Cloud Computing', 0)
    devops_score = skills.get('DevOps', 0)
    lead_score = skills.get('Leadership', 0)

    has_data = any([exp, backend_score, sys_design_score, cloud_score, devops_score, lead_score])

    if not has_data:
        sr_backend_match = 0
        architect_match = 0
        cloud_match = 0
        eng_lead_match = 0
    else:
        sr_backend_match = min(99, max(0, int((backend_score * 0.5) + (sys_design_score * 0.3) + (min(exp, 10) * 3))))
        architect_match = min(99, max(0, int((sys_design_score * 0.55) + (backend_score * 0.25) + (cloud_score * 0.2))))
        cloud_match = min(99, max(0, int((cloud_score * 0.5) + (devops_score * 0.3) + (backend_score * 0.2))))
        eng_lead_match = min(99, max(0, int((lead_score * 0.55) + (sys_design_score * 0.25) + (min(exp, 10) * 2.5))))

    st.info(f"**Current Role:** {profile.get('current_role', 'Not Set')} | **Experience:** {exp} Years | **Current Salary:** ₹{profile.get('current_salary', 0.0):.1f} LPA")


    st.markdown("### Recommended Career Paths")

    transitions = [
        {
            "role": "Senior Backend Engineer",
            "match": sr_backend_match,
            "required": ["Advanced Microservices", "High Throughput API Design", "Cloud Infrastructure Basics"],
            "description": f"Natural progression leveraging your {backend_score}% Backend Development score and {exp} yrs experience."
        },
        {
            "role": "Backend Architect",
            "match": architect_match,
            "required": ["System Architecture", "Distributed Databases", "Fault-tolerant Design"],
            "description": f"System Design score is currently {sys_design_score}%. Target 85%+ for tier 1 architecture roles."
        },
        {
            "role": "Cloud Engineer",
            "match": cloud_match,
            "required": ["AWS Architecture", "Terraform / Infrastructure as Code", "Docker & Kubernetes"],
            "description": f"Requires elevating Cloud & DevOps scores from {cloud_score}% and {devops_score}%."
        },
        {
            "role": "Engineering Lead",
            "match": eng_lead_match,
            "required": ["Team Strategy & Hiring", "Sprint Planning", "Cross-functional Leadership"],
            "description": f"Leverages your {lead_score}% Leadership rating and team mentoring background."
        }
    ]

    # Sort transitions by match score descending
    transitions.sort(key=lambda x: x["match"], reverse=True)

    for item in transitions:
        with st.container(border=True):
            col1, col2 = st.columns([3, 1], vertical_alignment="center")
            with col1:
                st.markdown(f"#### {item['role']}")
                st.write(item["description"])
                st.write(f"**Key Skills to master:** {', '.join(item['required'])}")
            with col2:
                st.metric("Match Score", f"{item['match']}%")
                st.progress(item["match"] / 100.0)

    top_role = transitions[0]
    st.divider()
    st.markdown("### AI Transition Feasibility Insight")
    st.success(f"Targeting **{top_role['role']} ({top_role['match']}% Match)** yields your highest transition velocity with an estimated 25% to 45% salary upside.")

