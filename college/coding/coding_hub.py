import streamlit as st
import datetime
import pandas as pd
from college.coding.utils import CODING_CUSTOM_CSS, format_minutes_to_hours
from college.coding.database import (
    get_coding_progress,
    save_coding_progress,
    get_leetcode_progress,
    save_leetcode_progress,
    save_bookmark,
    get_interview_progress,
    save_interview_progress
)
from college.coding.leetcode import CHALLENGES
from college.coding.roadmap import get_roadmap_status, mark_subtopic_completed, get_resume_skill_gaps
from college.coding.ai_assistant import get_assistant_response, QUICK_START_PROMPTS
from college.coding.interview_bank import get_augmented_interview_questions, INTERVIEW_QUESTIONS
from college.coding.analytics import (
    generate_difficulty_distribution_chart,
    generate_weekly_activity_chart,
    generate_topic_mastery_chart,
    generate_readiness_gauge
)

def coding_hub():
    """
    Main entry coordinator for the refined College Coding Hub module.
    """
    st.markdown(CODING_CUSTOM_CSS, unsafe_allow_html=True)
    
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("Please log in to continue.")
        return
        
    stats = get_coding_progress(user_id)
    
    # 1. State Calculations
    gaps = get_resume_skill_gaps(user_id)
    resume_score = st.session_state.get("ats_analysis", {}).get("overall_score")
    if resume_score is None:
        resume_score = gaps["completeness_score"]
        
    local_leetcode = get_leetcode_progress(user_id)
    solved_count = sum(1 for p in local_leetcode.values() if p["status"] == "Solved")
    easy_solved = sum(1 for p_id, p in local_leetcode.items() if p["status"] == "Solved" and any(x["id"] == p_id and x["difficulty"] == "Easy" for x in CHALLENGES))
    medium_solved = sum(1 for p_id, p in local_leetcode.items() if p["status"] == "Solved" and any(x["id"] == p_id and x["difficulty"] == "Medium" for x in CHALLENGES))
    hard_solved = sum(1 for p_id, p in local_leetcode.items() if p["status"] == "Solved" and any(x["id"] == p_id and x["difficulty"] == "Hard" for x in CHALLENGES))
    
    roadmap_status = get_roadmap_status(user_id)
    roadmap_comp_pct = roadmap_status["completion_percentage"]
    
    int_qs = get_augmented_interview_questions(user_id)
    completed_int = sum(1 for q in int_qs if q["completed"])
    total_int = len(INTERVIEW_QUESTIONS)
    int_comp_pct = int((completed_int / total_int) * 100) if total_int > 0 else 0
    
    # Progress math
    total_challenges = len(CHALLENGES)
    sandbox_comp_pct = int((solved_count / total_challenges) * 100) if total_challenges > 0 else 0
    
    coding_readiness_val = min(100, int((sandbox_comp_pct * 0.7) + (roadmap_comp_pct * 0.3)))
    interview_readiness_val = min(100, int((int_comp_pct * 0.6) + (coding_readiness_val * 0.4)))
    placement_readiness_val = min(100, int((resume_score * 0.4) + (coding_readiness_val * 0.4) + (interview_readiness_val * 0.2)))
    
    # Save statistics
    stats["overall_readiness"] = placement_readiness_val
    save_coding_progress(user_id, stats)
    
    # Define 5 tabs without emojis
    tab_dash, tab_roadmap, tab_practice, tab_ai, tab_interview = st.tabs([
        "Dashboard",
        "Roadmap",
        "Practice",
        "AI Coding Mentor",
        "Interview Prep"
    ])
    
    # ==========================================
    # TAB 1: DASHBOARD
    # ==========================================
    with tab_dash:
        st.markdown("### Coding Dashboard")
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-card-title">Placement Readiness</div>
                <div class="metric-card-value">{placement_readiness_val}%</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-card-title">Resume Score</div>
                <div class="metric-card-value">{resume_score}%</div>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-card-title">Coding Score</div>
                <div class="metric-card-value">{coding_readiness_val}%</div>
            </div>
            """, unsafe_allow_html=True)
        with c4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-card-title">Interview Score</div>
                <div class="metric-card-value">{interview_readiness_val}%</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.write("")
        st.divider()
        
        # Display charts
        col_g1, col_g2 = st.columns([1, 1], gap="medium")
        with col_g1:
            st.markdown("##### Solve Breakdown")
            st.metric("Total Solved", solved_count)
            
            c_sub1, c_sub2, c_sub3 = st.columns(3)
            c_sub1.metric("Easy", easy_solved)
            c_sub2.metric("Medium", medium_solved)
            c_sub3.metric("Hard", hard_solved)
            
            st.write("")
            st.metric("Active Streak", f"{stats.get('streak', 0)} Days")
            st.metric("Longest Streak", f"{stats.get('longest_streak', 0)} Days")
            
        with col_g2:
            st.markdown("##### Difficulty Distribution")
            fig_pie = generate_difficulty_distribution_chart(easy_solved, medium_solved, hard_solved)
            st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
            
        st.divider()
        
        # Recently Solved
        st.markdown("##### Recently Solved Problems")
        solved_probs = []
        for prob in CHALLENGES:
            ch_id = prob["id"]
            prog = local_leetcode.get(ch_id, {"status": "Pending", "last_solved": ""})
            if prog["status"] == "Solved":
                p_copy = dict(prob)
                p_copy["last_solved"] = prog["last_solved"]
                solved_probs.append(p_copy)
                
        solved_probs.sort(key=lambda x: x.get("last_solved", ""), reverse=True)
        
        if solved_probs:
            for prob in solved_probs[:4]:
                diff_class = f"badge-{prob['difficulty'].lower()}"
                st.markdown(f"""
                <div style="background-color: #1e293b; padding: 12px 18px; border-radius: 6px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #334155;">
                    <div>
                        <span class="{diff_class}">{prob['difficulty']}</span>
                        <b style="margin-left: 10px; color: #f8fafc;">#{prob['id']} - {prob['title']}</b>
                        <span style="color: #64748b; font-size: 13px; margin-left: 12px;">({prob['topic']})</span>
                    </div>
                    <span style="color: #22c55e; font-size: 13px; font-weight: 600;">Solved on {prob['last_solved'] or 'Recent Date'}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No problems marked solved yet. Check completed tasks inside the Practice tab.")

    # ==========================================
    # TAB 2: ROADMAP & GAPS
    # ==========================================
    with tab_roadmap:
        st.markdown("### Learning Roadmap")
        
        st.markdown("##### Skill Gap Analysis")
        if gaps["missing_skills"]:
            st.warning("The following core placement skills are missing from your resume:")
            missing_str = "".join([f'<span style="background-color: rgba(239, 68, 68, 0.1); color: #f87171; padding: 4px 10px; border-radius: 4px; margin: 4px; display: inline-block; font-size: 13px; border: 1px solid rgba(239, 68, 68, 0.2);">{s}</span>' for s in gaps["missing_skills"]])
            st.markdown(missing_str, unsafe_allow_html=True)
            st.write("")
            st.info("Study these topics in the Roadmap below to improve your score.")
        else:
            st.success("All core placement skills are present on your resume.")
            
        st.write("")
        
        col_rm1, col_rm2 = st.columns([2, 1])
        with col_rm1:
            st.markdown(f"**Roadmap Progress:** {roadmap_comp_pct}%")
            st.progress(roadmap_comp_pct / 100.0)
        with col_rm2:
            rem_hours = roadmap_status["remaining_minutes"] // 60
            st.metric("Study Time Remaining", f"{rem_hours} Hours")
            
        st.divider()
        
        if roadmap_status["recommended_topics"]:
            rec = roadmap_status["recommended_topics"][0]
            st.info(f"Recommended next topic: {rec['subtopic']} under {rec['category']} ({rec['hours']}h study time)")
            
        st.write("")
        
        # Stepper with Undo
        for category, subtopics in roadmap_status["status_map"].items():
            st.markdown(f"#### {category} Path")
            st.markdown('<div style="border-left: 2px solid #334155; margin-left: 15px; padding-left: 20px; position: relative;">', unsafe_allow_html=True)
            
            for idx, sub_data in enumerate(subtopics):
                sub_name = sub_data["subtopic"]
                status = sub_data["status"]
                hours = sub_data["hours"]
                
                if status == "Completed":
                    card_class = "stepper-item-completed"
                    status_text = "Completed"
                elif status == "Unlocked":
                    card_class = "stepper-item-unlocked"
                    status_text = "Unlocked & Ready"
                else:
                    card_class = "stepper-item-locked"
                    status_text = "Locked"
                    
                st.markdown(f"""
                <div class="{card_class}">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-weight: 700; color: #f8fafc; font-size: 15px;">{sub_name}</span>
                            <span style="color: #94a3b8; font-size: 12px; margin-left: 10px;">({hours}h estimation)</span>
                        </div>
                        <span style="font-size: 12px; font-weight: 600; text-transform: uppercase;">{status_text}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if status == "Unlocked":
                    col_st1, col_st2 = st.columns([5, 1])
                    with col_st2:
                        if st.button("Complete", key=f"mark_comp_{category}_{sub_name}", use_container_width=True):
                            mark_subtopic_completed(user_id, category, sub_name, True)
                            stats["time_spent"] = stats.get("time_spent", 0) + (hours * 60)
                            stats["streak"] = max(1, stats.get("streak", 0))
                            save_coding_progress(user_id, stats)
                            st.rerun()
                            
                elif status == "Completed":
                    col_st1, col_st2 = st.columns([5, 1])
                    with col_st2:
                        if st.button("Undo", key=f"undo_comp_{category}_{sub_name}", use_container_width=True):
                            mark_subtopic_completed(user_id, category, sub_name, False)
                            # Subtract time spent
                            stats["time_spent"] = max(0, stats.get("time_spent", 0) - (hours * 60))
                            save_coding_progress(user_id, stats)
                            st.success(f"Reset progress for {sub_name}")
                            st.rerun()
                            
            st.markdown('</div>', unsafe_allow_html=True)
            st.write("")

    # ==========================================
    # TAB 3: PRACTICE (LEETCODE LINKS & CHECKBOXES)
    # ==========================================
    with tab_practice:
        st.markdown("### LeetCode Practice")
        st.write("Browse coding challenges, solve them directly on LeetCode, and check them off here to track your progress.")
        
        diff_order = {"Easy": 1, "Medium": 2, "Hard": 3}
        sorted_challenges = sorted(CHALLENGES, key=lambda x: diff_order.get(x["difficulty"], 4))
        
        for p in sorted_challenges:
            ch_id = p["id"]
            diff_class = f"badge-{p['difficulty'].lower()}"
            is_solved = local_leetcode.get(ch_id, {}).get("status") == "Solved"
            is_fav = local_leetcode.get(ch_id, {}).get("is_favorite", False)
            
            with st.container(border=True):
                c_p1, c_p2 = st.columns([4, 1])
                with c_p1:
                    st.markdown(f"""
                    <span class="{diff_class}">{p['difficulty']}</span>
                    <b style="font-size: 16px; margin-left: 8px; color: #f8fafc;">#{ch_id} - {p['title']}</b>
                    <span style="color: #94a3b8; font-size: 13px; margin-left: 10px;">({p['topic']})</span>
                    """, unsafe_allow_html=True)
                    st.write(p["description"])
                    st.markdown(f"[Solve on LeetCode]({p['url']})", unsafe_allow_html=True)
                    
                with c_p2:
                    # Completion Checkbox
                    checked = st.checkbox("Completed", value=is_solved, key=f"chk_solved_{ch_id}")
                    if checked != is_solved:
                        save_leetcode_progress(
                            user_id=user_id,
                            problem_id=ch_id,
                            status="Solved" if checked else "Pending",
                            is_favorite=is_fav,
                            last_solved=datetime.date.today().isoformat() if checked else ""
                        )
                        # Sync daily analytics solved count
                        if checked:
                            stats["streak"] = max(1, stats.get("streak", 0))
                            save_coding_progress(user_id, stats)
                        st.rerun()
                        
                    # Favorite check
                    fav = st.checkbox("Favorite", value=is_fav, key=f"chk_fav_{ch_id}")
                    if fav != is_fav:
                        save_leetcode_progress(
                            user_id=user_id,
                            problem_id=ch_id,
                            status="Solved" if is_solved else "Pending",
                            is_favorite=fav,
                            last_solved=local_leetcode.get(ch_id, {}).get("last_solved", "")
                        )
                        st.rerun()

    # ==========================================
    # TAB 4: AI CODING MENTOR
    # ==========================================
    with tab_ai:
        st.markdown("### AI Coding Mentor")
        st.write("Get explanation, debugging help, or complexity analysis. Limited strictly to programming topics.")
        
        if "coding_chat_history" not in st.session_state:
            st.session_state.coding_chat_history = []
            
        if not st.session_state.coding_chat_history:
            st.markdown("##### Quick Start Templates")
            c_qp1, c_qp2 = st.columns(2)
            with c_qp1:
                for qp in QUICK_START_PROMPTS[:2]:
                    if st.button(qp, use_container_width=True):
                        st.session_state.coding_chat_history.append(("User", qp))
                        with st.spinner("AI thinking..."):
                            ai_reply = get_assistant_response([], qp)
                        st.session_state.coding_chat_history.append(("Assistant", ai_reply))
                        st.rerun()
            with c_qp2:
                for qp in QUICK_START_PROMPTS[2:]:
                    if st.button(qp, use_container_width=True):
                        st.session_state.coding_chat_history.append(("User", qp))
                        with st.spinner("AI thinking..."):
                            ai_reply = get_assistant_response([], qp)
                        st.session_state.coding_chat_history.append(("Assistant", ai_reply))
                        st.rerun()
            st.write("")
            st.divider()
            
        for idx, (role, text) in enumerate(st.session_state.coding_chat_history):
            bubble_class = "chat-bubble-user" if role == "User" else "chat-bubble-assistant"
            sender_label = "You" if role == "User" else "Coding Mentor"
            st.markdown(f"""
            <div class="{bubble_class}">
                <b>{sender_label}:</b><br/>{text}
            </div>
            """, unsafe_allow_html=True)
            
        with st.form("chat_form_refined_final", clear_on_submit=True):
            user_msg = st.text_input("Ask a coding question...", placeholder="e.g. Write a python function for Binary Search")
            cols_form = st.columns([5, 1])
            with cols_form[1]:
                submit_msg = st.form_submit_button("Send")
                
            if submit_msg and user_msg.strip():
                st.session_state.coding_chat_history.append(("User", user_msg.strip()))
                with st.spinner("AI thinking..."):
                    ai_reply = get_assistant_response(st.session_state.coding_chat_history[:-1], user_msg.strip())
                st.session_state.coding_chat_history.append(("Assistant", ai_reply))
                st.rerun()
                
        if st.button("Clear Chat History"):
            st.session_state.coding_chat_history = []
            st.rerun()

    # ==========================================
    # TAB 5: INTERVIEW PREPARATION
    # ==========================================
    with tab_interview:
        st.markdown("### Interview Preparation Bank")
        st.write("Browse categorized questions and expert answers for top technology roles.")
        
        q_bank = get_augmented_interview_questions(user_id)
        
        col_qi1, col_qi2, col_qi3 = st.columns([2, 1, 1])
        with col_qi1:
            q_search = st.text_input("Search Questions", value="", placeholder="Search by keyword")
        with col_qi2:
            cats = sorted(list(set(q["category"] for q in INTERVIEW_QUESTIONS)))
            q_cat_filter = st.selectbox("Category Filter", ["All"] + cats)
        with col_qi3:
            q_type_filter = st.selectbox("Type Filter", ["All", "Programming", "CS Core", "Behavioral", "Company"])
            
        filtered_qs = []
        for q in q_bank:
            if q_search.strip().lower() not in q["question"].lower() and q_search.strip().lower() not in q["answer"].lower():
                continue
            if q_cat_filter != "All" and q["category"] != q_cat_filter:
                continue
            if q_type_filter != "All" and q["sub_type"] != q_type_filter:
                continue
            filtered_qs.append(q)
            
        st.write(f"Showing {len(filtered_qs)} Questions:")
        
        diff_order = {"Easy": 1, "Medium": 2, "Hard": 3}
        sorted_qs = sorted(filtered_qs, key=lambda x: diff_order.get(x["difficulty"], 4))
        
        for q in sorted_qs:
            q_id = q["id"]
            
            with st.container(border=True):
                c_qh1, c_qh2 = st.columns([4, 1])
                with c_qh1:
                    st.markdown(f"Category: **{q['category']}** | Type: **{q['sub_type']}** | Difficulty: **{q['difficulty']}**")
                    st.markdown(f"##### Q: {q['question']}")
                with c_qh2:
                    is_book = st.checkbox("Bookmark", value=q["bookmarked"], key=f"q_book_{q_id}")
                    if is_book != q["bookmarked"]:
                        save_bookmark(user_id, "interview", q_id, is_book)
                        st.rerun()
                        
                    is_comp = st.checkbox("Complete", value=q["completed"], key=f"q_comp_{q_id}")
                    if is_comp != q["completed"]:
                        save_interview_progress(user_id, q_id, is_comp, q["notes"])
                        st.rerun()
                        
                show_ans = st.toggle("Show Answer", key=f"show_ans_{q_id}")
                if show_ans:
                    st.markdown(f"""
                    <div style="background-color: #0f172a; padding: 15px; border-radius: 6px; border-left: 4px solid #10b981; margin-top: 10px; margin-bottom: 15px; color: #f1f5f9; font-size: 14px;">
                        <b>Answer:</b><br/>{q['answer'].replace(chr(10), '<br/>')}
                    </div>
                    """, unsafe_allow_html=True)
                    
                with st.expander("Notes Log", expanded=False):
                    q_note = st.text_area("Write notes...", value=q["notes"], key=f"q_note_input_{q_id}", height=80, label_visibility="collapsed")
                    if st.button("Save Notes", key=f"save_q_note_{q_id}"):
                        save_interview_progress(user_id, q_id, q["completed"], q_note)
                        st.success("Notes saved.")
