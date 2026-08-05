# -*- coding: utf-8 -*-
import streamlit as st
from utils.report import generate_professional_report
from professional.database import (
    get_professional_profile,
    get_professional_skills,
    get_leadership_scores,
    get_certification_status
)
from professional.profile_ui import render_profile_section
from professional.skills_ui import render_skills_section
from professional.transition_ui import render_transition_section
from professional.readiness_ui import render_readiness_section
from professional.salary_ui import render_salary_section
from professional.trends_ui import render_trends_and_certs_section
from professional.leadership_ui import render_leadership_section
from professional.job_matching_ui import render_job_matching_section
from professional.roadmap_ui import render_roadmap_section

st.set_page_config(page_title="Professional Dashboard - TalentSphere Elevate", layout="wide")

st.markdown("""
<style>
[data-testid="stSidebarNav"] {
    display: none;
}
.stProgress > div > div > div > div {
    background-color: #1E88E5;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN CHECK ---------------- #
if not st.session_state.get("logged_in"):
    st.warning("Please login first to access the Working Professional Dashboard.")
    if st.button("Go to Login Page"):
        st.switch_page("pages/Login.py")
    st.stop()

user_name = st.session_state.get("user_name", "Professional")
user_id = st.session_state.get("user_id", 0)

prof_modules = [
    "home",
    "profile",
    "skills",
    "transition",
    "readiness",
    "salary",
    "trends",
    "leadership",
    "jobs",
    "roadmap"
]

if "module" not in st.session_state or st.session_state.module not in prof_modules:
    st.session_state.module = "home"

# ---------------- SIDEBAR ---------------- #
with st.sidebar:
    st.image("assets/logo.png", width=70)
    st.markdown("## Working Professional")
    st.caption("TalentSphere Elevate")
    st.divider()

    nav_items = [
        ("Dashboard Overview", "home"),
        ("Professional Profile", "profile"),
        ("Skill Assessment", "skills"),
        ("Career Transition", "transition"),
        ("Promotion Readiness", "readiness"),
        ("Salary Benchmarks", "salary"),
        ("Trends & Certifications", "trends"),
        ("Leadership Evaluation", "leadership"),
        ("Advanced Job Matching", "jobs"),
        ("90-Day AI Roadmap", "roadmap"),
    ]

    for label, key in nav_items:
        if st.button(label, use_container_width=True):
            st.session_state.module = key
            st.rerun()

    st.divider()
    if st.button("Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("app.py")

# ---------------- HEADER ---------------- #
c1, c2 = st.columns([1, 6], vertical_alignment="center")
with c1:
    st.image("assets/logo.png", width=80)
with c2:
    st.title("TalentSphere Elevate")
    st.caption("Working Professional Career Growth & Transition Module")

st.divider()

# Fetch latest database records for dashboard home & reporting
profile = get_professional_profile(user_id)
skills = get_professional_skills(user_id)
leadership = get_leadership_scores(user_id)
certs = get_certification_status(user_id)

# # Calculation metrics — all from live DB
backend_score = skills.get("Backend Development", 0)
sys_design_score = skills.get("System Design", 0)
cloud_score = skills.get("Cloud Computing", 0)
devops_score = skills.get("DevOps", 0)
skill_lead_score = skills.get("Leadership", 0)
tech_avg = int((backend_score + sys_design_score) / 2)
lead_avg = int(sum(leadership.values()) / max(len(leadership), 1))
exp = profile.get("experience", 0)
current_sal = float(profile.get("current_salary", 0.0))

# Check if this is a completely fresh/empty profile
is_blank_profile = (backend_score == 0 and sys_design_score == 0 and lead_avg == 0 and exp == 0 and current_sal == 0.0)

if is_blank_profile:
    overall_promotion_readiness = 0
    sr_backend_match = 0
    sal_growth_pct = 0
else:
    comm_readiness = min(100, int(76 + (min(exp, 10) * 1.2)))
    overall_promotion_readiness = min(99, int((tech_avg * 0.40) + (lead_avg * 0.35) + (comm_readiness * 0.15) + (min(exp, 10) * 1.0)))
    # Match score uses all 5 skill dimensions + experience
    sr_backend_match = min(99, int(
        (backend_score * 0.40) +
        (sys_design_score * 0.25) +
        (cloud_score * 0.10) +
        (devops_score * 0.05) +
        (skill_lead_score * 0.05) +
        (min(exp, 10) * 1.5)
    ))
    sal_growth_pct = max(0, int(((12.0 - current_sal) / max(current_sal, 0.1)) * 100)) if current_sal > 0 else 0

salary_potential = f"+{sal_growth_pct}%"
top_job_match = f"Senior Backend Engineer ({sr_backend_match}%)"

# ---------------- MODULE CONTENT DISPATCH ---------------- #
if st.session_state.module == "home":
    if is_blank_profile:
        st.info(" **Welcome to TalentSphere Elevate!** Complete your profile to unlock personalized career insights.")
        if st.button(" Fill Your Profile Details", use_container_width=True):
            st.session_state.module = "profile"
            st.rerun()
        st.divider()

    col_welcome, col_download = st.columns([4, 2], vertical_alignment="center")
    with col_welcome:
        st.subheader(f"Welcome back, {user_name}")
        curr_role = profile.get('current_role', '')
        curr_comp = profile.get('company', '')
        if curr_role and curr_role not in ("Not Set", ""):
            st.caption(f"**{curr_role}**{f' at **{curr_comp}**' if curr_comp else ''} · {exp} {'Year' if exp == 1 else 'Years'} Experience")
        else:
            st.caption("Please complete your **Professional Profile** and **Skill Assessment** to unlock personalized insights.")

    with col_download:
        try:
            report_file = generate_professional_report(
                user_name=user_name,
                company=profile.get("company", "N/A"),
                role=curr_role or "Not Set",
                exp=exp,
                promotion_readiness=overall_promotion_readiness,
                salary_growth=salary_potential,
                top_match=top_job_match,
                skills_dict=skills,
                cert_list=certs
            )
            with open(report_file, "rb") as f:
                pdf_bytes = f.read()
            st.download_button(
                label="Download Growth Report PDF",
                data=pdf_bytes,
                file_name=f"{user_name}_Professional_Growth_Report.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Could not compile report: {e}")

    st.write("")

    # Metrics row — 100% dynamic from DB
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(
        "Promotion Readiness",
        f"{overall_promotion_readiness}%",
        delta="Complete profile to unlock" if overall_promotion_readiness == 0 else f"Tech {tech_avg}% · Lead {lead_avg}%"
    )
    m2.metric(
        "Salary Growth Potential",
        salary_potential,
        delta="Add salary in profile" if current_sal == 0 else f"Current ₹{current_sal:.1f} LPA"
    )
    m3.metric(
        "Top Job Match",
        f"{sr_backend_match}%",
        delta="Rate skills to unlock" if sr_backend_match == 0 else "Senior Backend Engineer"
    )
    m4.metric(
        "Leadership Rating",
        f"{lead_avg}%",
        delta="Rate in Leadership tab" if lead_avg == 0 else "Across 5 dimensions"
    )

    st.divider()

    col_left, col_right = st.columns([3, 2])

    if is_blank_profile:
        with col_left:
            st.markdown("### Recommended Next Steps")
            st.info("Complete your **Professional Profile** and **Skill Assessment** to get personalized recommendations.")
            if st.button("Go to Profile →", use_container_width=True, key="goto_profile_rec"):
                st.session_state.module = "profile"
                st.rerun()

        with col_right:
            with st.container(border=True):
                st.markdown("### AI Career Summary")
                st.info("Your personalized career summary will appear here once you complete your profile and skill assessment.")
                if st.button("Go to Skill Assessment →", use_container_width=True, key="goto_skills_rec"):
                    st.session_state.module = "skills"
                    st.rerun()
    else:
        with col_left:
            # Dynamic Next Steps — driven by actual weakest skill areas
            st.markdown("### Recommended Next Steps")

            skill_advice = {
                "Backend Development": ("Strengthen Backend Fundamentals", "Target 90%+ in REST APIs, Django, and microservices patterns."),
                "System Design": ("Master System Design & Scalability", "Reach 85%+ for senior architect-level roles (+40% salary upside)."),
                "Cloud Computing": ("Complete AWS Solutions Architect Cert", "Cloud is top hiring criteria for Senior and Lead roles."),
                "DevOps": ("Learn Docker & Kubernetes", "Bridge container gap — +38% job demand growth in 2024."),
                "Leadership": ("Lead an Infrastructure Project", "Strengthen leadership score for Engineering Lead transition."),
            }
            sorted_skills_asc = sorted(skills.items(), key=lambda x: x[1])
            shown = 0
            for sk_name, sk_val in sorted_skills_asc:
                if shown >= 4:
                    break
                title, desc = skill_advice.get(sk_name, (f"Improve {sk_name}", f"Current level: {sk_val}%"))
                st.checkbox(
                    f"**{title}** — *{desc}* (Current: {sk_val}%)",
                    value=(sk_val >= 75),
                    key=f"step_{sk_name[:12]}"
                )
                shown += 1
            if shown == 0 or all(v >= 80 for v in skills.values()):
                st.success(" All core skills above 80%! Focus on leadership projects and system design interviews.")

            st.divider()

            # Skill progress bars — dynamic
            st.markdown("### Current Skill Progress Breakdown")
            for sk_name, sk_val in skills.items():
                c_a, c_b = st.columns([4, 1])
                c_a.markdown(f"**{sk_name}**")
                c_b.markdown(f"`{sk_val}%`")
                st.progress(sk_val / 100.0)

        with col_right:
            # AI Career Summary — fully dynamic
            preferred_roles = profile.get("preferred_roles", [])
            target_role = preferred_roles[0] if preferred_roles else "Not Set"
            career_goals = profile.get("career_goals", "")

            # Market salary range derived from current salary
            if current_sal > 0:
                market_low = round(current_sal * 1.4, 1)
                market_high = round(current_sal * 2.0, 1)
            else:
                market_low = 0.0
                market_high = 0.0

            # Dynamic 90-day plan based on top 3 weakest skills
            skill_months = {
                "Cloud Computing": "AWS Fundamentals & Cloud Architecture",
                "DevOps": "Docker & Kubernetes Containerization",
                "System Design": "System Design & Microservices Patterns",
                "Backend Development": "Backend Optimization & High-Scale APIs",
                "Leadership": "Leadership & Team Strategy Development",
            }
            month_plan = []
            for sk_name, sk_val in sorted_skills_asc:
                if len(month_plan) >= 3 and sk_name in skill_months:
                    break
                if sk_name in skill_months:
                    month_plan.append((sk_name, skill_months[sk_name]))
            # Fill up to 3 if needed
            fallback = [
                ("Cloud Computing", "AWS Fundamentals & Cloud Architecture"),
                ("DevOps", "Docker & Kubernetes Containerization"),
                ("System Design", "System Design & Microservices Patterns"),
            ]
            for fb in fallback:
                if len(month_plan) >= 3:
                    break
                if fb not in month_plan:
                    month_plan.append(fb)

            with st.container(border=True):
                st.markdown("### AI Career Summary")
                st.markdown(f"**Target Role:** {target_role}")
                if career_goals:
                    st.caption(f"🎯 {career_goals}")
                st.divider()
                col_s1, col_s2 = st.columns(2)
                col_s1.metric("Promotion Ready", f"{overall_promotion_readiness}%")
                col_s2.metric("Current Salary", f"₹{current_sal:.1f} LPA")
                col_s1.metric("Job Match", f"{sr_backend_match}%")
                if market_high > 0:
                    col_s2.metric("Target Market", f"₹{market_low}–{market_high} LPA")
                else:
                    col_s2.metric("Target Market", "Add salary in profile")

                st.divider()
                st.markdown("#### 90-Day Focus Plan")
                for i, (_, plan_item) in enumerate(month_plan[:3], 1):
                    st.write(f"**Month {i}:** {plan_item}")

                st.write("")
                if st.button("Explore Full 90-Day Roadmap", use_container_width=True):
                    st.session_state.module = "roadmap"
                    st.rerun()

elif st.session_state.module == "profile":
    render_profile_section(user_id)
elif st.session_state.module == "skills":
    render_skills_section(user_id)
elif st.session_state.module == "transition":
    render_transition_section(user_id)
elif st.session_state.module == "readiness":
    render_readiness_section(user_id)
elif st.session_state.module == "salary":
    render_salary_section(user_id)
elif st.session_state.module == "trends":
    render_trends_and_certs_section(user_id)
elif st.session_state.module == "leadership":
    render_leadership_section(user_id)
elif st.session_state.module == "jobs":
    render_job_matching_section(user_id)
elif st.session_state.module == "roadmap":
    render_roadmap_section(user_id)