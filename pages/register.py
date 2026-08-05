import streamlit as st
from utils.database import register_new_user

st.set_page_config(
    page_title="Register - TalentSphere Elevate",
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

st.title("Create Your Account")
st.caption("Join TalentSphere Elevate and begin your career journey.")

st.divider()

name = st.text_input(
    "Full Name",
    placeholder="Enter your full name"
)

email = st.text_input(
    "Email",
    placeholder="Enter your email"
)

password = st.text_input(
    "Password",
    type="password",
    placeholder="Create a password"
)

category = st.selectbox(
    "Category",
    [
        "High School Student",
        "College Student",
        "Working Professional"
    ]
)

if st.button("Create Account", use_container_width=True):
    success, msg = register_new_user(name, email, password, category)
    if success:
        st.success(msg)
        st.info("You can now log in with your email and password.")
        st.session_state["demo_email"] = email.strip().lower()
        st.session_state["demo_pass"] = password.strip()
    else:
        st.error(msg)


st.write("")

col1, col2 = st.columns(2)

with col1:
    if st.button("← Home", use_container_width=True):
        st.switch_page("app.py")

with col2:
    if st.button("Login", use_container_width=True):
        st.switch_page("pages/Login.py")