import streamlit as st
from professional.database import get_professional_skills, save_professional_skills

def render_skills_section(user_id):
    st.subheader("2. Professional Skill Assessment")
    st.caption("Rate your core engineering and leadership domain competencies.")

    skills = get_professional_skills(user_id)

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("### Current Skill Benchmark Scores")
        for skill_name, score in skills.items():
            st.write(f"**{skill_name}**: `{score}%`")
            st.progress(score / 100.0)



    with col2:
        st.markdown("### Update Skill Levels")
        with st.form("prof_skills_form"):
            new_backend = st.slider("Backend Development", 0, 100, int(skills.get("Backend Development", 0)))
            new_sys_design = st.slider("System Design", 0, 100, int(skills.get("System Design", 0)))
            new_cloud = st.slider("Cloud Computing", 0, 100, int(skills.get("Cloud Computing", 0)))
            new_devops = st.slider("DevOps", 0, 100, int(skills.get("DevOps", 0)))
            new_leadership = st.slider("Leadership", 0, 100, int(skills.get("Leadership", 0)))

            saved = st.form_submit_button("Save Skill Assessment", use_container_width=True)
            if saved:
                updated_skills = {
                    "Backend Development": new_backend,
                    "System Design": new_sys_design,
                    "Cloud Computing": new_cloud,
                    "DevOps": new_devops,
                    "Leadership": new_leadership
                }
                save_professional_skills(user_id, updated_skills)
                st.success("Skill assessment updated successfully!")
                st.rerun()

    st.divider()
    avg_score = sum(skills.values()) / max(len(skills), 1)
    has_skills = any(v > 0 for v in skills.values())

    if has_skills:
        strongest_key = max(skills, key=skills.get)
        weakest_key = min(skills, key=skills.get)
        strongest_str = f"{strongest_key} ({skills[strongest_key]}%)"
        weakest_str = f"{weakest_key} ({skills[weakest_key]}%)"
    else:
        strongest_str = "Not Assessed"
        weakest_str = "Not Assessed"

    c1, c2, c3 = st.columns(3)
    c1.metric("Overall Competency Score", f"{avg_score:.1f}%")
    c2.metric("Strongest Technical Domain", strongest_str)
    c3.metric("Primary Skill Focus Area", weakest_str)


