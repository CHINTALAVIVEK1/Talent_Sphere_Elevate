import streamlit as st
import json
from college.resume.database import get_resume, save_resume
from college.resume.templates import DEFAULT_SKILLS, CUSTOM_CSS
from college.resume.pdf_generator import generate_resume_pdf
from college.resume.ats_score import render_ats_analyzer
from college.resume.gemini_resume import (
    generate_ai_objective,
    optimize_career_objective,
    optimize_project_description
)

def resume_builder():
    """
    Main controller for the Resume Studio module inside the College Dashboard.
    Uses three Streamlit tabs: Resume Builder, ATS Resume Analyzer, AI Resume Optimizer.
    """
    # Embed customized stylesheet
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("Please log in to use the Resume Studio.")
        return
        
    # Load resume data on initialization
    if "resume_data" not in st.session_state:
        db_data = get_resume(user_id)
        if db_data:
            st.session_state.resume_data = db_data
        else:
            st.session_state.resume_data = {
                "full_name": st.session_state.get("user_name", ""),
                "email": "",
                "phone": "",
                "linkedin": "",
                "github": "",
                "address": "",
                "college": "",
                "degree": "",
                "branch": "",
                "cgpa": "",
                "graduation_year": "",
                "skills": [],
                "experience": [],
                "projects": [],
                "certifications": [],
                "languages": [],
                "career_objective": ""
            }
            
    # Define tabs
    tab_builder, tab_analyzer, tab_optimizer = st.tabs([
        "📝 Resume Builder",
        "🔍 ATS Resume Analyzer",
        "⚡ AI Resume Optimizer"
    ])
    
    # ==========================================
    # TAB 1: RESUME BUILDER
    # ==========================================
    with tab_builder:
        st.markdown("###  Resume Builder")
        st.write("Fill in your details below to build your professional resume. All changes will be saved to the database.")
        
        # 1. Personal Information
        with st.expander("👤 Personal Information", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                full_name = st.text_input("Full Name", value=st.session_state.resume_data.get("full_name", ""))
                phone = st.text_input("Phone Number", value=st.session_state.resume_data.get("phone", ""))
                github = st.text_input("GitHub Profile URL", value=st.session_state.resume_data.get("github", ""))
            with c2:
                email = st.text_input("Email Address", value=st.session_state.resume_data.get("email", ""))
                linkedin = st.text_input("LinkedIn Profile URL", value=st.session_state.resume_data.get("linkedin", ""))
                address = st.text_input("Address", value=st.session_state.resume_data.get("address", ""))
                
        # 2. Education
        with st.expander("🎓 Education", expanded=False):
            college = st.text_input("College / University", value=st.session_state.resume_data.get("college", ""))
            c_edu1, c_edu2, c_edu3 = st.columns(3)
            with c_edu1:
                degree = st.text_input("Degree (e.g. B.Tech, B.Sc)", value=st.session_state.resume_data.get("degree", ""))
            with c_edu2:
                branch = st.text_input("Branch / Major", value=st.session_state.resume_data.get("branch", ""))
            with c_edu3:
                cgpa = st.text_input("CGPA or Percentage", value=st.session_state.resume_data.get("cgpa", ""))
            graduation_year = st.text_input("Graduation Year", value=st.session_state.resume_data.get("graduation_year", ""))
            
        # 3. Skills
        with st.expander("🛠 Technical Skills", expanded=False):
            current_skills = st.session_state.resume_data.get("skills", [])
            # Combine default and current custom skills
            all_options = list(set(DEFAULT_SKILLS + current_skills))
            
            selected_skills = st.multiselect(
                "Select Skills",
                options=all_options,
                default=current_skills
            )
            
            # Custom skill adder
            c_sk1, c_sk2 = st.columns([3, 1])
            with c_sk1:
                new_custom_skill = st.text_input("Add Custom Skill", value="", placeholder="e.g. Docker, AWS, Kubernetes", key="custom_skill_input")
            with c_sk2:
                st.write("")
                st.write("")
                if st.button("➕ Add", key="add_custom_skill_btn", use_container_width=True):
                    if new_custom_skill.strip():
                        skill_to_add = new_custom_skill.strip()
                        if skill_to_add not in selected_skills:
                            selected_skills.append(skill_to_add)
                            st.session_state.resume_data["skills"] = selected_skills
                            st.rerun()
                            
        # 4. Experience
        with st.expander("💼 Experience", expanded=False):
            exp_list = st.session_state.resume_data.get("experience", [])
            updated_exp = []
            
            for idx, exp in enumerate(exp_list):
                st.markdown(f"**Experience Details #{idx+1}**")
                col_exp1, col_exp2 = st.columns(2)
                with col_exp1:
                    comp = st.text_input(f"Company Name #{idx+1}", value=exp.get("company", ""), key=f"comp_{idx}")
                    role = st.text_input(f"Job Role #{idx+1}", value=exp.get("role", ""), key=f"role_{idx}")
                with col_exp2:
                    dur = st.text_input(f"Duration #{idx+1}", value=exp.get("duration", ""), key=f"dur_{idx}", placeholder="e.g. June 2025 - Present")
                    st.write("")
                    st.write("")
                    if st.button(f"🗑 Remove Experience #{idx+1}", key=f"rem_exp_{idx}", use_container_width=True):
                        st.session_state.resume_data["experience"].pop(idx)
                        st.rerun()
                desc = st.text_area(f"Description / Accomplishments #{idx+1}", value=exp.get("description", ""), key=f"desc_{idx}", height=120)
                updated_exp.append({
                    "company": comp,
                    "role": role,
                    "duration": dur,
                    "description": desc
                })
                st.markdown("---")
                
            if st.button("➕ Add Experience", key="add_exp_btn"):
                st.session_state.resume_data["experience"].append({"company": "", "role": "", "duration": "", "description": ""})
                st.rerun()
                
        # 5. Projects
        with st.expander("📂 Projects", expanded=False):
            proj_list = st.session_state.resume_data.get("projects", [])
            updated_proj = []
            
            for idx, proj in enumerate(proj_list):
                st.markdown(f"**Project Details #{idx+1}**")
                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    p_title = st.text_input(f"Project Title #{idx+1}", value=proj.get("title", ""), key=f"p_title_{idx}")
                    p_tech = st.text_input(f"Technologies Used #{idx+1}", value=proj.get("technologies", ""), key=f"p_tech_{idx}", placeholder="e.g. Python, SQLite")
                with col_p2:
                    p_link = st.text_input(f"Project Repository / Demo Link #{idx+1}", value=proj.get("github_link", ""), key=f"p_link_{idx}")
                    st.write("")
                    st.write("")
                    if st.button(f"🗑 Remove Project #{idx+1}", key=f"rem_proj_{idx}", use_container_width=True):
                        st.session_state.resume_data["projects"].pop(idx)
                        st.rerun()
                p_desc = st.text_area(f"Project Description #{idx+1}", value=proj.get("description", ""), key=f"p_desc_{idx}", height=120)
                updated_proj.append({
                    "title": p_title,
                    "technologies": p_tech,
                    "github_link": p_link,
                    "description": p_desc
                })
                st.markdown("---")
                
            if st.button("➕ Add Project", key="add_proj_btn"):
                st.session_state.resume_data["projects"].append({"title": "", "technologies": "", "github_link": "", "description": ""})
                st.rerun()
                
        # 6. Certifications
        with st.expander("📜 Certifications", expanded=False):
            cert_list = st.session_state.resume_data.get("certifications", [])
            updated_certs = []
            
            for idx, cert in enumerate(cert_list):
                col_cert1, col_cert2 = st.columns([5, 1])
                with col_cert1:
                    cert_val = st.text_input(f"Certification #{idx+1}", value=cert, key=f"cert_{idx}")
                with col_cert2:
                    st.write("")
                    if st.button("🗑", key=f"rem_cert_{idx}", use_container_width=True):
                        st.session_state.resume_data["certifications"].pop(idx)
                        st.rerun()
                updated_certs.append(cert_val)
                
            if st.button("➕ Add Certification", key="add_cert_btn"):
                st.session_state.resume_data["certifications"].append("")
                st.rerun()
                
        # 7. Languages
        with st.expander("🗣 Languages", expanded=False):
            lang_list = st.session_state.resume_data.get("languages", [])
            updated_langs = []
            
            for idx, lang in enumerate(lang_list):
                col_lang1, col_lang2 = st.columns([5, 1])
                with col_lang1:
                    lang_val = st.text_input(f"Language #{idx+1}", value=lang, key=f"lang_{idx}")
                with col_lang2:
                    st.write("")
                    if st.button("🗑", key=f"rem_lang_{idx}", use_container_width=True):
                        st.session_state.resume_data["languages"].pop(idx)
                        st.rerun()
                updated_langs.append(lang_val)
                
            if st.button("➕ Add Language", key="add_lang_btn"):
                st.session_state.resume_data["languages"].append("")
                st.rerun()
                
        # 8. Career Objective & AI Generation
        with st.expander("🎯 Career Objective", expanded=False):
            career_objective = st.text_area(
                "Career Objective",
                value=st.session_state.resume_data.get("career_objective", ""),
                height=120,
                help="A professional statement summarizing your career goals and key strengths."
            )
            
            if st.button("✨ Generate using AI", key="ai_obj_btn"):
                # Construct temporary dict to pass to Gemini
                temp_data = {
                    "skills": selected_skills,
                    "degree": degree,
                    "branch": branch,
                    "college": college
                }
                with st.spinner("Generating AI-driven career objective..."):
                    ai_obj = generate_ai_objective(temp_data)
                    st.session_state.resume_data["career_objective"] = ai_obj
                    st.rerun()

        # Action buttons
        st.write("")
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        
        # Save resume to sqlite
        with col_btn1:
            save_clicked = st.button("💾 Save Resume", use_container_width=True, type="primary")
            if save_clicked:
                # Sync form fields back into session state
                st.session_state.resume_data.update({
                    "full_name": full_name,
                    "email": email,
                    "phone": phone,
                    "linkedin": linkedin,
                    "github": github,
                    "address": address,
                    "college": college,
                    "degree": degree,
                    "branch": branch,
                    "cgpa": cgpa,
                    "graduation_year": graduation_year,
                    "skills": selected_skills,
                    "experience": updated_exp,
                    "projects": updated_proj,
                    "certifications": [c.strip() for c in updated_certs if c.strip()],
                    "languages": [l.strip() for l in updated_langs if l.strip()],
                    "career_objective": career_objective
                })
                save_resume(user_id, st.session_state.resume_data)
                st.success("Resume saved successfully!")
                
        # Preview resume
        with col_btn2:
            preview_clicked = st.button("👁 Preview Resume", use_container_width=True)
            if preview_clicked:
                # Sync first
                st.session_state.resume_data.update({
                    "full_name": full_name,
                    "email": email,
                    "phone": phone,
                    "linkedin": linkedin,
                    "github": github,
                    "address": address,
                    "college": college,
                    "degree": degree,
                    "branch": branch,
                    "cgpa": cgpa,
                    "graduation_year": graduation_year,
                    "skills": selected_skills,
                    "experience": updated_exp,
                    "projects": updated_proj,
                    "certifications": [c.strip() for c in updated_certs if c.strip()],
                    "languages": [l.strip() for l in updated_langs if l.strip()],
                    "career_objective": career_objective
                })
                st.session_state.show_preview = True
                st.info("Scroll down to view current preview.")
                
        # Generate PDF resume
        with col_btn3:
            pdf_clicked = st.button("📄 Generate PDF", use_container_width=True)
            if pdf_clicked:
                # Sync first
                st.session_state.resume_data.update({
                    "full_name": full_name,
                    "email": email,
                    "phone": phone,
                    "linkedin": linkedin,
                    "github": github,
                    "address": address,
                    "college": college,
                    "degree": degree,
                    "branch": branch,
                    "cgpa": cgpa,
                    "graduation_year": graduation_year,
                    "skills": selected_skills,
                    "experience": updated_exp,
                    "projects": updated_proj,
                    "certifications": [c.strip() for c in updated_certs if c.strip()],
                    "languages": [l.strip() for l in updated_langs if l.strip()],
                    "career_objective": career_objective
                })
                # Build the PDF file
                filename = f"Resume_{user_id}.pdf"
                pdf_path = generate_resume_pdf(st.session_state.resume_data, filename)
                
                with open(pdf_path, "rb") as f:
                    pdf_bytes = f.read()
                
                st.session_state.pdf_bytes = pdf_bytes
                st.success("PDF generated successfully! Click below to download:")

        # Show download button if ready
        if "pdf_bytes" in st.session_state:
            st.download_button(
                label="📥 Download Resume PDF",
                data=st.session_state.pdf_bytes,
                file_name=f"{full_name.replace(' ', '_')}_Resume.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            
        # Render static preview
        if st.session_state.get("show_preview"):
            st.divider()
            st.markdown("### 📝 Resume Preview")
            with st.container(border=True):
                st.markdown(f"<h2 style='text-align: center; color: #1e3a8a; margin-bottom: 0;'>{full_name}</h2>", unsafe_allow_html=True)
                contact_line = " | ".join([x for x in [email, phone, linkedin, github, address] if x])
                st.markdown(f"<p style='text-align: center; color: #64748b; font-size: 14px;'>{contact_line}</p>", unsafe_allow_html=True)
                
                if career_objective:
                    st.markdown("<h4 style='color: #1e3a8a; border-bottom: 1px solid #1e3a8a; padding-bottom: 2px;'>CAREER OBJECTIVE</h4>", unsafe_allow_html=True)
                    st.write(career_objective)
                    
                if college or degree or branch:
                    st.markdown("<h4 style='color: #1e3a8a; border-bottom: 1px solid #1e3a8a; padding-bottom: 2px;'>EDUCATION</h4>", unsafe_allow_html=True)
                    st.write(f"**{degree} in {branch}**")
                    st.write(f"{college} (Graduation: {graduation_year} | CGPA: {cgpa})")
                    
                if selected_skills:
                    st.markdown("<h4 style='color: #1e3a8a; border-bottom: 1px solid #1e3a8a; padding-bottom: 2px;'>TECHNICAL SKILLS</h4>", unsafe_allow_html=True)
                    st.write(", ".join(selected_skills))
                    
                if updated_exp:
                    st.markdown("<h4 style='color: #1e3a8a; border-bottom: 1px solid #1e3a8a; padding-bottom: 2px;'>PROFESSIONAL EXPERIENCE</h4>", unsafe_allow_html=True)
                    for exp in updated_exp:
                        if exp.get("company") or exp.get("role"):
                            st.write(f"**{exp.get('role')}** at **{exp.get('company')}** ({exp.get('duration')})")
                            st.write(exp.get('description'))
                            
                if updated_proj:
                    st.markdown("<h4 style='color: #1e3a8a; border-bottom: 1px solid #1e3a8a; padding-bottom: 2px;'>ACADEMIC & PERSONAL PROJECTS</h4>", unsafe_allow_html=True)
                    for proj in updated_proj:
                        if proj.get("title"):
                            title_line = f"**{proj.get('title')}** *({proj.get('technologies')})*"
                            if proj.get("github_link"):
                                title_line += f" - [GitHub]({proj.get('github_link')})"
                            st.markdown(title_line)
                            st.write(proj.get('description'))
                            
                valid_certs = [c for c in updated_certs if c.strip()]
                if valid_certs:
                    st.markdown("<h4 style='color: #1e3a8a; border-bottom: 1px solid #1e3a8a; padding-bottom: 2px;'>CERTIFICATIONS</h4>", unsafe_allow_html=True)
                    for cert in valid_certs:
                        st.write(f"• {cert}")
                        
                valid_langs = [l for l in updated_langs if l.strip()]
                if valid_langs:
                    st.markdown("<h4 style='color: #1e3a8a; border-bottom: 1px solid #1e3a8a; padding-bottom: 2px;'>LANGUAGES</h4>", unsafe_allow_html=True)
                    st.write(", ".join(valid_langs))

    # ==========================================
    # TAB 2: ATS RESUME ANALYZER
    # ==========================================
    with tab_analyzer:
        render_ats_analyzer()
        
    # ==========================================
    # TAB 3: AI RESUME OPTIMIZER
    # ==========================================
    with tab_optimizer:
        st.markdown("### ⚡ AI Resume Optimizer")
        st.write("Address identified keyword gaps and optimize your resume's impact statements to beat the ATS scanner.")
        
        # Guard clause: Require ATS analysis first
        if "ats_analysis" not in st.session_state:
            st.warning("⚠️ **Analysis Required:** Please upload a PDF resume and paste a Job Description under the **ATS Resume Analyzer** tab, then run the analysis first to unlock optimization tools.")
        else:
            job_desc_str = st.session_state.target_job_description
            
            # --- 1. Objective Optimization ---
            st.markdown("#### 🎯 Optimize Career Objective")
            st.write(f"**Current Career Objective:**")
            st.info(st.session_state.resume_data.get("career_objective", "None"))
            
            if st.button("✨ Optimize Objective via Gemini", key="opt_obj_gem"):
                with st.spinner("Rewriting career objective to match target job..."):
                    opt_objective = optimize_career_objective(
                        st.session_state.resume_data.get("career_objective", ""),
                        job_desc_str
                    )
                    st.session_state.optimized_objective_text = opt_objective
                    st.rerun()
                    
            if "optimized_objective_text" in st.session_state:
                st.success("🤖 AI-Optimized Career Objective:")
                st.write(st.session_state.optimized_objective_text)
                if st.button("💾 Apply and Save to Resume", key="apply_opt_obj"):
                    st.session_state.resume_data["career_objective"] = st.session_state.optimized_objective_text
                    save_resume(user_id, st.session_state.resume_data)
                    st.success("Applied and saved career objective!")
                    del st.session_state.optimized_objective_text
                    st.rerun()
            st.divider()
            
            # --- 2. Project Description Optimization ---
            st.markdown("#### 📂 Optimize Project Descriptions")
            projs = st.session_state.resume_data.get("projects", [])
            if not projs:
                st.info("No projects available to optimize. Add projects under the builder tab first.")
            else:
                proj_titles = [p.get("title", f"Project {i+1}") for i, p in enumerate(projs)]
                selected_proj_idx = st.selectbox("Select Project to Optimize", range(len(projs)), format_func=lambda i: proj_titles[i], key="proj_opt_select")
                proj_to_opt = projs[selected_proj_idx]
                
                st.write(f"**Current Project Description:**")
                st.info(proj_to_opt.get("description", "None"))
                
                if st.button("✨ Optimize Project Description via Gemini", key="opt_proj_desc_gem"):
                    with st.spinner("Rewriting project bullets with STAR method..."):
                        opt_proj_desc = optimize_project_description(
                            proj_to_opt.get("title", ""),
                            proj_to_opt.get("description", ""),
                            job_desc_str
                        )
                        st.session_state.optimized_proj_desc_text = opt_proj_desc
                        st.rerun()
                        
                if "optimized_proj_desc_text" in st.session_state:
                    st.success("🤖 AI-Optimized Project Description:")
                    st.write(st.session_state.optimized_proj_desc_text)
                    if st.button("💾 Apply and Save to Project", key="apply_opt_proj"):
                        st.session_state.resume_data["projects"][selected_proj_idx]["description"] = st.session_state.optimized_proj_desc_text
                        save_resume(user_id, st.session_state.resume_data)
                        st.success("Applied and saved project description!")
                        del st.session_state.optimized_proj_desc_text
                        st.rerun()
            st.divider()
            
            # --- 3. Missing Keywords Skills Auto-Adder ---
            st.markdown("#### 🛠 Add Missing Skills Keywords")
            missing_keywords = st.session_state.ats_analysis.get("missing_keywords", [])
            if not missing_keywords:
                st.success("✓ Your resume already includes all critical skills keywords identified by Gemini!")
            else:
                st.write("Gemini identified these keywords missing in your resume skills:")
                # Display pills of missing keywords
                pills = "".join([f'<span style="background-color: #7f1d1d; color: #fca5a5; padding: 4px 10px; border-radius: 12px; margin: 4px; display: inline-block; font-size: 13px;">{kw}</span>' for kw in missing_keywords])
                st.markdown(pills, unsafe_allow_html=True)
                st.write("")
                
                selected_missing = st.multiselect(
                    "Select keywords to add to your resume's skills list:",
                    options=missing_keywords,
                    default=missing_keywords[:min(3, len(missing_keywords))]
                )
                
                if st.button("➕ Add Selected Keywords to Skills List", key="add_missing_keywords_btn"):
                    curr_skills = st.session_state.resume_data.get("skills", [])
                    added_skills = []
                    for kw in selected_missing:
                        if kw not in curr_skills:
                            curr_skills.append(kw)
                            added_skills.append(kw)
                    if added_skills:
                        st.session_state.resume_data["skills"] = curr_skills
                        save_resume(user_id, st.session_state.resume_data)
                        st.success(f"Successfully added: {', '.join(added_skills)} to your skills list!")
                        st.rerun()
                    else:
                        st.info("Selected keywords are already present in your skills list.")
            st.divider()
            
            # --- 4. Generate AI-Optimized Resume PDF ---
            st.markdown("#### 📄 Compile AI-Optimized Resume PDF")
            st.write("Generate a copy of your resume incorporating ALL AI optimization features immediately, including re-written career objectives, optimized projects, and key missing skills.")
            
            if st.button("✨ Generate Optimized PDF", key="gen_opt_pdf_btn", use_container_width=True, type="primary"):
                with st.spinner("Compiling optimized content into PDF layout..."):
                    # Deep copy resume data
                    opt_resume = json.loads(json.dumps(st.session_state.resume_data))
                    
                    # 1. Optimize objective
                    opt_resume["career_objective"] = optimize_career_objective(
                        opt_resume.get("career_objective", ""),
                        job_desc_str
                    )
                    
                    # 2. Optimize projects
                    for proj in opt_resume.get("projects", []):
                        proj["description"] = optimize_project_description(
                            proj.get("title", ""),
                            proj.get("description", ""),
                            job_desc_str
                        )
                        
                    # 3. Add top 3 missing keywords to skills list
                    for kw in missing_keywords[:3]:
                        if kw not in opt_resume.get("skills", []):
                            opt_resume["skills"].append(kw)
                            
                    # Build document
                    opt_filename = f"Resume_{user_id}_Optimized.pdf"
                    opt_pdf_path = generate_resume_pdf(opt_resume, opt_filename)
                    
                    with open(opt_pdf_path, "rb") as f:
                        opt_pdf_bytes = f.read()
                        
                    st.session_state.opt_pdf_bytes = opt_pdf_bytes
                    st.success("Optimized PDF compiled successfully!")
                    
            if "opt_pdf_bytes" in st.session_state:
                st.download_button(
                    label="📥 Download AI-Optimized Resume PDF",
                    data=st.session_state.opt_pdf_bytes,
                    file_name=f"{st.session_state.resume_data.get('full_name', 'Student').replace(' ', '_')}_Optimized_Resume.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
