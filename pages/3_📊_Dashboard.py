import streamlit as st
from datetime import datetime
import json
import sys
sys.path.append('..')
from auth import require_auth, get_current_user, logout

# ─── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

# ─── Authentication Check ──────────────────────────────────────
require_auth()
current_user = get_current_user()

# ─── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 👤 User Profile")
    st.write(f"**{current_user['username']}**")
    if st.button("🚪 Logout", use_container_width=True):
        logout()
        st.rerun()

# ─── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
    .dashboard-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
    .task-item {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        background: #f0f2f6;
    }
    .completed-task {
        opacity: 0.6;
        text-decoration: line-through;
    }
</style>
""", unsafe_allow_html=True)

# ─── Initialize Session State ──────────────────────────────────
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

if 'completed_tasks' not in st.session_state:
    st.session_state.completed_tasks = []

# ─── Header ────────────────────────────────────────────────────
st.markdown("""
<div class="dashboard-header">
    <h1>📊 Study Dashboard</h1>
    <p>Track your progress and manage study tasks</p>
</div>
""", unsafe_allow_html=True)

# ─── Metrics ───────────────────────────────────────────────────
st.markdown("## 📈 Your Progress")

col1, col2, col3, col4 = st.columns(4)

total_tasks = len(st.session_state.tasks)
completed = len([t for t in st.session_state.tasks if t.get('completed', False)])
pending = total_tasks - completed
completion_rate = (completed / total_tasks * 100) if total_tasks > 0 else 0

with col1:
    st.metric(
        label="📝 Total Tasks",
        value=total_tasks,
        delta=None
    )

with col2:
    st.metric(
        label="✅ Completed",
        value=completed,
        delta=None
    )

with col3:
    st.metric(
        label="⏳ Pending",
        value=pending,
        delta=None
    )

with col4:
    st.metric(
        label="📊 Completion Rate",
        value=f"{completion_rate:.1f}%",
        delta=None
    )

# Progress bar
if total_tasks > 0:
    st.progress(completion_rate / 100)

st.markdown("---")

# ─── Task Management ───────────────────────────────────────────
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("## ✅ Tasks & To-Do")
    
    if st.session_state.tasks:
        # Filter options
        filter_option = st.radio(
            "Show:",
            ["All", "Pending Only", "Completed Only"],
            horizontal=True
        )
        
        # Display tasks
        for idx, task in enumerate(st.session_state.tasks):
            is_completed = task.get('completed', False)
            
            # Apply filter
            if filter_option == "Pending Only" and is_completed:
                continue
            if filter_option == "Completed Only" and not is_completed:
                continue
            
            task_container = st.container()
            with task_container:
                col_check, col_task = st.columns([1, 10])
                
                with col_check:
                    if st.checkbox(
                        "✓",
                        value=is_completed,
                        key=f"task_{idx}",
                        label_visibility="collapsed"
                    ):
                        st.session_state.tasks[idx]['completed'] = True
                        st.session_state.tasks[idx]['completed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M')
                        st.rerun()
                    elif is_completed and not st.session_state.tasks[idx].get('completed', False):
                        st.session_state.tasks[idx]['completed'] = False
                        st.rerun()
                
                with col_task:
                    task_class = "completed-task" if is_completed else ""
                    priority_emoji = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(task.get('priority', 'Medium'), "🟡")
                    
                    st.markdown(f"""
                    <div class="task-item {task_class}">
                        <strong>{priority_emoji} {task['title']}</strong><br>
                        <small>📚 {task.get('subject', 'General')} | ⏰ Due: {task.get('due_date', 'No date')}</small>
                        {f"<br><small>✅ Completed: {task.get('completed_at', '')}</small>" if is_completed else ""}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Clear completed tasks
        if completed > 0:
            if st.button("🗑️ Clear Completed Tasks"):
                st.session_state.tasks = [t for t in st.session_state.tasks if not t.get('completed', False)]
                st.rerun()
    else:
        st.info("📝 No tasks yet! Add your first task using the form on the right.")

