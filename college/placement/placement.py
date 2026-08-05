import streamlit as st
import datetime
import pandas as pd
from college.coding.database import get_placements, save_placement, delete_placement
from college.coding.roadmap import get_resume_skill_gaps

def placement_preparation():
    st.markdown("### Placement Preparation")
    st.write("Track active job/internship applications, view recommendations matched to your skill gaps, and explore hackathons.")
    
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("Please log in to continue.")
        return
        
    tab_tracker, tab_internships, tab_hackathons = st.tabs([
        "Job Application Tracker",
        "Internship Recommendations",
        "Upcoming Hackathons"
    ])
    
    # ==========================================
    # TAB 1: JOB TRACKER
    # ==========================================
    with tab_tracker:
        st.markdown("#### Application Logger")
        
        # Add application form
        with st.expander("Log New Job / Internship Application", expanded=False):
            with st.form("add_placement_form_p", clear_on_submit=True):
                company = st.text_input("Company Name", placeholder="e.g. Amazon")
                role = st.text_input("Role Title", placeholder="e.g. Cloud Developer Intern")
                status = st.selectbox("Application Status", ["Applied", "Interviewing", "Offered", "Rejected"])
                package = st.text_input("Package / Stipend (e.g. 15 LPA, $40/hr)")
                interview_date = st.date_input("Interview / Test Date", value=datetime.date.today())
                
                sub_btn = st.form_submit_button("Save Application")
                if sub_btn:
                    if company.strip() and role.strip():
                        save_placement(user_id, company.strip(), role.strip(), status, package.strip(), interview_date.isoformat())
                        st.success(f"Log saved successfully for {company.strip()} - {role.strip()}.")
                        st.rerun()
                    else:
                        st.error("Company Name and Role Title are required.")
                        
        # Display applications
        apps = get_placements(user_id)
        if apps:
            df_apps = pd.DataFrame(apps)
            df_display = df_apps[["company", "role", "status", "package", "interview_date"]]
            df_display.columns = ["Company", "Role", "Status", "Package Details", "Action Date"]
            st.dataframe(df_display, use_container_width=True)
            
            st.write("")
            st.markdown("##### Remove Application Record:")
            app_delete_idx = st.selectbox(
                "Select record to remove",
                range(len(apps)),
                format_func=lambda i: f"{apps[i]['company']} - {apps[i]['role']} ({apps[i]['status']})"
            )
            if st.button("Delete Selected Record", type="secondary"):
                delete_placement(user_id, apps[app_delete_idx]["id"])
                st.success("Record deleted successfully.")
                st.rerun()
        else:
            st.info("No applications logged yet. Track your placements by adding a record above.")

    # ==========================================
    # TAB 2: INTERNSHIP RECOMMENDATIONS
    # ==========================================
    with tab_internships:
        st.markdown("#### AI Internship Matches")
        st.write("Dynamic internship opportunities matched based on your current resume skills and identified gaps:")
        
        gaps = get_resume_skill_gaps(user_id)
        
        # Recommendations
        if gaps["missing_skills"]:
            for skill in gaps["missing_skills"][:3]:
                st.markdown(f"""
                <div style="background-color: #1e293b; padding: 15px; border-radius: 6px; margin-bottom: 12px; border-left: 4px solid #f59e0b; border-right: 1px solid #334155; border-top: 1px solid #334155; border-bottom: 1px solid #334155;">
                    <b style="color: #f8fafc; font-size: 15px;">{skill} Engineering Intern</b><br/>
                    <span style="font-size: 13px; color: #94a3b8;">Required: {skill}, Data Structures, General Problem Solving</span><br/>
                    <span style="font-size: 13px; color: #fca5a5;">Gaps: Study {skill} roadmap subtopics to complete match.</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background-color: #1e293b; padding: 15px; border-radius: 6px; margin-bottom: 12px; border-left: 4px solid #10b981; border-right: 1px solid #334155; border-top: 1px solid #334155; border-bottom: 1px solid #334155;">
                <b style="color: #f8fafc; font-size: 15px;">Full-Stack Developer Intern</b><br/>
                <span style="font-size: 13px; color: #94a3b8;">Google / Amazon / Meta Retail System Backend Services</span><br/>
                <span style="font-size: 13px; color: #4ade80;">Resume Match: 95% (All core placement skills met).</span>
            </div>
            """, unsafe_allow_html=True)

    # ==========================================
    # TAB 3: HACKATHONS
    # ==========================================
    with tab_hackathons:
        st.markdown("#### Upcoming Hackathons")
        st.write("Active programming events to test your engineering capability, build your portfolio, and gain visibility:")
        
        hackathons = [
            {"name": "Smart India Hackathon", "organizer": "Government of India", "date": "August 2026", "prize": "1 Lakh INR"},
            {"name": "Google Hash Code", "organizer": "Google Inc.", "date": "September 2026", "prize": "Global Recognition"},
            {"name": "Meta Hacker Cup", "organizer": "Meta", "date": "October 2026", "prize": "$10,000 USD"}
        ]
        
        for hk in hackathons:
            st.markdown(f"""
            <div style="background-color: #1e293b; padding: 12px 18px; border-radius: 6px; margin-bottom: 8px; border: 1px solid #334155;">
                <b style="color: #60a5fa; font-size: 15px;">{hk['name']}</b><br/>
                <span style="font-size: 13px; color: #94a3b8;">Organizer: {hk['organizer']}</span><br/>
                <span style="font-size: 13px; color: #f8fafc;">Date: {hk['date']} | Prizes: {hk['prize']}</span>
            </div>
            """, unsafe_allow_html=True)
