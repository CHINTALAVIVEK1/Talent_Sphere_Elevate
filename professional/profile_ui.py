import streamlit as st
from professional.database import get_professional_profile, save_professional_profile

def render_profile_section(user_id):
    st.subheader("1. Professional Profile")
    st.caption("Manage your current employment, skills, leadership experience, and career aspirations.")

    profile = get_professional_profile(user_id)
    current_name = st.session_state.get("user_name", "")

    with st.form("prof_profile_form"):
        col1, col2 = st.columns(2)

        with col1:
            full_name = st.text_input("Full Name", value=current_name, placeholder="Enter your full name")
            company = st.text_input("Current Company", value=profile.get("company", ""), placeholder="e.g. TechCorp Solutions")
            current_role = st.text_input("Current Role", value="" if profile.get("current_role") == "Not Set" else profile.get("current_role", ""), placeholder="e.g. Software Developer")
            experience = st.number_input("Total Experience (Years)", min_value=0, max_value=40, value=int(profile.get("experience", 0)))
            current_salary = st.number_input("Current Salary (LPA in ₹)", min_value=0.0, max_value=200.0, value=float(profile.get("current_salary", 0.0)), step=0.5)

        with col2:
            all_skill_options = ["Python", "Django", "REST API", "SQL", "Git", "Java", "React", "Node.js", "Docker", "Kubernetes", "AWS", "Microservices", "System Design", "CI/CD"]
            current_skills = profile.get("skills", [])
            skills_selected = st.multiselect("Technical Skills", options=list(dict.fromkeys(all_skill_options + current_skills)), default=current_skills)

            all_certs = ["AWS Cloud Practitioner", "AWS Solutions Architect", "Docker Certified Associate", "Kubernetes Administrator", "System Design Fundamentals"]
            certs_selected = st.multiselect("Certifications", options=list(dict.fromkeys(all_certs + profile.get("certifications", []))), default=profile.get("certifications", []))

            career_goals = st.text_input("Career Goal", value=profile.get("career_goals", ""), placeholder="e.g. Become Senior Backend Engineer")
            all_roles = ["Senior Backend Engineer", "Backend Architect", "Cloud Engineer", "Engineering Lead", "DevOps Engineer", "Solutions Architect"]
            preferred_roles = st.multiselect("Preferred Job Roles", options=all_roles, default=profile.get("preferred_roles", []))

        leadership_exp = st.text_area("Leadership Experience / Impact", value=profile.get("leadership_exp", ""), placeholder="Describe any leadership, team coordination, or project ownership highlights...", height=100)

        submitted = st.form_submit_button("Save Profile Updates", use_container_width=True)
        if submitted:
            st.session_state["user_name"] = full_name
            updated_data = {
                "company": company,
                "current_role": current_role if current_role else "Not Set",
                "experience": experience,
                "current_salary": current_salary,
                "skills": skills_selected,
                "leadership_exp": leadership_exp,
                "certifications": certs_selected,
                "career_goals": career_goals,
                "preferred_roles": preferred_roles
            }
            save_professional_profile(user_id, updated_data)
            st.success("Professional Profile saved successfully!")
            st.rerun()

    st.divider()
    st.markdown("### Profile Summary Card")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Name", st.session_state.get("user_name", "Not Set") or "Not Set")
    c2.metric("Current Role", profile.get("current_role", "Not Set"))
    c3.metric("Company", profile.get("company", "Not Specified") or "Not Specified")
    c4.metric("Experience", f"{profile.get('experience', 0)} Yrs")

    st.markdown(f"**Current Salary:** ₹{profile.get('current_salary', 0.0):.1f} LPA")
    st.markdown(f"**Technical Skills:** {', '.join(profile.get('skills', [])) if profile.get('skills') else 'None selected'}")
    st.markdown(f"**Career Goal:** {profile.get('career_goals', 'Not set')}")
    st.markdown(f"**Target Roles:** {', '.join(profile.get('preferred_roles', [])) if profile.get('preferred_roles') else 'None selected'}")
    st.markdown(f"**Leadership Highlight:** {profile.get('leadership_exp', 'None provided')}")


