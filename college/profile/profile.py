import streamlit as st
import json
from google.genai import types
from utils.gemini import client
from college.coding.database import get_student_profile, save_student_profile
from college.resume.pdf_parser import extract_text_from_pdf

def parse_profile_from_resume(resume_text):
    """
    Calls Gemini API to parse resume text and extract profile details.
    """
    prompt = f"""
    You are an expert resume parsing assistant.
    Analyze the following resume text and extract the key profile fields in structured JSON format.

    Resume Text:
    {resume_text}

    You MUST return a JSON object with the following fields:
    - college_name (String: name of the college or university, or empty string if not found)
    - degree (String: must match exactly one of: 'B.E', 'B.Tech', 'B.Sc', 'MCA', 'M.Tech', 'BCA', or if not matching, select 'Other')
    - department (String: e.g. 'Computer Science', 'Information Technology', 'Mechanical Engineering', etc., or empty string if not found)
    - year_of_study (String: guess based on graduation year if possible, matching one of: '1st Year', '2nd Year', '3rd Year', '4th Year', or 'Other')
    - cgpa_percentage (String: e.g. '9.2', '85%', etc., or empty string if not found)
    - skills (String: comma-separated list of technical skills found, e.g. 'Python, HTML, CSS')
    - interested_roles (String: comma-separated list of suggested job roles based on their resume, e.g. 'Software Developer, Frontend Engineer')

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
        st.error(f"Error parsing profile from resume using AI: {e}")
        return None

def student_profile_tab():
    st.subheader("👤 Student Profile")
    st.write("View and update your academic achievements and career preferences below.")

    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("Please log in to continue.")
        return

    # Load existing profile
    profile = get_student_profile(user_id)

    # Initialize session state variables for the inputs if not already present or if user changed
    if "profile_loaded" not in st.session_state or st.session_state.get("profile_user_id") != user_id or "profile_degree" not in st.session_state:
        st.session_state.profile_loaded = True
        st.session_state.profile_user_id = user_id
        st.session_state.profile_college_name = profile.get("college_name", "")
        st.session_state.profile_degree = profile.get("degree") or "B.Tech"
        st.session_state.profile_department = profile.get("department", "")
        st.session_state.profile_year_of_study = profile.get("year_of_study") or "1st Year"
        st.session_state.profile_cgpa_percentage = profile.get("cgpa_percentage", "")
        st.session_state.profile_skills = profile.get("skills", "")
        st.session_state.profile_interested_roles = profile.get("interested_roles", "")

    # If the user is not in editing mode, show the profile details table
    if not st.session_state.get("profile_editing", False):
        # 1. VIEW MODE: Show details in a structured table format
        profile_html = f"""
        <div style="background-color: #ffffff; padding: 22px; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); margin-bottom: 20px;">
            <h4 style="margin-top: 0; color: #1e3a8a; border-bottom: 2px solid #3b82f6; padding-bottom: 8px; font-family: sans-serif;">Academic & Career Summary</h4>
            <table style="width: 100%; border-collapse: collapse; font-family: sans-serif; font-size: 15px; text-align: left;">
                <tr style="border-bottom: 1px solid #f1f5f9;">
                    <td style="padding: 12px 0; font-weight: 600; color: #4b5563; width: 35%;">Name</td>
                    <td style="padding: 12px 0; color: #1f2937; font-weight: bold;">{profile.get('name', 'N/A')}</td>
                </tr>
                <tr style="border-bottom: 1px solid #f1f5f9;">
                    <td style="padding: 12px 0; font-weight: 600; color: #4b5563;">College Name</td>
                    <td style="padding: 12px 0; color: #1f2937;">{profile.get('college_name') or '<span style="color:#9ca3af; font-style:italic;">Not Provided</span>'}</td>
                </tr>
                <tr style="border-bottom: 1px solid #f1f5f9;">
                    <td style="padding: 12px 0; font-weight: 600; color: #4b5563;">Degree</td>
                    <td style="padding: 12px 0; color: #1f2937;">{profile.get('degree') or '<span style="color:#9ca3af; font-style:italic;">Not Provided</span>'}</td>
                </tr>
                <tr style="border-bottom: 1px solid #f1f5f9;">
                    <td style="padding: 12px 0; font-weight: 600; color: #4b5563;">Department / Branch</td>
                    <td style="padding: 12px 0; color: #1f2937;">{profile.get('department') or '<span style="color:#9ca3af; font-style:italic;">Not Provided</span>'}</td>
                </tr>
                <tr style="border-bottom: 1px solid #f1f5f9;">
                    <td style="padding: 12px 0; font-weight: 600; color: #4b5563;">Year of Study</td>
                    <td style="padding: 12px 0; color: #1f2937;">{profile.get('year_of_study') or '<span style="color:#9ca3af; font-style:italic;">Not Provided</span>'}</td>
                </tr>
                <tr style="border-bottom: 1px solid #f1f5f9;">
                    <td style="padding: 12px 0; font-weight: 600; color: #4b5563;">CGPA / Percentage</td>
                    <td style="padding: 12px 0; color: #10b981; font-weight: bold;">{profile.get('cgpa_percentage') or '<span style="color:#9ca3af; font-style:italic;">Not Provided</span>'}</td>
                </tr>
                <tr style="border-bottom: 1px solid #f1f5f9;">
                    <td style="padding: 12px 0; font-weight: 600; color: #4b5563;">Skills Known</td>
                    <td style="padding: 12px 0; color: #1f2937;">{profile.get('skills') or '<span style="color:#9ca3af; font-style:italic;">Not Provided</span>'}</td>
                </tr>
                <tr style="border-bottom: 1px solid #f1f5f9;">
                    <td style="padding: 12px 0; font-weight: 600; color: #4b5563;">Interested Job Roles</td>
                    <td style="padding: 12px 0; color: #1f2937;">{profile.get('interested_roles') or '<span style="color:#9ca3af; font-style:italic;">Not Provided</span>'}</td>
                </tr>
                <tr>
                    <td style="padding: 12px 0; font-weight: 600; color: #4b5563;">Resume File</td>
                    <td style="padding: 12px 0; color: #1f2937; font-weight: 500;">{profile.get('resume_filename') or '<span style="color:#9ca3af; font-style:italic;">No Resume Uploaded</span>'}</td>
                </tr>
            </table>
        </div>
        """
        st.markdown(profile_html, unsafe_allow_html=True)
        
        # Resume Download and Delete buttons
        if profile.get("resume_filename"):
            c_dl, c_rm = st.columns(2)
            with c_dl:
                st.download_button(
                    label="📥 Download Uploaded Resume",
                    data=profile["resume_bytes"],
                    file_name=profile["resume_filename"],
                    mime="application/pdf",
                    key="view_download_resume_btn",
                    use_container_width=True
                )
            with c_rm:
                if st.button("🗑️ Remove Resume", key="view_remove_resume_btn", use_container_width=True, type="secondary"):
                    from college.coding.database import delete_student_resume
                    delete_student_resume(user_id)
                    st.success("Resume removed successfully!")
                    st.rerun()
        else:
            st.info("💡 You can upload a resume in the update form.")

        st.write("")
        if st.button("✏️ Update Profile Details", type="primary", use_container_width=True):
            st.session_state.profile_editing = True
            st.rerun()

    else:
        # 2. EDIT MODE: Render form inputs to edit student profile
        # Degrees and Years options
        degree_options = ["B.E", "B.Tech", "B.Sc", "MCA", "M.Tech", "BCA", "M.Sc", "MBA", "Other"]
        year_options = ["1st Year", "2nd Year", "3rd Year", "4th Year", "Other"]

        # Ensure selected value exists in options, else set to "Other"
        current_degree = st.session_state.profile_degree
        if current_degree not in degree_options:
            current_degree = "Other"
            
        current_year = st.session_state.profile_year_of_study
        if current_year not in year_options:
            current_year = "Other"

        # Layout: Two columns
        col_left, col_right = st.columns([1, 1], gap="large")

        with col_left:
            st.markdown("#### 📝 Edit Personal & Academic Details")
            
            # Read-only Name from registration
            st.text_input("Full Name (from Registration)", value=profile.get("name", ""), disabled=True, help="Your name is synced with registration.")
            
            # College Name
            college_name = st.text_input("College Name", value=st.session_state.profile_college_name, key="profile_college_name")
            
            # Degree & Department
            c_deg, c_dept = st.columns(2)
            with c_deg:
                degree_idx = degree_options.index(current_degree)
                degree = st.selectbox("Degree", degree_options, index=degree_idx, key="profile_degree")
            with c_dept:
                department = st.text_input("Department / Branch", value=st.session_state.profile_department, key="profile_department", placeholder="e.g. Computer Science")
                
            # Year of Study & CGPA
            c_yr, c_cgpa = st.columns(2)
            with c_yr:
                year_idx = year_options.index(current_year)
                year_of_study = st.selectbox("Year of Study", year_options, index=year_idx, key="profile_year_of_study")
            with c_cgpa:
                cgpa_percentage = st.text_input("CGPA / Percentage", value=st.session_state.profile_cgpa_percentage, key="profile_cgpa_percentage", placeholder="e.g. 9.2 or 88%")

            # Skills & Job Roles
            skills = st.text_area("Skills Known (comma-separated)", value=st.session_state.profile_skills, key="profile_skills", placeholder="e.g. Python, HTML, CSS, JavaScript", height=80)
            interested_roles = st.text_area("Interested Job Roles (comma-separated)", value=st.session_state.profile_interested_roles, key="profile_interested_roles", placeholder="e.g. Software Developer, Frontend Developer", height=80)

        with col_right:
            st.markdown("#### 📄 Resume Upload & AI Parsing")
            
            # Display existing resume if any
            if profile.get("resume_filename"):
                st.info(f"📁 Current Resume: **{profile.get('resume_filename')}**")
                # Safe binary data retrieval
                resume_data_bytes = profile.get("resume_bytes")
                if resume_data_bytes:
                    st.download_button(
                        label="📥 Download Uploaded Resume",
                        data=resume_data_bytes,
                        file_name=profile.get("resume_filename"),
                        mime="application/pdf",
                        key="edit_download_resume_btn",
                        use_container_width=True
                    )
                    if st.button("❌ Remove Resume", key="edit_remove_resume_btn", use_container_width=True, type="secondary"):
                        from college.coding.database import delete_student_resume
                        delete_student_resume(user_id)
                        st.success("Resume removed successfully!")
                        st.rerun()
            else:
                st.warning("⚠️ No resume uploaded yet.")

            st.write("")
            uploaded_file = st.file_uploader("Upload New Resume (PDF only)", type=["pdf"], key="resume_uploader")
            
            # Parser option
            if uploaded_file is not None:
                st.success(f"Selected file: {uploaded_file.name}")
                
                # Button to parse
                if st.button("⚡ Auto-Fill Profile from Resume (AI)", type="secondary", use_container_width=True):
                    with st.spinner("Extracting text and running AI parsing..."):
                        resume_text = extract_text_from_pdf(uploaded_file)
                        if resume_text.strip():
                            parsed = parse_profile_from_resume(resume_text)
                            if parsed:
                                # Update session state values
                                st.session_state.profile_college_name = parsed.get("college_name", "")
                                st.session_state.profile_degree = parsed.get("degree", "Other")
                                st.session_state.profile_department = parsed.get("department", "")
                                st.session_state.profile_year_of_study = parsed.get("year_of_study", "Other")
                                st.session_state.profile_cgpa_percentage = parsed.get("cgpa_percentage", "")
                                st.session_state.profile_skills = parsed.get("skills", "")
                                st.session_state.profile_interested_roles = parsed.get("interested_roles", "")
                                st.success("✨ suggested inputs populated from resume! Click 'Save Profile' below to apply.")
                                st.rerun()
                        else:
                            st.error("Could not extract any readable text from the uploaded PDF. Please make sure it's not a scanned image.")

        st.divider()

        # Save and Cancel buttons
        c_save, c_cancel = st.columns(2)
        with c_save:
            if st.button("💾 Save Profile", type="primary", use_container_width=True):
                res_filename = None
                res_bytes = None
                if uploaded_file is not None:
                    res_filename = uploaded_file.name
                    res_bytes = uploaded_file.read()

                save_student_profile(
                    user_id=user_id,
                    college_name=college_name,
                    degree=degree,
                    department=department,
                    year_of_study=year_of_study,
                    cgpa_percentage=cgpa_percentage,
                    skills=skills,
                    interested_roles=interested_roles,
                    resume_filename=res_filename,
                    resume_bytes=res_bytes
                )
                st.success("🎉 Profile updated successfully!")
                st.session_state.profile_editing = False
                st.rerun()
                
        with c_cancel:
            if st.button("❌ Cancel", type="secondary", use_container_width=True):
                st.session_state.profile_editing = False
                st.rerun()
