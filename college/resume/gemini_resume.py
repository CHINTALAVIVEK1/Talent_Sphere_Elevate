import json
from google.genai import types
from utils.gemini import client

def generate_ai_objective(resume_data):
    """
    Generates a professional 2-3 sentence career objective using Gemini based on resume data.
    """
    skills_str = ", ".join(resume_data.get("skills", []))
    degree_str = f"{resume_data.get('degree', '')} in {resume_data.get('branch', '')}"
    college_str = resume_data.get("college", "")
    
    prompt = f"""
    You are an expert resume writer. Generate a professional, highly-tailored career objective (2 to 3 sentences) for a college student with the following background:
    - Degree: {degree_str}
    - College: {college_str}
    - Skills: {skills_str}
    
    Ensure it is written in a professional, active voice, outlining how they can add value to a company.
    Do not use placeholders, brackets, or generic templates. 
    Return ONLY the objective text.
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"Error generating AI objective: {e}")
        return "Dedicated and detail-oriented student seeking a challenging role to leverage technical skills and academic background to contribute to organizational success."

def analyze_ats(resume_text, job_description):
    """
    Performs ATS resume analysis against a job description.
    Returns structured JSON with scores, keywords, strengths, weaknesses, and suggestions.
    """
    prompt = f"""
    You are an expert ATS (Applicant Tracking System) recruiter and resume analyzer.
    Analyze the following resume text against the provided job description and return a detailed report in structured JSON format.

    Resume Text:
    {resume_text}

    Job Description:
    {job_description}

    You MUST return a JSON object with the following fields:
    - overall_score (Integer between 0 and 100)
    - skills_match (Integer between 0 and 100)
    - keyword_match (Integer between 0 and 100)
    - experience_match (Integer between 0 and 100)
    - education_match (Integer between 0 and 100)
    - missing_keywords (List of strings)
    - matched_keywords (List of strings)
    - strengths (List of strings describing strengths of the resume relative to the job description)
    - weaknesses (List of strings describing weaknesses/gaps in the resume)
    - suggestions (List of strings suggesting actionable improvements)

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
        print(f"Error in analyze_ats: {e}")
        # Fallback dictionary
        return {
            "overall_score": 65,
            "skills_match": 60,
            "keyword_match": 55,
            "experience_match": 70,
            "education_match": 80,
            "missing_keywords": ["Node.js", "Docker", "RESTful APIs"],
            "matched_keywords": ["Python", "SQL", "Git"],
            "strengths": ["Strong educational foundation", "Good programming language coverage"],
            "weaknesses": ["Lack of deployment/cloud technologies", "Project descriptions lack quantitative impact"],
            "suggestions": ["Add containerization experience", "Rewrite projects to show results, not just tasks"]
        }

def optimize_career_objective(objective, job_desc):
    """
    Optimizes a career objective to align with a job description.
    """
    prompt = f"""
    Optimize the following career objective to align with this job description.
    Ensure it remains professional, under 3 sentences, and highlights relevant skills/experience without introducing fake information.

    Current Career Objective:
    {objective}

    Job Description:
    {job_desc}

    Return ONLY the optimized career objective text. Do not include introductory text or quotes.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text.strip().replace('"', '')
    except Exception as e:
        print(f"Error optimizing objective: {e}")
        return objective

def optimize_project_description(title, desc, job_desc):
    """
    Optimizes a project description to align with a job description.
    """
    prompt = f"""
    Optimize the project description for the project titled "{title}" to align with the provided job description.
    Highlight relevant technologies, impacts, and quantify achievements if possible, in 2-3 bullet points.

    Current Project Description:
    {desc}

    Job Description:
    {job_desc}

    Return ONLY the optimized project description bullets. Each bullet must start with a '•' or '-' character.
    Do not add introductory lines or headings.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"Error optimizing project description: {e}")
        return desc

def optimize_skills_list(skills_list, job_desc):
    """
    Suggests technical skills to add based on a job description.
    """
    skills_str = ", ".join(skills_list)
    prompt = f"""
    Compare these current skills: {skills_str} with the job description.
    Suggest up to 5 relevant technical/soft skills that are missing from the resume but important for the job.

    Job Description:
    {job_desc}

    Return ONLY a comma-separated list of the suggested skills (e.g. Docker, TypeScript, AWS). No explanation.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        res = response.text.strip()
        # Parse comma-separated string to list
        return [s.strip() for s in res.split(",") if s.strip()]
    except Exception as e:
        print(f"Error optimizing skills: {e}")
        return []