with col_right:
    st.markdown("## ➕ Add New Task")
    
    with st.form("add_task_form", clear_on_submit=True):
        task_title = st.text_input("Task Title *", placeholder="E.g., Complete Chapter 5")
        
        task_subject = st.selectbox(
            "Subject *",
            ["Mathematics", "Physics", "Chemistry", "Biology", "English", 
             "History", "Geography", "Computer Science", "Other"]
        )
        
        task_priority = st.select_slider(
            "Priority",
            options=["Low", "Medium", "High"],
            value="Medium"
        )
        
        task_due_date = st.date_input(
            "Due Date",
            value=datetime.now().date()
        )
        
        task_notes = st.text_area(
            "Notes (Optional)",
            placeholder="Additional details..."
        )
        
        submitted = st.form_submit_button("✅ Add Task", use_container_width=True)
        
        if submitted:
            if task_title:
                new_task = {
                    'title': task_title,
                    'subject': task_subject,
                    'priority': task_priority,
                    'due_date': task_due_date.strftime('%Y-%m-%d'),
                    'notes': task_notes,
                    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'completed': False
                }
                st.session_state.tasks.append(new_task)
                st.success("✅ Task added!")
                st.rerun()
            else:
                st.error("❌ Please enter a task title")

# ─── Study Insights ────────────────────────────────────────────
st.markdown("---")
st.markdown("## 💡 Study Insights")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📚 Tasks by Subject")
    if st.session_state.tasks:
        subject_counts = {}
        for task in st.session_state.tasks:
            subject = task.get('subject', 'Other')
            subject_counts[subject] = subject_counts.get(subject, 0) + 1
        
        for subject, count in sorted(subject_counts.items(), key=lambda x: x[1], reverse=True):
            completed_subject = len([t for t in st.session_state.tasks 
                                    if t.get('subject') == subject and t.get('completed', False)])
            st.write(f"**{subject}:** {completed_subject}/{count} completed")
    else:
        st.info("No data yet")

with col2:
    st.markdown("### 🎯 Tasks by Priority")
    if st.session_state.tasks:
        priority_counts = {"High": 0, "Medium": 0, "Low": 0}
        for task in st.session_state.tasks:
            if not task.get('completed', False):
                priority = task.get('priority', 'Medium')
                priority_counts[priority] += 1
        
        st.write(f"🔴 **High Priority:** {priority_counts['High']}")
        st.write(f"🟡 **Medium Priority:** {priority_counts['Medium']}")
        st.write(f"🟢 **Low Priority:** {priority_counts['Low']}")
    else:
        st.info("No data yet")

# ─── Study Plans ───────────────────────────────────────────────
if 'study_plans' in st.session_state and st.session_state.study_plans:
    st.markdown("---")
    st.markdown("## 📋 Your Study Plans")
    
    for idx, plan in enumerate(reversed(st.session_state.study_plans)):
        with st.expander(f"📅 Plan {len(st.session_state.study_plans) - idx}: {plan['name']} - {plan['level']}"):
            col_a, col_b = st.columns(2)
            with col_a:
                st.write(f"**Created:** {plan['created_at'].strftime('%Y-%m-%d %H:%M')}")
                st.write(f"**Exam Date:** {plan['exam_date']}")
            with col_b:
                st.write(f"**Subjects:** {plan['subjects']}")
                
                # Calculate days until exam
                days_left = (plan['exam_date'] - datetime.now().date()).days
                if days_left > 0:
                    st.info(f"⏰ {days_left} days until exam")
                else:
                    st.warning("⚠️ Exam date has passed")

# ─── Export Data ───────────────────────────────────────────────
if st.session_state.tasks:
    st.markdown("---")
    
    # Export tasks as JSON
    tasks_json = json.dumps(st.session_state.tasks, indent=2)
    
    st.download_button(
        label="📥 Export Tasks (JSON)",
        data=tasks_json,
        file_name=f"study_tasks_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json"
    )
