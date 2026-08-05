import streamlit as st
import datetime
import pandas as pd
from college.coding.database import get_certifications, save_certification, delete_certification
from college.coding.roadmap import get_resume_skill_gaps

# Popular Certification links
FREE_CERTS = [
    {
        "name": "IBM Python for Data Science",
        "provider": "Cognitive Class",
        "url": "https://cognitiveclass.ai/courses/python-for-data-science",
        "description": "Learn the basics of Python including data structures and logic."
    },
    {
        "name": "freeCodeCamp Responsive Web Design",
        "provider": "freeCodeCamp",
        "url": "https://www.freecodecamp.org/learn/responsive-web-design/",
        "description": "Comprehensive HTML, CSS, and web page layout certification."
    },
    {
        "name": "Kaggle Intro to Programming",
        "provider": "Kaggle",
        "url": "https://www.kaggle.com/learn/intro-to-programming",
        "description": "Essential Python syntax and data structures practice."
    },
    {
        "name": "Google Analytics Certification",
        "provider": "Google Skillshop",
        "url": "https://skillshop.google.com/",
        "description": "Official analytics tracking and optimization certification."
    }
]

PAID_CERTS = [
    {
        "name": "AWS Certified Developer - Associate",
        "provider": "Amazon Web Services",
        "url": "https://aws.amazon.com/certification/certified-developer-associate/",
        "fee": "$150 USD",
        "description": "Validates technical expertise in developing and maintaining AWS-based applications."
    },
    {
        "name": "Oracle Certified Associate Java SE Programmer",
        "provider": "Oracle Corporation",
        "url": "https://education.oracle.com/oracle-certified-associate-java-se-8-programmer/",
        "fee": "$245 USD",
        "description": "Validates core Java programming capabilities and foundational object-oriented logic."
    },
    {
        "name": "Google Associate Cloud Engineer",
        "provider": "Google Cloud",
        "url": "https://cloud.google.com/learn/certification/associate-cloud-engineer",
        "fee": "$125 USD",
        "description": "Focuses on deploying applications, monitoring operations, and managing enterprise cloud solutions."
    },
    {
        "name": "Microsoft Certified: Azure Developer Associate",
        "provider": "Microsoft Corporation",
        "url": "https://learn.microsoft.com/en-us/credentials/certifications/azure-developer-associate/",
        "fee": "$165 USD",
        "description": "Validates ability to design, build, test, and maintain cloud SDK services on Microsoft Azure."
    }
]

