import streamlit as st
from college.coding.database import (
    get_planner_tasks,
    save_planner_task,
    delete_planner_task,
    toggle_planner_task
)

def daily_planner():
    st.markdown("### Daily Planner")
    st.write("Track and execute your daily preparation targets, apply to internships, and monitor study schedules.")
    
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("Please log in to continue.")
        return
        
    # Form to add task
    with st.form("add_task_form", clear_on_submit=True):
        new_task = st.text_input("New Planning Task", placeholder="e.g. Review 3 SQL Join questions")
        sub_btn = st.form_submit_button("Add Task")
        if sub_btn and new_task.strip():
            save_planner_task(user_id, new_task.strip())
            st.success(f"Added task: {new_task.strip()}")
            st.rerun()
            
    # Retrieve tasks
    tasks = get_planner_tasks(user_id)
    
    # Pre-populate defaults if list is empty
    if not tasks:
        default_tasks = [
            "Complete 2 LeetCode practice problems",
            "Update Resume skill tags inside Resume Builder",
            "Take 1 Aptitude Logical Reasoning quiz"
        ]
        for t in default_tasks:
            save_planner_task(user_id, t)
        tasks = get_planner_tasks(user_id)
        
    st.write("")
    st.markdown("##### Active Checklist Tasks:")
    
    # Display tasks
    for task in tasks:
        t_id = task["id"]
        # Use checkboxes to toggle status
        checked = st.checkbox(
            task["task_text"],
            value=task["completed"],
            key=f"task_chk_{t_id}"
        )
        if checked != task["completed"]:
            toggle_planner_task(user_id, t_id, checked)
            st.rerun()
            
    st.divider()
    
    # Delete task selector
    if tasks:
        st.markdown("##### Remove Tasks:")
        task_delete_idx = st.selectbox(
            "Select task to delete",
            range(len(tasks)),
            format_func=lambda i: tasks[i]["task_text"]
        )
        if st.button("Delete Selected Task", type="secondary"):
            delete_planner_task(user_id, tasks[task_delete_idx]["id"])
            st.success("Task deleted.")
            st.rerun()
