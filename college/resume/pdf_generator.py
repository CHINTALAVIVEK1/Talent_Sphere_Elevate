from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
import json

def generate_resume_pdf(resume_data, filename="Resume.pdf"):
    """
    Generates a professional, ATS-friendly resume PDF using ReportLab.
    """
    # 72 points = 1 inch. letter size is 612 x 792 points.
    # Margins: 36 points (0.5 inch) all sides. Printable width = 612 - 72 = 540.
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    # Primary: Dark Navy (#1e3a8a), Secondary: Charcoal (#334155), Body: Off-black (#1e293b)
    primary_color = colors.HexColor("#1e3a8a")
    secondary_color = colors.HexColor("#334155")
    text_color = colors.HexColor("#1e293b")
    
    name_style = ParagraphStyle(
        "ResumeName",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=26,
        textColor=primary_color,
        alignment=1 # Centered
    )
    
    contact_style = ParagraphStyle(
        "ResumeContact",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=secondary_color,
        alignment=1 # Centered
    )
    
    header_style = ParagraphStyle(
        "ResumeHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=primary_color
    )
    
    body_style = ParagraphStyle(
        "ResumeBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=text_color
    )
    
    bold_body_style = ParagraphStyle(
        "ResumeBoldBody",
        parent=body_style,
        fontName="Helvetica-Bold"
    )
    
    italic_body_style = ParagraphStyle(
        "ResumeItalicBody",
        parent=body_style,
        fontName="Helvetica-Oblique"
    )

    story = []
    
    # --- 1. HEADER (NAME & CONTACT) ---
    name = resume_data.get("full_name", "Student Name").strip()
    story.append(Paragraph(name, name_style))
    story.append(Spacer(1, 4))
    
    contact_parts = []
    email = resume_data.get("email", "").strip()
    phone = resume_data.get("phone", "").strip()
    linkedin = resume_data.get("linkedin", "").strip()
    github = resume_data.get("github", "").strip()
    address = resume_data.get("address", "").strip()
    
    if email: contact_parts.append(email)
    if phone: contact_parts.append(phone)
    if linkedin: contact_parts.append(f"LinkedIn: {linkedin}")
    if github: contact_parts.append(f"GitHub: {github}")
    if address: contact_parts.append(address)
    
    contact_text = "  |  ".join(contact_parts)
    story.append(Paragraph(contact_text, contact_style))
    story.append(Spacer(1, 10))
    
    # Section Heading helper
    def add_section_header(title):
        tbl = Table([[Paragraph(f"<b>{title.upper()}</b>", header_style)]], colWidths=[540])
        tbl.setStyle(TableStyle([
            ('LINEBELOW', (0,0), (-1,-1), 1, primary_color),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 6))

    # --- 2. OBJECTIVE ---
    objective = resume_data.get("career_objective", "").strip()
    if objective:
        add_section_header("Career Objective")
        story.append(Paragraph(objective, body_style))
        story.append(Spacer(1, 8))
        
    # --- 3. EDUCATION ---
    college = resume_data.get("college", "").strip()
    degree = resume_data.get("degree", "").strip()
    branch = resume_data.get("branch", "").strip()
    cgpa = resume_data.get("cgpa", "").strip()
    grad_year = resume_data.get("graduation_year", "").strip()
    
    if college or degree or branch:
        add_section_header("Education")
        edu_details = []
        if degree and branch:
            edu_details.append(f"<b>{degree} in {branch}</b>")
        elif degree:
            edu_details.append(f"<b>{degree}</b>")
        elif branch:
            edu_details.append(f"<b>{branch}</b>")
            
        if college:
            edu_details.append(college)
            
        edu_left = "<br/>".join(edu_details)
        
        edu_right_parts = []
        if grad_year:
            edu_right_parts.append(f"Graduation: {grad_year}")
        if cgpa:
            edu_right_parts.append(f"CGPA/Percentage: {cgpa}")
            
        edu_right = "<br/>".join(edu_right_parts)
        
        edu_table_data = [
            [Paragraph(edu_left, body_style), Paragraph(edu_right, ParagraphStyle("EduRight", parent=body_style, alignment=2))]
        ]
        
        edu_table = Table(edu_table_data, colWidths=[380, 160])
        edu_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(edu_table)
        story.append(Spacer(1, 8))
        
    # --- 4. SKILLS ---
    skills = resume_data.get("skills", [])
    if skills:
        add_section_header("Technical Skills")
        skills_text = ", ".join(skills)
        story.append(Paragraph(skills_text, body_style))
        story.append(Spacer(1, 8))
        
    # --- 5. EXPERIENCE ---
    experience = resume_data.get("experience", [])
    if experience:
        add_section_header("Professional Experience")
        for i, exp in enumerate(experience):
            company = exp.get("company", "").strip()
            role = exp.get("role", "").strip()
            duration = exp.get("duration", "").strip()
            desc = exp.get("description", "").strip()
            
            if company or role:
                exp_left = f"<b>{role}</b> at <b>{company}</b>"
                exp_right = duration
                
                exp_header_table = Table([
                    [Paragraph(exp_left, body_style), Paragraph(exp_right, ParagraphStyle("ExpRight", parent=body_style, alignment=2))]
                ], colWidths=[400, 140])
                exp_header_table.setStyle(TableStyle([
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('LEFTPADDING', (0,0), (-1,-1), 0),
                    ('RIGHTPADDING', (0,0), (-1,-1), 0),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 0),
                    ('TOPPADDING', (0,0), (-1,-1), 0),
                ]))
                story.append(exp_header_table)
                story.append(Spacer(1, 2))
                
                if desc:
                    # Render description lines as bullet list elements if separated by newlines
                    desc_lines = [line.strip().lstrip("•-* ") for line in desc.split("\n") if line.strip()]
                    for d_line in desc_lines:
                        bullet_p = Paragraph(f"• {d_line}", ParagraphStyle("ExpDesc", parent=body_style, leftIndent=12, firstLineIndent=-8))
                        story.append(bullet_p)
                story.append(Spacer(1, 6))
        story.append(Spacer(1, 2))
        
    # --- 6. PROJECTS ---
    projects = resume_data.get("projects", [])
    if projects:
        add_section_header("Academic & Personal Projects")
        for proj in projects:
            title = proj.get("title", "").strip()
            tech = proj.get("technologies", "").strip()
            link = proj.get("github_link", "").strip()
            desc = proj.get("description", "").strip()
            
            if title:
                proj_title = f"<b>{title}</b>"
                if tech:
                    proj_title += f" <i>({tech})</i>"
                
                proj_right = f"<font color='#1e3a8a'>{link}</font>" if link else ""
                
                proj_header_table = Table([
                    [Paragraph(proj_title, body_style), Paragraph(proj_right, ParagraphStyle("ProjRight", parent=body_style, alignment=2))]
                ], colWidths=[380, 160])
                proj_header_table.setStyle(TableStyle([
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('LEFTPADDING', (0,0), (-1,-1), 0),
                    ('RIGHTPADDING', (0,0), (-1,-1), 0),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 0),
                    ('TOPPADDING', (0,0), (-1,-1), 0),
                ]))
                story.append(proj_header_table)
                story.append(Spacer(1, 2))
                
                if desc:
                    desc_lines = [line.strip().lstrip("•-* ") for line in desc.split("\n") if line.strip()]
                    for d_line in desc_lines:
                        bullet_p = Paragraph(f"• {d_line}", ParagraphStyle("ProjDesc", parent=body_style, leftIndent=12, firstLineIndent=-8))
                        story.append(bullet_p)
                story.append(Spacer(1, 6))
        story.append(Spacer(1, 2))
        
    # --- 7. CERTIFICATIONS ---
    certifications = resume_data.get("certifications", [])
    if certifications:
        add_section_header("Certifications")
        for cert in certifications:
            if cert.strip():
                story.append(Paragraph(f"• {cert.strip()}", ParagraphStyle("CertBullet", parent=body_style, leftIndent=12, firstLineIndent=-8)))
        story.append(Spacer(1, 8))
        
    # --- 8. LANGUAGES ---
    languages = resume_data.get("languages", [])
    if languages:
        add_section_header("Languages")
        langs_text = ", ".join(languages)
        story.append(Paragraph(langs_text, body_style))
        story.append(Spacer(1, 8))
        
    # Build Document
    try:
        doc.build(story)
    except Exception as e:
        print(f"Error building PDF: {e}")
        # Build simple fallback document in case of layout pagebreak exceptions
        doc.build([Paragraph("Error generating PDF: " + str(e), body_style)])
        
    return filename
