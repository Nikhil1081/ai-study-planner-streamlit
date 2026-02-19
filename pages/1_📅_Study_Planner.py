import streamlit as st
import requests
from datetime import datetime, timedelta
import sys
sys.path.append('..')
from auth import require_auth, get_current_user, logout

# ─── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Study Planner",
    page_icon="📅",
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

# ─── Gemini API Config ─────────────────────────────────────────
GEMINI_API_KEY = "AIzaSyBO3qiLuaIDE4lN5tfOe78owEw6onp5ZmU"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={GEMINI_API_KEY}"

def call_gemini_api(prompt):
    """Call Gemini API with given prompt"""
    try:
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }
        response = requests.post(GEMINI_API_URL, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
        else:
            return f"Error: {response.status_code} - {response.text[:200]}"
    except Exception as e:
        return f"Error calling API: {str(e)}"

# ─── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
    
    * { font-family: 'Poppins', sans-serif; }
    
    .stApp {
        background: linear-gradient(135deg, #000000 0%, #0a0a0a 25%, #001520 50%, #0a0a0a 75%, #000000 100%);
    }
    
    .plan-header {
        background: linear-gradient(135deg, #000000 0%, #00d9ff 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(0, 217, 255, 0.4);
        border: 2px solid rgba(0, 217, 255, 0.3);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #000000 0%, #00d9ff 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 2rem !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0, 217, 255, 0.4) !important;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #00b8d4 0%, #00ffea 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(0, 217, 255, 0.6) !important;
    }
</style>
""", unsafe_allow_html=True)

# ─── Header ────────────────────────────────────────────────────
st.markdown("""
<div class="plan-header">
    <h1>📅 AI Study Plan Generator</h1>
    <p>Create personalized study schedules powered by Gemini AI</p>
</div>
""", unsafe_allow_html=True)

# ─── Form ──────────────────────────────────────────────────────
st.markdown("## 📝 Enter Your Details")

with st.form("study_plan_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("👤 Your Name", placeholder="Enter your name")
        
        education_level = st.selectbox(
            "🎓 Education Level",
            [
                "10th Standard",
                "12th Standard - Science",
                "12th Standard - Commerce",
                "12th Standard - Arts",
                "B.Tech - Computer Science",
                "B.Tech - Electrical/Electronics",
                "B.Tech - Mechanical",
                "B.Tech - Civil",
                "MBA - All Streams"
            ]
        )
        
        subjects = st.text_area(
            "📚 Subjects to Cover",
            placeholder="E.g., Math, Physics, Chemistry, Biology",
            help="Enter subjects separated by commas"
        )
    
    with col2:
        exam_date = st.date_input(
            "📆 Exam Date",
            min_value=datetime.now().date(),
            value=datetime.now().date() + timedelta(days=30)
        )
        
        study_hours = st.slider(
            "⏰ Daily Study Hours",
            min_value=1,
            max_value=16,
            value=6,
            help="How many hours can you study per day?"
        )
        
        weak_subjects = st.text_input(
            "⚠️ Weak Subjects (Optional)",
            placeholder="Subjects you need extra focus on",
            help="These will get more study time"
        )
    
    # Additional options
    with st.expander("⚙️ Advanced Options"):
        include_breaks = st.checkbox("Include break times", value=True)
        include_revision = st.checkbox("Include revision sessions", value=True)
        difficulty = st.select_slider(
            "Study Intensity",
            options=["Light", "Moderate", "Intense", "Very Intense"],
            value="Moderate"
        )
    
    # Submit button
    submitted = st.form_submit_button("🚀 Generate Study Plan", use_container_width=True)

# ─── Generate Plan ─────────────────────────────────────────────
if submitted:
    if not name or not subjects:
        st.error("❌ Please fill in your name and subjects!")
    else:
        # Calculate days until exam
        days_until_exam = (exam_date - datetime.now().date()).days
        
        # Build prompt for Gemini
        prompt = f"""Create a detailed study plan with the following details:

Student Name: {name}
Education Level: {education_level}
Subjects: {subjects}
Exam Date: {exam_date} (in {days_until_exam} days)
Daily Study Hours: {study_hours} hours
Weak Subjects: {weak_subjects if weak_subjects else "None specified"}
Include Breaks: {include_breaks}
Include Revision: {include_revision}
Study Intensity: {difficulty}

Generate a comprehensive study plan that includes:
1. Week-by-week breakdown
2. Daily study schedule with time slots
3. Subject allocation based on importance and difficulty
4. Extra time for weak subjects
5. Regular revision sessions
6. Break times for rest
7. Tips for effective studying
8. Motivational advice

Format the plan in a clear, organized way with proper sections and bullet points."""

        # Show loading
        with st.spinner("🤖 AI is creating your personalized study plan..."):
            plan = call_gemini_api(prompt)
        
        # Display result
        if plan and not plan.startswith("Error"):
            st.success("✅ Your study plan is ready!")
            
            # Save to session state
            if 'study_plans' not in st.session_state:
                st.session_state.study_plans = []
            
            st.session_state.study_plans.append({
                'name': name,
                'level': education_level,
                'subjects': subjects,
                'exam_date': exam_date,
                'plan': plan,
                'created_at': datetime.now()
            })
            
            st.markdown("---")
            st.markdown("## 📋 Your Personalized Study Plan")
            st.markdown(plan)
            
            # Download button
            st.download_button(
                label="📥 Download Plan",
                data=f"Study Plan for {name}\n\n{plan}",
                file_name=f"study_plan_{name}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
        else:
            st.error(f"❌ Failed to generate plan: {plan}")

# ─── Previous Plans ────────────────────────────────────────────
if 'study_plans' in st.session_state and st.session_state.study_plans:
    st.markdown("---")
    st.markdown("## 📚 Previous Study Plans")
    
    for idx, plan in enumerate(reversed(st.session_state.study_plans)):
        with st.expander(f"Plan {len(st.session_state.study_plans) - idx}: {plan['name']} - {plan['level']}"):
            st.markdown(f"**Created:** {plan['created_at'].strftime('%Y-%m-%d %H:%M')}")
            st.markdown(f"**Exam Date:** {plan['exam_date']}")
            st.markdown(f"**Subjects:** {plan['subjects']}")
            st.markdown("---")
            st.markdown(plan['plan'])
