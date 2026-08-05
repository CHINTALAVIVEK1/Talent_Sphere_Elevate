import streamlit as st
from college.resume.pdf_parser import extract_text_from_pdf
from college.resume.gemini_resume import analyze_ats
from college.resume.templates import CUSTOM_CSS

def render_ats_analyzer():
    """
    Renders the ATS Resume Analyzer tab interface.
    """
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    
    st.markdown("### 🔍 ATS Resume Analyzer")
    st.write("Compare your resume against a specific job description to receive detailed feedback on keyword matches, strengths, and weaknesses.")
    
    col1, col2 = st.columns([1, 1], gap="medium")
    
    with col1:
        st.markdown("##### 1. Upload Your Resume")
        uploaded_file = st.file_uploader(
            "Upload Resume (PDF format only)",
            type=["pdf"],
            help="Please upload your PDF resume to extract its text."
        )
        
        # Display feedback when file is uploaded
        if uploaded_file:
            st.success(f"✓ {uploaded_file.name} uploaded successfully!")
            
    with col2:
        st.markdown("##### 2. Paste Job Description")
        job_desc = st.text_area(
            "Paste the target job description here...",
            height=180,
            placeholder="We are looking for a Software Engineer with experience in Python, SQL..."
        )
        
    st.write("")
    
    analyze_btn = st.button("🚀 Analyze Resume", use_container_width=True, type="primary")
    
    if analyze_btn:
        if not uploaded_file:
            st.error("Please upload a resume PDF first.")
        elif not job_desc.strip():
            st.error("Please enter a job description to compare against.")
        else:
            with st.spinner("Analyzing resume content and parsing job description via Gemini AI..."):
                # Extract text from PDF
                resume_text = extract_text_from_pdf(uploaded_file)
                
                if not resume_text:
                    st.error("Could not extract text from the uploaded PDF. Please make sure it contains selectable text.")
                else:
                    # Run ATS analysis
                    analysis_result = analyze_ats(resume_text, job_desc)
                    
                    # Store in session state
                    st.session_state.ats_analysis = analysis_result
                    st.session_state.extracted_resume_text = resume_text
                    st.session_state.target_job_description = job_desc
                    st.success("Analysis complete!")
                    st.rerun()

    # Display Analysis Dashboard if available
    if "ats_analysis" in st.session_state:
        res = st.session_state.ats_analysis
        st.divider()
        st.markdown("### 📊 ATS Analysis Dashboard")
        
        # Core metric callout
        score = res.get("overall_score", 70)
        
        # Decide badge class
        if score >= 80:
            badge_class = "badge-excellent"
            badge_text = "Excellent Match"
        elif score >= 60:
            badge_class = "badge-good"
            badge_text = "Good Match"
        else:
            badge_class = "badge-needs-improvement"
            badge_text = "Needs Improvement"
            
        score_html = f"""
        <div class="ats-score-container">
            <div class="ats-score-title">OVERALL ATS COMPATIBILITY SCORE</div>
            <div class="ats-score-value">{score}%</div>
            <div class="ats-score-badge {badge_class}">{badge_text}</div>
        </div>
        """
        st.markdown(score_html, unsafe_allow_html=True)
        
        # Sub-scores
        st.markdown("#### Match Breakdown")
        c1, c2, c3, c4 = st.columns(4)
        
        with c1:
            st.metric("Skills Match", f"{res.get('skills_match', 50)}%")
            st.progress(res.get('skills_match', 50) / 100.0)
            
        with c2:
            st.metric("Keyword Match", f"{res.get('keyword_match', 50)}%")
            st.progress(res.get('keyword_match', 50) / 100.0)
            
        with c3:
            st.metric("Experience Match", f"{res.get('experience_match', 50)}%")
            st.progress(res.get('experience_match', 50) / 100.0)
            
        with c4:
            st.metric("Education Match", f"{res.get('education_match', 50)}%")
            st.progress(res.get('education_match', 50) / 100.0)
            
        st.write("")
        st.divider()
        
        # Keywords Section
        st.markdown("#### 🔑 Keyword Analysis")
        col_key1, col_key2 = st.columns(2)
        
        with col_key1:
            st.markdown("##### 🟢 Matched Keywords")
            matched = res.get("matched_keywords", [])
            if matched:
                # Render as pills
                pills = "".join([f'<span style="background-color: #064e3b; color: #a7f3d0; padding: 4px 10px; border-radius: 12px; margin: 4px; display: inline-block; font-size: 13px;">{kw}</span>' for kw in matched])
                st.markdown(pills, unsafe_allow_html=True)
            else:
                st.info("No matching keywords found.")
                
        with col_key2:
            st.markdown("##### 🔴 Missing Keywords")
            missing = res.get("missing_keywords", [])
            if missing:
                pills = "".join([f'<span style="background-color: #7f1d1d; color: #fca5a5; padding: 4px 10px; border-radius: 12px; margin: 4px; display: inline-block; font-size: 13px;">{kw}</span>' for kw in missing])
                st.markdown(pills, unsafe_allow_html=True)
            else:
                st.success("No missing keywords identified!")
                
        st.divider()
        
        # Strengths / Weaknesses / Suggestions
        col_sw1, col_sw2 = st.columns(2)
        
        with col_sw1:
            st.markdown("##### ➕ Strengths")
            strengths = res.get("strengths", [])
            if strengths:
                list_html = '<ul class="strength-list">'
                for strg in strengths:
                    list_html += f"<li>{strg}</li>"
                list_html += "</ul>"
                st.markdown(list_html, unsafe_allow_html=True)
            else:
                st.write("None identified.")
                
        with col_sw2:
            st.markdown("##### ➖ Weaknesses / Gaps")
            weaknesses = res.get("weaknesses", [])
            if weaknesses:
                list_html = '<ul class="weakness-list">'
                for weak in weaknesses:
                    list_html += f"<li>{weak}</li>"
                list_html += "</ul>"
                st.markdown(list_html, unsafe_allow_html=True)
            else:
                st.write("None identified.")
                
        st.divider()
        
        st.markdown("##### 💡 Actionable Improvement Suggestions")
        suggestions = res.get("suggestions", [])
        if suggestions:
            list_html = '<ul class="suggestion-list">'
            for sug in suggestions:
                list_html += f"<li>{sug}</li>"
            list_html += "</ul>"
            st.markdown(list_html, unsafe_allow_html=True)
        else:
            st.write("No specific suggestions.")
            
        st.write("")
        
        # Provide a quick prompt link to Tab 3
        st.info("💡 **Ready to fix these gaps?** Head over to the **AI Resume Optimizer** tab to generate optimized resume fields instantly based on these suggestions.")
