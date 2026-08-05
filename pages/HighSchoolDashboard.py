import streamlit as st
from utils.report import generate_student_report


st.set_page_config(
    page_title="High School Dashboard",
    layout="wide"
)

st.markdown("""
<style>
[data-testid="stSidebarNav"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)



# ---------------- LOGIN CHECK ---------------- #

if not st.session_state.get("logged_in"):
    st.warning("Please login first.")
    if st.button("Go to Login Page"):
        st.switch_page("pages/Login.py")
    st.stop()

user = st.session_state.user_name

# ---------------- MODULE STATE ---------------- #

if "module" not in st.session_state:
    st.session_state.module = "home"


# ---------------- HEADER ---------------- #

col1, col2 = st.columns([1,6])

with col1:
    st.image("assets/logo.png", width=90)

with col2:
    st.title("TalentSphere Elevate")
    st.caption("AI-Powered Career Development Platform")

st.divider()

# ---------------- BANNER ---------------- #

st.image("assets/HighSchool.png", use_container_width=True)

st.write("")

# ---------------- WELCOME ---------------- #

col1, col2 = st.columns([3,2])

with col1:
    st.subheader(f"Welcome, {user}")
    st.write("High School Student")

with col2:
    st.info("Career Stage : Beginner")

st.divider()

# ---------------- DASHBOARD OVERVIEW ---------------- #
st.divider()

if st.button("📄 Generate Student Report", use_container_width=True):

    pdf = generate_student_report(
        st.session_state.user_name
    )

    with open(pdf, "rb") as file:

        st.download_button(
            "⬇ Download Report",
            file,
            file_name=pdf,
            mime="application/pdf",
            use_container_width=True
        )


        
st.subheader("Dashboard Overview")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Learning Progress", "25%")

with c2:
    st.metric("Career Readiness", "Beginner")

with c3:
    st.metric("Tasks Completed", "3")

with c4:
    st.metric("Quiz Score", "80%")

st.divider()

# ---------------- QUICK ACCESS ---------------- #

left, right = st.columns([1,4])

with left:

    st.subheader("Navigation")

    if st.button("Dashboard", use_container_width=True):
        st.session_state.module = "home"

    if st.button("Career Explorer", use_container_width=True):
        st.session_state.module = "career"

    if st.button("AI Career Quiz", use_container_width=True):
        st.session_state.module = "quiz"

    if st.button("Interest Assessment", use_container_width=True):
        st.session_state.module = "interest"

    if st.button("Future Skills Roadmap", use_container_width=True):
        st.session_state.module = "roadmap"

    if st.button("Daily Learning Tasks", use_container_width=True):
        st.session_state.module = "daily"

    if st.button("Coding Basics", use_container_width=True):
        st.session_state.module = "coding"

    if st.button("Aptitude Practice", use_container_width=True):
        st.session_state.module = "aptitude"

    if st.button("Communication Skills", use_container_width=True):
        st.session_state.module = "communication"

    if st.button("Goal Tracker", use_container_width=True):
        st.session_state.module = "goal"

    if st.button("AI Mentor", use_container_width=True):
        st.session_state.module = "mentor"

    st.divider()

    if st.button("Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("app.py")

with right:


    # ---------------- CONTENT AREA ---------------- #

    if st.session_state.module == "home":

        st.subheader("Today's Learning Tasks")

        tasks = [
            "Learn Python Basics",
            "Complete Career Quiz",
            "Solve 5 Aptitude Questions"
        ]

        for i, task in enumerate(tasks):
            st.checkbox(task, key=f"home_task_{i}")

        st.divider()

        st.subheader("Career Recommendation")

        st.info("""
    Recommended Career

    Artificial Intelligence Engineer

    Reason

    • Interested in Computers

    • Strong Mathematics

    • Good Logical Thinking

    Skills to Learn

    • Python

    • Mathematics

    • Communication

    • Problem Solving
    """)

        st.divider()

        st.subheader("Recent Activities")

        activities = [
            "Welcome to TalentSphere Elevate",
            "Profile Created Successfully",
            "Dashboard Initialized"
        ]

        for activity in activities:
            st.write("•", activity)

    # ---------------- CAREER EXPLORER ---------------- #

    elif st.session_state.module == "career":

        st.subheader("Career Explorer")

        st.write("Explore different career options available after school.")

        careers = [
            "Artificial Intelligence Engineer",
            "Software Developer",
            "Doctor",
            "Teacher",
            "Civil Engineer",
            "Architect",
            "Graphic Designer",
            "Business Analyst"
        ]

        selected = st.selectbox(
            "Choose a Career",
            careers
        )

        if selected == "Artificial Intelligence Engineer":

            st.markdown("### Career Overview")

            st.write(
                "AI Engineers develop intelligent systems capable of learning, decision making and automation."
            )

            st.markdown("### Required Skills")

            st.write("- Python")
            st.write("- Mathematics")
            st.write("- Machine Learning")
            st.write("- Problem Solving")

            st.markdown("### Subjects to Focus")

            st.write("- Mathematics")
            st.write("- Computer Science")
            st.write("- Physics")

            st.markdown("### Future Scope")

            st.write(
                "Artificial Intelligence is one of the fastest growing industries with opportunities in healthcare, finance, robotics and education."
            )

            st.markdown("### Suggested Learning Path")

            st.write(
                "Python → Mathematics → Machine Learning → AI Projects"
            )

        elif selected == "Software Developer":

            st.markdown("### Career Overview")

            st.write(
                "Software Developers create websites, mobile applications and software systems."
            )

            st.markdown("### Required Skills")

            st.write("- Programming")
            st.write("- HTML")
            st.write("- CSS")
            st.write("- Python")

            st.markdown("### Subjects to Focus")

            st.write("- Computer Science")
            st.write("- Mathematics")

            st.markdown("### Future Scope")

            st.write(
                "Software Developers are required in almost every industry including technology, banking and healthcare."
            )

            st.markdown("### Suggested Learning Path")

            st.write(
                "HTML → CSS → Python → Projects"
            )
        elif selected == "Doctor":

            st.markdown("### Career Overview")

            st.write(
                "Doctors diagnose diseases, treat patients and help improve people's health through medical care."
            )

            st.markdown("### Roles & Responsibilities")

            st.write("- Diagnose illnesses")
            st.write("- Prescribe medicines")
            st.write("- Perform surgeries (specialists)")
            st.write("- Guide patients towards healthy living")

            st.markdown("### Required Skills")

            st.write("- Biology Knowledge")
            st.write("- Communication")
            st.write("- Decision Making")
            st.write("- Patience")

            st.markdown("### Subjects to Focus")

            st.write("- Biology")
            st.write("- Chemistry")
            st.write("- Physics")

            st.markdown("### Higher Education")

            st.write("MBBS → MD/MS → Super Specialization (Optional)")

            st.markdown("### Career Opportunities")

            st.write("- Government Hospitals")
            st.write("- Private Hospitals")
            st.write("- Clinics")
            st.write("- Research Institutes")

            st.markdown("### Future Scope")

            st.write(
                "Healthcare is one of the fastest growing sectors with increasing demand for qualified doctors."
            )

            st.markdown("### Average Salary")

            st.write("₹8 LPA - ₹40 LPA")

            st.markdown("### Top Recruiters")

            st.write("- Apollo Hospitals")
            st.write("- AIIMS")
            st.write("- Fortis")
            st.write("- Government Hospitals")

            st.markdown("### Suggested Learning Path")

            st.write("NEET → MBBS → Internship → Practice")


        elif selected == "Teacher":

            st.markdown("### Career Overview")

            st.write(
                "Teachers educate students and help them develop academic, social and practical skills."
            )

            st.markdown("### Roles & Responsibilities")

            st.write("- Teach subjects")
            st.write("- Prepare lesson plans")
            st.write("- Evaluate students")
            st.write("- Guide career development")

            st.markdown("### Required Skills")

            st.write("- Communication")
            st.write("- Leadership")
            st.write("- Subject Knowledge")
            st.write("- Patience")

            st.markdown("### Subjects to Focus")

            st.write("- English")
            st.write("- Mathematics")
            st.write("- Subject of Interest")

            st.markdown("### Higher Education")

            st.write("Bachelor's Degree → B.Ed → M.Ed (Optional)")

            st.markdown("### Career Opportunities")

            st.write("- Government Schools")
            st.write("- Private Schools")
            st.write("- Colleges")
            st.write("- Online Teaching")

            st.markdown("### Future Scope")

            st.write(
                "Teaching remains one of the most respected professions with steady career opportunities."
            )

            st.markdown("### Average Salary")

            st.write("₹3 LPA - ₹12 LPA")

            st.markdown("### Top Recruiters")

            st.write("- Kendriya Vidyalaya")
            st.write("- Navodaya Schools")
            st.write("- State Government Schools")
            st.write("- Private Institutions")

            st.markdown("### Suggested Learning Path")

            st.write("Degree → B.Ed → Teacher Eligibility Test")


        elif selected == "Civil Engineer":

            st.markdown("### Career Overview")

            st.write(
                "Civil Engineers design, build and maintain roads, bridges, buildings and other infrastructure."
            )

            st.markdown("### Roles & Responsibilities")

            st.write("- Design structures")
            st.write("- Manage construction")
            st.write("- Estimate project costs")
            st.write("- Ensure safety standards")

            st.markdown("### Required Skills")

            st.write("- Mathematics")
            st.write("- AutoCAD")
            st.write("- Project Management")
            st.write("- Problem Solving")

            st.markdown("### Subjects to Focus")

            st.write("- Mathematics")
            st.write("- Physics")
            st.write("- Engineering Drawing")

            st.markdown("### Higher Education")

            st.write("B.Tech Civil Engineering → M.Tech (Optional)")

            st.markdown("### Career Opportunities")

            st.write("- Construction Companies")
            st.write("- Government Departments")
            st.write("- Metro Projects")
            st.write("- Real Estate")

            st.markdown("### Future Scope")

            st.write(
                "Infrastructure development continues to create strong demand for Civil Engineers."
            )

            st.markdown("### Average Salary")

            st.write("₹4 LPA - ₹18 LPA")

            st.markdown("### Top Recruiters")

            st.write("- L&T")
            st.write("- NCC")
            st.write("- Tata Projects")
            st.write("- Government Organizations")

            st.markdown("### Suggested Learning Path")

            st.write("JEE → B.Tech Civil → Internship → Site Engineer")
        elif selected == "Architect":

            st.markdown("### Career Overview")

            st.write(
                "Architects design residential, commercial and public buildings by combining creativity with engineering principles."
            )

            st.markdown("### Roles & Responsibilities")

            st.write("- Design buildings")
            st.write("- Prepare architectural drawings")
            st.write("- Meet clients")
            st.write("- Supervise construction")

            st.markdown("### Required Skills")

            st.write("- Creativity")
            st.write("- AutoCAD")
            st.write("- 3D Design")
            st.write("- Mathematics")

            st.markdown("### Subjects to Focus")

            st.write("- Mathematics")
            st.write("- Physics")
            st.write("- Drawing")

            st.markdown("### Higher Education")

            st.write("B.Arch → M.Arch (Optional)")

            st.markdown("### Career Opportunities")

            st.write("- Architecture Firms")
            st.write("- Construction Companies")
            st.write("- Government Projects")
            st.write("- Interior Design")

            st.markdown("### Future Scope")

            st.write(
                "Rapid urban development creates continuous demand for skilled architects."
            )

            st.markdown("### Average Salary")

            st.write("₹5 LPA - ₹20 LPA")

            st.markdown("### Top Recruiters")

            st.write("- L&T")
            st.write("- DLF")
            st.write("- Prestige Group")
            st.write("- Shapoorji Pallonji")

            st.markdown("### Suggested Learning Path")

            st.write("NATA → B.Arch → Internship → Licensed Architect")


        elif selected == "Graphic Designer":

            st.markdown("### Career Overview")

            st.write(
                "Graphic Designers create visual content for advertisements, websites, social media and branding."
            )

            st.markdown("### Roles & Responsibilities")

            st.write("- Design logos")
            st.write("- Create posters")
            st.write("- Design social media posts")
            st.write("- Branding")

            st.markdown("### Required Skills")

            st.write("- Creativity")
            st.write("- Photoshop")
            st.write("- Illustrator")
            st.write("- UI Design Basics")

            st.markdown("### Subjects to Focus")

            st.write("- Computer Science")
            st.write("- Arts")
            st.write("- Multimedia")

            st.markdown("### Higher Education")

            st.write("B.Des / BFA / Graphic Design Courses")

            st.markdown("### Career Opportunities")

            st.write("- Advertising Agencies")
            st.write("- IT Companies")
            st.write("- Freelancing")
            st.write("- Digital Marketing")

            st.markdown("### Future Scope")

            st.write(
                "The digital marketing industry has increased demand for skilled graphic designers."
            )

            st.markdown("### Average Salary")

            st.write("₹4 LPA - ₹15 LPA")

            st.markdown("### Top Recruiters")

            st.write("- TCS")
            st.write("- Infosys")
            st.write("- Amazon")
            st.write("- Design Studios")

            st.markdown("### Suggested Learning Path")

            st.write("Photoshop → Illustrator → Figma → Portfolio")


        elif selected == "Business Analyst":

            st.markdown("### Career Overview")

            st.write(
                "Business Analysts identify business problems and recommend technology-driven solutions."
            )

            st.markdown("### Roles & Responsibilities")

            st.write("- Gather requirements")
            st.write("- Analyze business data")
            st.write("- Improve processes")
            st.write("- Communicate with stakeholders")

            st.markdown("### Required Skills")

            st.write("- Communication")
            st.write("- SQL")
            st.write("- Excel")
            st.write("- Data Analysis")

            st.markdown("### Subjects to Focus")

            st.write("- Mathematics")
            st.write("- Economics")
            st.write("- Computer Science")

            st.markdown("### Higher Education")

            st.write("B.Tech / BBA → MBA (Optional)")

            st.markdown("### Career Opportunities")

            st.write("- IT Companies")
            st.write("- Banks")
            st.write("- Consulting Firms")
            st.write("- Product Companies")

            st.markdown("### Future Scope")

            st.write(
                "Every growing company requires Business Analysts for strategic decision making."
            )

            st.markdown("### Average Salary")

            st.write("₹6 LPA - ₹20 LPA")

            st.markdown("### Top Recruiters")

            st.write("- Deloitte")
            st.write("- Accenture")
            st.write("- Infosys")
            st.write("- Cognizant")

            st.markdown("### Suggested Learning Path")

            st.write("Excel → SQL → Power BI → Business Analytics")

        

        else:

            st.info(
                "Details for this career will be added in upcoming phases."
            )

        if st.button("Back to Dashboard"):

            st.session_state.module = "home"
            st.rerun()



    # ---------------- AI CAREER QUIZ ---------------- #

    elif st.session_state.module == "quiz":

        st.header("Career Quiz")

        st.write(
            "Answer the following questions to discover careers that best match your interests."
        )

        st.divider()

        questions = [

            {
                "question":"1. Which subject do you enjoy the most?",
                "options":["Mathematics","Science","Arts","Commerce"]
            },

            {
                "question":"2. Which activity do you enjoy?",
                "options":["Coding","Drawing","Helping People","Managing Money"]
            },

            {
                "question":"3. What type of problems do you like solving?",
                "options":["Logical","Creative","Social","Business"]
            },

            {
                "question":"4. Which environment do you prefer?",
                "options":["Office","Hospital","Outdoor","Studio"]
            },

            {
                "question":"5. Which skill describes you best?",
                "options":["Analytical","Creative","Leadership","Communication"]
            },

            {
                "question":"6. What motivates you?",
                "options":["Innovation","Helping Others","Money","Creativity"]
            },

            {
                "question":"7. Which hobby do you enjoy?",
                "options":["Programming","Painting","Reading","Sports"]
            },

            {
                "question":"8. Which school activity do you like?",
                "options":["Science Fair","Drama","Debate","Sports"]
            },

            {
                "question":"9. What do you prefer?",
                "options":["Technology","Medicine","Business","Design"]
            },

            {
                "question":"10. How do you solve problems?",
                "options":["Logic","Creativity","Discussion","Research"]
            }

        ]

        if "quiz_answers" not in st.session_state:
            st.session_state.quiz_answers = {}

        score = {
            "Artificial Intelligence Engineer":0,
            "Software Developer":0,
            "Doctor":0,
            "Teacher":0,
            "Civil Engineer":0,
            "Architect":0,
            "Graphic Designer":0,
            "Business Analyst":0
        }

        for i, q in enumerate(questions):

            answer = st.radio(
                q["question"],
                q["options"],
                key=f"quiz_{i}"
            )

            st.session_state.quiz_answers[i] = answer

        st.divider()

        if st.button("Generate Career Recommendation", use_container_width=True):

            for answer in st.session_state.quiz_answers.values():

                if answer in ["Mathematics","Coding","Logical","Technology","Programming","Innovation"]:
                    score["Artificial Intelligence Engineer"] += 2
                    score["Software Developer"] += 2

                if answer in ["Science","Helping People","Hospital","Medicine","Research"]:
                    score["Doctor"] += 2

                if answer in ["Communication","Reading","Discussion"]:
                    score["Teacher"] += 2

                if answer in ["Outdoor"]:
                    score["Civil Engineer"] += 2

                if answer in ["Creative","Drawing","Design","Painting","Studio"]:
                    score["Architect"] += 2
                    score["Graphic Designer"] += 2

                if answer in ["Business","Managing Money","Leadership"]:
                    score["Business Analyst"] += 2

            best = max(score, key=score.get)

            st.success(f"Recommended Career : {best}")

            st.divider()

            if best == "Artificial Intelligence Engineer":

                st.markdown("### Why this career?")

                st.write("""
    You enjoy technology, logical thinking and solving complex problems.

    Artificial Intelligence is one of the fastest-growing fields and offers excellent career opportunities.
                """)

                st.markdown("### Skills to Learn")

                st.write("- Python")
                st.write("- Mathematics")
                st.write("- Machine Learning")
                st.write("- Communication")

            elif best == "Software Developer":

                st.markdown("### Why this career?")

                st.write("""
    You enjoy programming, technology and creating software solutions.

    Software Developers build websites, mobile apps and enterprise applications.
                """)

                st.markdown("### Skills to Learn")

                st.write("- HTML")
                st.write("- CSS")
                st.write("- Python")
                st.write("- Git")

            elif best == "Doctor":

                st.markdown("### Why this career?")

                st.write("""
    You enjoy helping people and have strong interest in science.

    A medical career allows you to improve lives through healthcare.
                """)

                st.markdown("### Skills to Learn")

                st.write("- Biology")
                st.write("- Communication")
                st.write("- Patience")

            elif best == "Teacher":

                st.markdown("### Why this career?")

                st.write("""
    You enjoy sharing knowledge and communicating with others.

    Teaching is a respected profession with long-term opportunities.
                """)

            elif best == "Civil Engineer":

                st.markdown("### Why this career?")

                st.write("""
    You enjoy infrastructure, construction and solving real-world engineering problems.
                """)

            elif best == "Architect":

                st.markdown("### Why this career?")

                st.write("""
    You have creativity and enjoy designing buildings and spaces.
                """)

            elif best == "Graphic Designer":

                st.markdown("### Why this career?")

                st.write("""
    You enjoy creativity, design and visual storytelling.
                """)

            elif best == "Business Analyst":

                st.markdown("### Why this career?")

                st.write("""
    You enjoy solving business problems using analytical thinking.
                """)

            st.divider()

            st.subheader("Career Match Score")

            for career, value in sorted(score.items(), key=lambda x: x[1], reverse=True):

                st.write(career)

                st.progress(min(value/10,1.0))

        st.divider()

        c1, c2 = st.columns(2)

        with c1:

            if st.button("Restart Quiz", use_container_width=True):

                for i in range(len(questions)):
                    if f"quiz_{i}" in st.session_state:
                        del st.session_state[f"quiz_{i}"]

                st.session_state.quiz_answers = {}

                st.rerun()

        with c2:

            if st.button("Back to Dashboard", use_container_width=True):

                st.session_state.module = "home"

                st.rerun()



# ---------------- INTEREST ASSESSMENT ---------------- #

    elif st.session_state.module == "interest":

        st.header("Interest Assessment")

        st.write(
            "Answer the following questions honestly to discover your strongest career interests."
        )

        st.divider()

        questions = [

            ("1. I enjoy solving mathematical problems.", "Technology"),
            ("2. I like helping sick or injured people.", "Healthcare"),
            ("3. I enjoy drawing and designing.", "Creative"),
            ("4. I like managing money and planning.", "Business"),
            ("5. I enjoy building machines or structures.", "Engineering"),
            ("6. I enjoy programming computers.", "Technology"),
            ("7. Biology is my favourite subject.", "Healthcare"),
            ("8. I enjoy photography or video editing.", "Creative"),
            ("9. I like leading a team.", "Business"),
            ("10. I enjoy fixing things.", "Engineering"),
            ("11. I like learning new technologies.", "Technology"),
            ("12. I enjoy volunteering and helping others.", "Healthcare"),
            ("13. I enjoy painting or sketching.", "Creative"),
            ("14. I like starting new business ideas.", "Business"),
            ("15. Physics is one of my favourite subjects.", "Engineering")

        ]

        if "interest_answers" not in st.session_state:
            st.session_state.interest_answers = {}

        scores = {
            "Technology":0,
            "Healthcare":0,
            "Creative":0,
            "Business":0,
            "Engineering":0
        }

        for i, (question, category) in enumerate(questions):

            answer = st.radio(
                question,
                ["Strongly Agree",
                "Agree",
                "Neutral",
                "Disagree",
                "Strongly Disagree"],
                key=f"interest_{i}"
            )

            st.session_state.interest_answers[i] = (answer, category)

        st.divider()

        if st.button("Analyze My Interests", use_container_width=True):

            for answer, category in st.session_state.interest_answers.values():

                if answer == "Strongly Agree":
                    scores[category] += 5

                elif answer == "Agree":
                    scores[category] += 4

                elif answer == "Neutral":
                    scores[category] += 3

                elif answer == "Disagree":
                    scores[category] += 2

                else:
                    scores[category] += 1

            ranking = sorted(
                scores.items(),
                key=lambda x: x[1],
                reverse=True
            )

            st.success("Assessment Completed Successfully")

            st.divider()

            st.subheader("Your Interest Profile")

            for area, score in ranking:

                st.write(f"**{area}**")

                st.progress(score/75)

                st.write(f"Score : {score}/75")

            st.divider()

            top = ranking[0][0]

            st.subheader("Recommended Domain")

            st.success(top)

# ---------------- FUTURE SKILLS ROADMAP ---------------- #

    elif st.session_state.module == "roadmap":

        st.header("Future Skills Roadmap")

        st.write("Select your dream career to view the complete learning roadmap.")

        careers = [
            "Artificial Intelligence Engineer",
            "Software Developer",
            "Doctor",
            "Teacher",
            "Civil Engineer",
            "Architect",
            "Graphic Designer",
            "Business Analyst"
        ]

        career = st.selectbox("Choose Career", careers)

        st.divider()

        if career == "Artificial Intelligence Engineer":

            st.success("Career Goal : Artificial Intelligence Engineer")

            st.subheader("📍 Stage 1 : High School")

            st.checkbox("Master Mathematics")
            st.checkbox("Learn Python Basics")
            st.checkbox("Improve Logical Thinking")
            st.checkbox("Participate in Science Competitions")

            st.divider()

            st.subheader("📍 Stage 2 : College")

            st.checkbox("Data Structures & Algorithms")
            st.checkbox("Machine Learning")
            st.checkbox("Deep Learning")
            st.checkbox("Build AI Projects")
            st.checkbox("Complete Internship")

            st.divider()

            st.subheader("📍 Stage 3 : Career")

            st.checkbox("Build Portfolio")
            st.checkbox("Prepare Resume")
            st.checkbox("Practice Interviews")
            st.checkbox("Apply for AI Jobs")

            st.divider()

            st.subheader("Top Skills")

            st.progress(0.95)
            st.write("★★★★★ Python")

            st.progress(0.90)
            st.write("★★★★★ Mathematics")

            st.progress(0.85)
            st.write("★★★★☆ Machine Learning")

            st.progress(0.80)
            st.write("★★★★☆ Communication")

            st.divider()

            st.subheader("Recommended Certifications")

            st.write("• Google AI Essentials")
            st.write("• IBM Python for Data Science")
            st.write("• Microsoft AI Fundamentals")

            st.divider()

            st.metric("Estimated Learning Journey", "5 - 7 Years")

        elif career == "Software Developer":

            st.success("Career Goal : Software Developer")

            st.subheader("📍 Stage 1 : High School")

            st.checkbox("Learn Computer Basics")
            st.checkbox("Python Programming")
            st.checkbox("Problem Solving")

            st.divider()

            st.subheader("📍 Stage 2 : College")

            st.checkbox("HTML")
            st.checkbox("CSS")
            st.checkbox("JavaScript")
            st.checkbox("Data Structures")
            st.checkbox("Database Management")

            st.divider()

            st.subheader("📍 Stage 3 : Career")

            st.checkbox("Full Stack Projects")
            st.checkbox("Git & GitHub")
            st.checkbox("Resume")
            st.checkbox("Internship")

            st.divider()

            st.subheader("Top Skills")

            st.progress(0.95)
            st.write("★★★★★ Programming")

            st.progress(0.90)
            st.write("★★★★★ JavaScript")

            st.progress(0.85)
            st.write("★★★★☆ Problem Solving")

            st.progress(0.80)
            st.write("★★★★☆ Communication")

            st.divider()

            st.subheader("Recommended Certifications")

            st.write("• Meta Front-End")
            st.write("• Google IT Automation")
            st.write("• IBM Full Stack")

            st.metric("Estimated Learning Journey", "4 - 6 Years")

        elif career == "Doctor":

            st.success("Career Goal : Doctor")

            st.subheader("📍 Stage 1 : High School")

            st.checkbox("Focus on Biology")
            st.checkbox("Chemistry")
            st.checkbox("Physics")
            st.checkbox("Prepare for NEET")

            st.divider()

            st.subheader("📍 Stage 2 : Medical College")

            st.checkbox("MBBS")
            st.checkbox("Clinical Practice")
            st.checkbox("Internship")

            st.divider()

            st.subheader("📍 Stage 3 : Career")

            st.checkbox("Medical License")
            st.checkbox("Hospital Experience")
            st.checkbox("Specialization")

            st.metric("Estimated Learning Journey", "8 - 12 Years")

        elif career == "Teacher":

            st.success("Career Goal : Teacher")

            st.subheader("📍 Stage 1 : High School")

            st.checkbox("Improve Communication")
            st.checkbox("Master Favourite Subject")

            st.divider()

            st.subheader("📍 Stage 2 : Higher Education")

            st.checkbox("Bachelor's Degree")
            st.checkbox("B.Ed")
            st.checkbox("Teaching Practice")

            st.divider()

            st.subheader("📍 Stage 3 : Career")

            st.checkbox("Teacher Eligibility Test")
            st.checkbox("School Placement")

            st.metric("Estimated Learning Journey", "5 Years")

        elif career == "Civil Engineer":

            st.success("Career Goal : Civil Engineer")

            st.checkbox("Strong Mathematics")
            st.checkbox("Physics")
            st.checkbox("Engineering Drawing")
            st.checkbox("B.Tech Civil")
            st.checkbox("Site Internship")

            st.metric("Estimated Learning Journey", "4 - 5 Years")

        elif career == "Architect":

            st.success("Career Goal : Architect")

            st.checkbox("Drawing Skills")
            st.checkbox("Mathematics")
            st.checkbox("NATA Preparation")
            st.checkbox("B.Arch")
            st.checkbox("Portfolio")

            st.metric("Estimated Learning Journey", "5 Years")

        elif career == "Graphic Designer":

            st.success("Career Goal : Graphic Designer")

            st.checkbox("Drawing")
            st.checkbox("Photoshop")
            st.checkbox("Illustrator")
            st.checkbox("Figma")
            st.checkbox("Portfolio")

            st.metric("Estimated Learning Journey", "3 - 4 Years")

        elif career == "Business Analyst":

            st.success("Career Goal : Business Analyst")

            st.checkbox("Excel")
            st.checkbox("SQL")
            st.checkbox("Power BI")
            st.checkbox("Business Analytics")
            st.checkbox("Internship")

            st.metric("Estimated Learning Journey", "4 - 5 Years")

        st.divider()

        c1, c2 = st.columns(2)

        with c1:

            if st.button("Download Roadmap", use_container_width=True):

                st.success("PDF download feature will be added soon.")

        with c2:

            if st.button("Back to Dashboard", use_container_width=True):

                st.session_state.module = "home"

                st.rerun()


# ---------------- DAILY LEARNING ---------------- #

    elif st.session_state.module == "daily":

        st.header("📚 Daily Learning")

        st.write("Complete your daily learning tasks and manage your personal tasks.")

        st.divider()

        # ---------------- FIXED TASKS ---------------- #

        fixed_tasks = [
            "Learn Python Basics",
            "Complete Career Quiz",
            "Solve 5 Aptitude Questions",
            "Practice Communication Skills",
            "Read Technology News",
            "Complete One Coding Exercise",
            "Revise Yesterday's Notes"
        ]

        completed = 0

        st.subheader("Today's Learning Tasks")

        for i, task in enumerate(fixed_tasks):

            checked = st.checkbox(task, key=f"fixed_task_{i}")

            if checked:
                completed += 1

        total = len(fixed_tasks)

        percentage = int((completed / total) * 100)

        st.divider()

        st.subheader("Today's Progress")

        st.progress(completed / total)

        c1, c2 = st.columns(2)

        with c1:
            st.metric("Completed", f"{completed}/{total}")

        with c2:
            st.metric("Progress", f"{percentage}%")

        st.divider()

        # ---------------- WEEKLY PROGRESS ---------------- #

        st.subheader("Weekly Progress")

        week = [
            ("Monday", percentage),
            ("Tuesday", 65),
            ("Wednesday", 80),
            ("Thursday", 40),
            ("Friday", 20),
            ("Saturday", 0),
            ("Sunday", 0)
        ]

        for day, value in week:

            st.write(day)

            st.progress(value / 100)

            st.caption(f"{value}%")

        st.divider()

        # ---------------- PERSONAL TASKS ---------------- #

        st.subheader("My Personal Tasks")

        if "personal_tasks" not in st.session_state:

            st.session_state.personal_tasks = []

        task = st.text_input(
            "Task Name",
            placeholder="Example: Complete Mathematics Homework"
        )

        c1, c2 = st.columns(2)

        with c1:

            category = st.selectbox(
                "Category",
                [
                    "Study",
                    "Coding",
                    "Assignment",
                    "Project",
                    "Personal"
                ]
            )

        with c2:

            priority = st.selectbox(
                "Priority",
                [
                    "High",
                    "Medium",
                    "Low"
                ]
            )

        if st.button("Add Task", use_container_width=True):

            if task.strip():

                st.session_state.personal_tasks.append(
                    {
                        "task": task,
                        "category": category,
                        "priority": priority
                    }
                )

                st.success("Task Added Successfully")

                st.rerun()

        st.divider()

        st.subheader("Today's Personal Task List")

        if len(st.session_state.personal_tasks) == 0:

            st.info("No personal tasks added.")

        else:

            for i, t in enumerate(st.session_state.personal_tasks):

                st.checkbox(
                    f"{t['task']}  |  {t['category']}  |  {t['priority']}",
                    key=f"personal_{i}"
                )

        st.divider()

        st.subheader("Learning Tips")

        st.success("✔ Learn something new every day.")

        st.success("✔ Practice coding regularly.")

        st.success("✔ Revise previous topics.")

        st.success("✔ Stay consistent.")

        st.divider()

        c1, c2 = st.columns(2)

        with c1:

            if st.button("Clear Personal Tasks", use_container_width=True):

                st.session_state.personal_tasks = []

                st.success("All personal tasks cleared.")

                st.rerun()

        with c2:

            if st.button("Back to Dashboard", use_container_width=True):

                st.session_state.module = "home"

                st.rerun()

    # ---------------- CODING BASICS ---------------- #

    elif st.session_state.module == "coding":

        st.header("💻 Coding Basics")

        st.write("Start your programming journey with beginner-friendly topics.")

        st.divider()

        topics = [
            "Introduction to Programming",
            "Python Basics",
            "Variables & Data Types",
            "Operators",
            "Conditional Statements",
            "Loops",
            "Functions",
            "Lists",
            "Tuples",
            "Dictionaries",
            "Strings",
            "File Handling"
        ]

        completed = 0

        st.subheader("Learning Roadmap")

        for i, topic in enumerate(topics):

            if st.checkbox(topic, key=f"coding_topic_{i}"):

                completed += 1

        total = len(topics)

        progress = completed / total

        st.divider()

        st.subheader("Progress")

        st.progress(progress)

        c1, c2 = st.columns(2)

        with c1:
            st.metric("Completed", f"{completed}/{total}")

        with c2:
            st.metric("Completion", f"{int(progress*100)}%")

        st.divider()

        st.subheader("Today's Python Example")

        st.code(
    '''
    name = input("Enter your name: ")

    print("Welcome", name)
    ''',
    language="python"
        )

        st.divider()

        st.subheader("Quick Quiz")

        q1 = st.radio(
            "Which keyword is used to define a function in Python?",
            [
                "define",
                "function",
                "def",
                "func"
            ],
            key="coding_quiz1"
        )

        q2 = st.radio(
            "Which symbol is used for comments?",
            [
                "//",
                "#",
                "/* */",
                "--"
            ],
            key="coding_quiz2"
        )

        if st.button("Check Answers", use_container_width=True):

            score = 0

            if q1 == "def":
                score += 1

            if q2 == "#":
                score += 1

            st.success(f"Score : {score}/2")

            if score == 2:
                st.balloons()
                st.success("Excellent! Keep learning.")

            elif score == 1:
                st.info("Good! Review one concept.")

            else:
                st.warning("Practice Python Basics again.")

        st.divider()

        st.subheader("Recommended Resources")


        st.write("📗 https://www.w3schools.com/")

        st.write("📙 GeeksforGeeks Python")

        st.write("📕 HackerRank Python Practice")

        st.divider()

        c1, c2 = st.columns(2)

        with c1:

            if st.button("Restart Progress", use_container_width=True):

                for i in range(total):

                    if f"coding_topic_{i}" in st.session_state:

                        del st.session_state[f"coding_topic_{i}"]

                st.rerun()

        with c2:

            if st.button("Back to Dashboard", use_container_width=True):

                st.session_state.module = "home"

                st.rerun()

# ---------------- APTITUDE PRACTICE ---------------- #

    elif st.session_state.module == "aptitude":

        st.header("🧠 Aptitude Practice")

        st.write("Strengthen your logical thinking, numerical ability and analytical skills.")

        st.divider()

        categories = [
            "Quantitative Aptitude",
            "Logical Reasoning",
            "Verbal Ability"
        ]

        category = st.selectbox("Select Category", categories)

        st.divider()

        score = 0

        if category == "Quantitative Aptitude":

            st.subheader("Quantitative Aptitude")

            q1 = st.radio(
                "1. 25 × 8 = ?",
                ["180", "200", "220", "250"],
                key="qa1"
            )

            q2 = st.radio(
                "2. √144 = ?",
                ["10", "11", "12", "13"],
                key="qa2"
            )

            q3 = st.radio(
                "3. 15% of 200 = ?",
                ["20", "25", "30", "35"],
                key="qa3"
            )

            if q1 == "200":
                score += 1

            if q2 == "12":
                score += 1

            if q3 == "30":
                score += 1

        elif category == "Logical Reasoning":

            st.subheader("Logical Reasoning")

            q1 = st.radio(
                "1. Find the next number: 2, 4, 8, 16, ?",
                ["18", "24", "32", "64"],
                key="lr1"
            )

            q2 = st.radio(
                "2. Odd one out",
                ["Apple", "Banana", "Car", "Orange"],
                key="lr2"
            )

            q3 = st.radio(
                "3. CAT : KITTEN :: DOG : ?",
                ["Cub", "Puppy", "Calf", "Kid"],
                key="lr3"
            )

            if q1 == "32":
                score += 1

            if q2 == "Car":
                score += 1

            if q3 == "Puppy":
                score += 1

        else:

            st.subheader("Verbal Ability")

            q1 = st.radio(
                "1. Synonym of Happy",
                ["Sad", "Joyful", "Angry", "Lazy"],
                key="va1"
            )

            q2 = st.radio(
                "2. Antonym of Strong",
                ["Powerful", "Weak", "Tall", "Large"],
                key="va2"
            )

            q3 = st.radio(
                "3. Choose the correct sentence.",
                [
                    "She go to school.",
                    "She goes to school.",
                    "She going school.",
                    "She gone school."
                ],
                key="va3"
            )

            if q1 == "Joyful":
                score += 1

            if q2 == "Weak":
                score += 1

            if q3 == "She goes to school.":
                score += 1

        st.divider()

        if st.button("Submit Test", use_container_width=True):

            st.subheader("Result")

            st.metric("Score", f"{score}/3")

            st.progress(score / 3)

            if score == 3:

                st.success("Excellent Performance!")

                st.balloons()

            elif score == 2:

                st.info("Good Job! Keep Practicing.")

            else:

                st.warning("Practice More to Improve.")

        st.divider()

        st.subheader("Practice Tips")

        st.success("✔ Practice at least 10 questions daily.")

        st.success("✔ Learn shortcuts for calculations.")

        st.success("✔ Improve reading speed.")

        st.success("✔ Solve previous placement papers.")

        st.divider()

        c1, c2 = st.columns(2)

        with c1:

            if st.button("Practice Again", use_container_width=True):

                st.rerun()

        with c2:

            if st.button("Back to Dashboard", use_container_width=True):

                st.session_state.module = "home"

                st.rerun()

# ---------------- COMMUNICATION SKILLS ---------------- #

    elif st.session_state.module == "communication":

        st.header(" Communication Skills")

        st.write("Improve your speaking, writing and presentation skills.")

        st.divider()

        tab1, tab2 = st.tabs([
            "Speaking",
            "Writing"
        ])

        # ---------------- SPEAKING ---------------- #

        with tab1:

            st.subheader("Daily Speaking Practice")

            speaking_tasks = [

                "Introduce Yourself for 1 Minute",

                "Describe Your Favourite Subject",

                "Explain Your Dream Career",

                "Speak About Today's News",

                "Talk About Your Hobby"

            ]

            completed = 0

            for i, task in enumerate(speaking_tasks):

                if st.checkbox(task, key=f"speaking_{i}"):

                    completed += 1

            st.divider()

            st.progress(completed/len(speaking_tasks))

            st.metric(
                "Completed",
                f"{completed}/{len(speaking_tasks)}"
            )

        # ---------------- WRITING ---------------- #

        with tab2:

            st.subheader("Writing Practice")

            topic = st.selectbox(
                "Choose a Topic",
                [
                    "My Dream Career",
                    "Artificial Intelligence",
                    "Importance of Education",
                    "Technology in Daily Life",
                    "My Future Goals"
                ]
            )

            response = st.text_area(
                "Write 100-150 words",
                height=250
            )

            words = len(response.split())

            st.write(f"Word Count : {words}")

            if st.button("Submit Writing"):

                if words >= 100:

                    st.success("Excellent! Keep practicing.")

                elif words >= 50:

                    st.info("Good. Try writing a little more.")

                else:

                    st.warning("Write at least 100 words.")


        st.divider()

        st.subheader("Communication Tips")

        st.success("✔ Read English newspapers daily.")

        st.success("✔ Practice speaking in front of a mirror.")

        st.success("✔ Learn one new English word every day.")

        st.success("✔ Watch TED Talks and educational videos.")

        st.success("✔ Participate in group discussions.")

        st.divider()

        c1, c2 = st.columns(2)

        with c1:

            if st.button("Reset Practice", use_container_width=True):

                st.rerun()

        with c2:

            if st.button("Back to Dashboard", use_container_width=True):

                st.session_state.module = "home"

                st.rerun()

# ---------------- GOAL TRACKER ---------------- #

    elif st.session_state.module == "goal":

        st.header("🎯 Goal Tracker")

        st.write("Set your academic and career goals and track your progress.")

        st.divider()

        if "goals" not in st.session_state:
            st.session_state.goals = []

        st.subheader("Create New Goal")

        goal = st.text_input(
            "Goal",
            placeholder="Example: Learn Python Basics"
        )

        c1, c2 = st.columns(2)

        with c1:

            category = st.selectbox(
                "Category",
                [
                    "Career",
                    "Coding",
                    "Academics",
                    "Communication",
                    "Personal"
                ]
            )

        with c2:

            priority = st.selectbox(
                "Priority",
                [
                    "High",
                    "Medium",
                    "Low"
                ]
            )

        if st.button("Add Goal", use_container_width=True):

            if goal.strip():

                st.session_state.goals.append({

                    "goal": goal,

                    "category": category,

                    "priority": priority

                })

                st.success("Goal Added Successfully!")

                st.rerun()

        st.divider()

        st.subheader("My Goals")

        if len(st.session_state.goals) == 0:

            st.info("No goals added yet.")

        else:

            completed = 0

            total = len(st.session_state.goals)

            for i, g in enumerate(st.session_state.goals):

                if st.checkbox(

                    f"{g['goal']} | {g['category']} | {g['priority']}",

                    key=f"goal_{i}"

                ):

                    completed += 1

            st.divider()

            progress = completed / total

            st.subheader("Overall Goal Progress")

            st.progress(progress)

            c1, c2 = st.columns(2)

            with c1:
                st.metric("Completed Goals", completed)

            with c2:
                st.metric("Completion", f"{int(progress*100)}%")

        st.divider()

        st.subheader("Suggested Goals")

        st.success("✔ Complete AI Career Quiz")

        st.success("✔ Learn Python Basics")

        st.success("✔ Practice Aptitude Daily")

        st.success("✔ Improve Communication Skills")

        st.success("✔ Build One Mini Project")

        st.divider()

        c1, c2 = st.columns(2)

        with c1:

            if st.button("Clear All Goals", use_container_width=True):

                st.session_state.goals = []

                st.success("Goals Cleared Successfully.")

                st.rerun()

        with c2:

            if st.button("Back to Dashboard", use_container_width=True):

                st.session_state.module = "home"

                st.rerun()

# ---------------- MENTOR ---------------- #

    elif st.session_state.module == "mentor":

        from utils.gemini import ask_gemini

        st.header(" Mentor")

        st.write(f"### Hello, {st.session_state.user_name} ")

        st.caption(
            "Ask me anything about careers, coding, studies, future skills or education."
        )

        st.divider()

        # ---------------- CHAT HISTORY ---------------- #

        if "mentor_history" not in st.session_state:
            st.session_state.mentor_history = []

        # Display previous conversation
        for role, message in st.session_state.mentor_history:

            with st.chat_message(role):
                st.markdown(message)

        # ---------------- CHAT INPUT ---------------- #

        prompt = st.chat_input("Type your question...")

        if prompt:

            # Show user message immediately
            st.session_state.mentor_history.append(("user", prompt))

            with st.chat_message("user"):
                st.markdown(prompt)

            # Previous history only
            history = st.session_state.mentor_history[:-1]

            # Gemini response
            with st.chat_message("assistant"):

                with st.spinner("Thinking..."):

                    reply = ask_gemini(
                        history,
                        prompt
                    )

                    st.markdown(reply)

            st.session_state.mentor_history.append(
                ("assistant", reply)
            )

            st.rerun()

        st.divider()

        if st.button("⬅ Back to Dashboard", use_container_width=True):

            st.session_state.module = "home"

            st.rerun()