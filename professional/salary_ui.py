# -*- coding: utf-8 -*-
import streamlit as st
from professional.database import get_professional_profile

def render_salary_section(user_id):
    st.subheader("5. Salary Benchmark Insights")
    st.caption("Compare your current compensation against industry standards and projected salary growth.")

    profile = get_professional_profile(user_id)
    current_sal = float(profile.get("current_salary", 0.0))
    market_avg = 7.5
    target_low = 9.0
    target_high = 12.0

    delta_market = current_sal - market_avg
    potential_pct = max(0, int(((target_low - current_sal) / max(current_sal, 0.1)) * 100)) if current_sal > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Current Salary", f"₹{current_sal:.1f} LPA")
    col2.metric("Market Average", f"₹{market_avg:.1f} LPA", delta=f"{'-' if delta_market < 0 else '+'}{abs(delta_market):.1f} LPA vs Market" if current_sal > 0 else "Baseline: ₹0.0 LPA")
    col3.metric("Senior Backend Range", f"₹{target_low} - ₹{target_high} LPA")
    col4.metric("Potential Growth", f"+{potential_pct}%", delta="Target Role Upside")


    st.divider()

    st.markdown("### Interactive Salary Progression Estimator")

    user_target_role = st.selectbox("Select Target Role for Salary Comparison", [
        "Senior Backend Engineer (₹9 - 12 LPA)",
        "Backend Architect (₹14 - 18 LPA)",
        "Cloud Engineer (₹10 - 14 LPA)",
        "Engineering Lead (₹16 - 22 LPA)"
    ])

    if "Senior Backend Engineer" in user_target_role:
        proj_low, proj_high = 9.0, 12.0
    elif "Backend Architect" in user_target_role:
        proj_low, proj_high = 14.0, 18.0
    elif "Cloud Engineer" in user_target_role:
        proj_low, proj_high = 10.0, 14.0
    else:
        proj_low, proj_high = 16.0, 22.0

    st.markdown("#### Salary Comparison Bar Visual")
    sal_data = {
        "Your Current Salary": current_sal,
        "Market Average (Software Dev)": market_avg,
        "Target Role Lower Bound": proj_low,
        "Target Role Upper Bound": proj_high
    }

    max_sal = max(25.0, proj_high + 2.0)
    for label, val in sal_data.items():
        st.write(f"**{label}**: ₹{val} LPA")
        st.progress(min(1.0, val / max_sal))

    st.divider()
    diff_low = max(0.0, proj_low - current_sal)
    diff_high = max(0.0, proj_high - current_sal)
    st.info(f"Upgrading your skills unlocks an estimated salary jump of **₹{diff_low:.1f} LPA to ₹{diff_high:.1f} LPA** above your current baseline.")

