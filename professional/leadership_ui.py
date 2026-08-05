import streamlit as st
from professional.database import get_leadership_scores, save_leadership_scores

def render_leadership_section(user_id):
    st.subheader("8. Leadership Skill Evaluation")
    st.caption("Assess core leadership metrics critical for senior engineers, tech leads, and managers.")

    scores = get_leadership_scores(user_id)

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("### Leadership Assessment Matrix")
        for area, val in scores.items():
            st.write(f"**{area}**: `{val}%`")
            st.progress(val / 100.0)

    with col2:
        st.markdown("### Self / Manager Evaluation Rater")
        with st.form("leadership_form"):
            t_coord = st.slider("Team Coordination", 0, 100, int(scores.get("Team Coordination", 0)))
            ment = st.slider("Mentoring", 0, 100, int(scores.get("Mentoring", 0)))
            dec_make = st.slider("Decision Making", 0, 100, int(scores.get("Decision Making", 0)))
            conf_res = st.slider("Conflict Resolution", 0, 100, int(scores.get("Conflict Resolution", 0)))
            proj_own = st.slider("Project Ownership", 0, 100, int(scores.get("Project Ownership", 0)))

            saved = st.form_submit_button("Save Leadership Scores", use_container_width=True)
            if saved:
                updated_scores = {
                    "Team Coordination": t_coord,
                    "Mentoring": ment,
                    "Decision Making": dec_make,
                    "Conflict Resolution": conf_res,
                    "Project Ownership": proj_own
                }
                save_leadership_scores(user_id, updated_scores)
                st.success("Leadership evaluation updated successfully!")
                st.rerun()

    st.divider()
    overall_lead = sum(scores.values()) / max(len(scores), 1)
    has_scores = any(v > 0 for v in scores.values())

    if has_scores:
        top_asset_key = max(scores, key=scores.get)
        growth_opp_key = min(scores, key=scores.get)
        top_asset_str = f"{top_asset_key} ({scores[top_asset_key]}%)"
        growth_opp_str = f"{growth_opp_key} ({scores[growth_opp_key]}%)"
    else:
        top_asset_str = "Not Evaluated"
        growth_opp_str = "Not Evaluated"

    c1, c2, c3 = st.columns(3)
    c1.metric("Leadership Index", f"{overall_lead:.1f}%")
    c2.metric("Top Leadership Asset", top_asset_str)
    c3.metric("Growth Opportunity", growth_opp_str)


