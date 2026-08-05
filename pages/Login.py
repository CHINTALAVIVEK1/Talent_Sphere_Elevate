import streamlit as st
from utils.database import authenticate_user

st.set_page_config(
    page_title="Login - TalentSphere Elevate",
    page_icon="assets/logo.png",
    layout="centered"
)

st.markdown("""
<style>
[data-testid="stSidebarNav"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

st.image("assets/logo.png", width=90)

st.title("Welcome Back")
st.caption("Sign in to continue to TalentSphere Elevate")

st.divider()

# Demo credentials quick selection expander
with st.expander("🔑 Quick Demo Credentials (For Testing)"):
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        if st.button("Use Working Professional Demo"):
            st.session_state["demo_email"] = "professional@demo.com"
            st.session_state["demo_pass"] = "demo123"
        if st.button("Use College Student Demo"):
            st.session_state["demo_email"] = "college@demo.com"
            st.session_state["demo_pass"] = "demo123"
    with c_col2:
        if st.button("Use High School Student Demo"):
            st.session_state["demo_email"] = "school@demo.com"
            st.session_state["demo_pass"] = "demo123"
        if st.button("Use Admin Demo"):
            st.session_state["demo_email"] = "admin@demo.com"
            st.session_state["demo_pass"] = "admin123"

default_email = st.session_state.get("demo_email", "")
default_pass = st.session_state.get("demo_pass", "")

email = st.text_input(
    "Email",
    value=default_email,
    placeholder="Enter your email"
)

password = st.text_input(
    "Password",
    value=default_pass,
    type="password",
    placeholder="Enter your password"
)

if st.button("Login", use_container_width=True):
    if not email or not password:
        st.warning("Please enter both email and password.")
    else:
        user = authenticate_user(email, password)

        if user:
            st.session_state.logged_in = True
            st.session_state.user_id = user["id"]
            st.session_state.user_name = user["name"]
            st.session_state.category = user["category"]
            
            st.success(f"Login successful! Redirecting to {user['category']} dashboard...")
            
            category = user["category"]
            if category == "High School Student":
                st.switch_page("pages/HighSchoolDashboard.py")
            elif category == "College Student":
                st.switch_page("pages/CollegeDashboard.py")
            elif category == "Working Professional":
                st.switch_page("pages/ProfessionalDashboard.py")
            elif category == "Admin":
                st.switch_page("pages/AdminDashboard.py")
            else:
                st.error(f"Unknown user category: {category}")
        else:
            st.error("Invalid email or password. Please verify your credentials or register a new account.")

st.write("")

col1, col2 = st.columns(2)

with col1:
    if st.button("← Home", use_container_width=True):
        st.switch_page("app.py")

with col2:
    if st.button("Register Account", use_container_width=True):
        st.switch_page("pages/register.py")