import streamlit as st
from professional.database import get_certification_status, update_cert_status

def render_trends_and_certs_section(user_id):
    st.subheader("6. Industry Trend Recommendations & 7. Certification Suggestions")
    st.caption("Stay aligned with high-growth technical skills and industry-standard credentials.")

    st.markdown("### Top Industry Trending Skills")
    trending_skills = ["Cloud Computing", "Docker", "Kubernetes", "Microservices", "AI Integration", "System Design"]

    cols = st.columns(6)
    for idx, sk in enumerate(trending_skills):
        cols[idx % 6].button(sk, key=f"trend_sk_{idx}", use_container_width=True)

    st.markdown("#### Industry Demand Forecast")
    forecast_data = [
        {"skill": "Kubernetes", "growth": "+38%", "score": 88},
        {"skill": "AWS", "growth": "+32%", "score": 82},
        {"skill": "Microservices", "growth": "+28%", "score": 78},
        {"skill": "System Design", "growth": "+25%", "score": 75}
    ]

    f_col1, f_col2 = st.columns(2)
    with f_col1:
        for f in forecast_data[:2]:
            with st.container(border=True):
                st.write(f"**{f['skill']}**: `{f['growth']} Demand Growth`")
                st.progress(f["score"] / 100.0)

    with f_col2:
        for f in forecast_data[2:]:
            with st.container(border=True):
                st.write(f"**{f['skill']}**: `{f['growth']} Demand Growth`")
                st.progress(f["score"] / 100.0)

    st.divider()

    st.markdown("### 7. Recommended Certifications & Tracker")
    st.caption("Update your progress on high-priority certifications recommended for experienced developers.")

    certs = get_certification_status(user_id)

    status_options = ["Wishlist", "In Progress", "Completed"]

    for idx, c in enumerate(certs):
        with st.container(border=True):
            col1, col2, col3 = st.columns([3, 2, 2], vertical_alignment="center")
            with col1:
                st.markdown(f"**{c['cert_name']}**")
                p_color = "red" if c['priority'] == "High" else "orange"
                st.markdown(f"Priority: <span style='color:{p_color};font-weight:bold;'>{c['priority']}</span>", unsafe_allow_html=True)
            with col2:
                curr_status_idx = status_options.index(c['status']) if c['status'] in status_options else 0
                new_status = st.selectbox("Status", status_options, index=curr_status_idx, key=f"cert_select_{idx}")
            with col3:
                if new_status != c['status']:
                    update_cert_status(user_id, c['cert_name'], new_status, c['priority'])
                    st.success(f"Updated {c['cert_name']} to {new_status}")
                    st.rerun()