def certifications_track():
    st.markdown("### Certifications Tracker")
    st.write("Log your completed certifications, see AI recommendations matched to resume gaps, and browse free and paid certification directories.")
    
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("Please log in to continue.")
        return
        
    tab_log, tab_recs, tab_directory = st.tabs([
        "My Logged Certifications",
        "AI Certification Recommendations",
        "Certifications Directory"
    ])
    
    # ==========================================
    # TAB 1: LOGGED CERTIFICATIONS
    # ==========================================
    with tab_log:
        st.markdown("#### Completed Credentials")
        
        with st.expander("Log Completed Certification", expanded=False):
            with st.form("add_cert_form", clear_on_submit=True):
                name = st.text_input("Certification Name", placeholder="e.g. AWS Developer Associate")
                provider = st.text_input("Issuing Provider", placeholder="e.g. Amazon Web Services")
                date = st.date_input("Completion Date", value=datetime.date.today())
                cred_id = st.text_input("Credential ID (Optional)", placeholder="e.g. AWS-DEV-12345")
                
                sub_btn = st.form_submit_button("Log Certification")
                if sub_btn:
                    if name.strip() and provider.strip():
                        save_certification(user_id, name.strip(), provider.strip(), date.isoformat(), cred_id.strip())
                        st.success(f"Logged certification {name.strip()}.")
                        st.rerun()
                    else:
                        st.error("Certification Name and Issuing Provider are required.")
                        
        certs = get_certifications(user_id)
        if certs:
            df_certs = pd.DataFrame(certs)
            df_display = df_certs[["name", "provider", "completion_date", "credential_id"]]
            df_display.columns = ["Name", "Provider", "Completion Date", "Credential ID"]
            st.dataframe(df_display, use_container_width=True)
            
            st.write("")
            st.markdown("##### Remove Certification:")
            cert_delete_idx = st.selectbox(
                "Select record to remove",
                range(len(certs)),
                format_func=lambda i: f"{certs[i]['name']} from {certs[i]['provider']}"
            )
            if st.button("Delete Selected Certification", type="secondary"):
                delete_certification(user_id, certs[cert_delete_idx]["id"])
                st.success("Record deleted successfully.")
                st.rerun()
        else:
            st.info("No certifications logged yet. Document your completed credentials using the form above.")

    # ==========================================
    # TAB 2: AI RECOMMENDATIONS
    # ==========================================
    with tab_recs:
        st.markdown("#### Gap-Matched Certifications")
        st.write("We analyzed your resume and found matching technical cloud or development credentials that target your skill gaps:")
        
        gaps = get_resume_skill_gaps(user_id)
        
        if gaps["missing_skills"]:
            for skill in gaps["missing_skills"][:3]:
                if skill == "Python":
                    st.info("**PCEP: Certified Entry-Level Python Programmer**\nProvider: Python Institute\nMatch Target: Resolves Python skills gaps on your resume.")
                elif skill == "SQL":
                    st.info("**PostgreSQL Associate Database Certification**\nProvider: EnterpriseDB\nMatch Target: Resolves SQL and relational database query gaps.")
                elif skill == "APIs":
                    st.info("**AWS Certified Developer - Associate**\nProvider: Amazon Web Services\nMatch Target: Validates microservices, serverless APIs, and SDK deployment.")
                else:
                    st.info(f"**Professional certification in {skill}**\nProvider: Coursera / Udacity\nMatch Target: Resolves skill gaps in {skill}.")
        else:
            st.success("No critical skill gaps found on your resume. We recommend completing the **AWS Certified Cloud Practitioner** to boost your systems architecture profile.")

    # ==========================================
    # TAB 3: CERTIFICATIONS DIRECTORY
    # ==========================================
    with tab_directory:
        st.markdown("#### Free Certifications")
        col_f1, col_f2 = st.columns(2)
        
        # Render free certificates
        for idx, cert in enumerate(FREE_CERTS):
            col = col_f1 if idx % 2 == 0 else col_f2
            with col:
                st.markdown(f"""
                <div style="background-color: #0f172a; border: 1px solid #334155; padding: 15px; border-radius: 6px; margin-bottom: 12px;">
                    <b style="color: #4ade80; font-size: 15px;">{cert['name']}</b><br/>
                    <span style="font-size: 12px; color: #94a3b8;">Provider: {cert['provider']}</span><br/>
                    <span style="font-size: 13px; color: #f8fafc; display: block; margin-top: 6px;">{cert['description']}</span><br/>
                    <a href="{cert['url']}" target="_blank" style="text-decoration: none; font-size: 13px; font-weight: 600; color: #3b82f6;">Enroll for Free</a>
                </div>
                """, unsafe_allow_html=True)
                
        st.write("")
        st.divider()
        st.markdown("#### Paid Certifications")
        col_p1, col_p2 = st.columns(2)
        
        # Render paid certificates
        for idx, cert in enumerate(PAID_CERTS):
            col = col_p1 if idx % 2 == 0 else col_p2
            with col:
                st.markdown(f"""
                <div style="background-color: #0f172a; border: 1px solid #334155; padding: 15px; border-radius: 6px; margin-bottom: 12px;">
                    <b style="color: #60a5fa; font-size: 15px;">{cert['name']}</b><br/>
                    <span style="font-size: 12px; color: #94a3b8;">Provider: {cert['provider']} | Cost: {cert['fee']}</span><br/>
                    <span style="font-size: 13px; color: #f8fafc; display: block; margin-top: 6px;">{cert['description']}</span><br/>
                    <a href="{cert['url']}" target="_blank" style="text-decoration: none; font-size: 13px; font-weight: 600; color: #3b82f6;">View Certification Page</a>
                </div>
                """, unsafe_allow_html=True)
