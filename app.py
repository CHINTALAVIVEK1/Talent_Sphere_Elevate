import streamlit as st

st.set_page_config(
    page_title="TalentSphere Elevate",
    page_icon="assets/logo.png",
    layout="wide"
)




# ---------------- PAGE STYLE ---------------- #

st.markdown("""
<style>

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

.demo-card{
    padding:18px;
    border-radius:12px;
    border:1px solid #ddd;
    background:#fafafa;
    text-align:center;
}

[data-testid="stSidebarNav"] {
    display: none;
}

</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ---------------- #

col1, col2 = st.columns([1,8], vertical_alignment="center")

with col1:
    st.image("assets/logo.png", width=80)

with col2:
    st.title("TalentSphere Elevate")
    st.caption("AI-Powered Career Development Platform")

st.divider()

# ---------------- HERO ---------------- #

st.image("assets/logo2.png", use_container_width=True)
st.markdown(
"""
### Empower Your Career Journey

TalentSphere Elevate helps students and professionals discover careers,
develop future-ready skills, and achieve their goals through personalized
learning and AI-powered career guidance.
"""
)
st.markdown(
"""
<h2 style="text-align:center;">
Discover Your Future with Confidence
</h2>

<p style="text-align:center;font-size:18px;">
Helping students and professionals explore careers,
develop skills and achieve success.
</p>
""",
unsafe_allow_html=True
)

st.write("")

# ---------------- LOGIN / REGISTER ---------------- #

c1,c2,c3 = st.columns([2,2,2])

with c2:

    if st.button("Login", use_container_width=True):
        st.switch_page("pages/Login.py")

    if st.button("Register", use_container_width=True):
        st.switch_page("pages/Register.py")

st.divider()

st.subheader("Platform Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.success("Career Explorer")
    st.success("AI Career Quiz")
    st.success("Interest Assessment")

with col2:
    st.success("Future Skills Roadmap")
    st.success("Daily Learning")
    st.success("Coding Basics")

with col3:
    st.success("Aptitude Practice")
    st.success("Goal Tracker")
    st.success("AI Mentor")

st.divider()

st.subheader("About TalentSphere Elevate")

st.write("""
TalentSphere Elevate is an AI-powered career development platform designed
to help students discover career opportunities, assess their interests,
develop future-ready skills, and achieve their academic and professional goals.
""")

st.divider()

st.caption("© 2026 TalentSphere Elevate. All Rights Reserved.")