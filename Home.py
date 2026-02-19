import streamlit as st
from auth import show_auth_page, init_auth, logout, get_current_user

# ─── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="AI Study Planner",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Authentication Check ──────────────────────────────────────
init_auth()

# If not logged in, show auth page
if not st.session_state.get('logged_in', False):
    show_auth_page()
    st.stop()

# Get current user
current_user = get_current_user()

# ─── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .feature-card {
        padding: 1.5rem;
        border-radius: 10px;
        background: #f0f2f6;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1.1rem;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    .education-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        background: #667eea;
        color: white;
        border-radius: 20px;
        margin: 0.5rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ─── Sidebar - User Info ───────────────────────────────────────
with st.sidebar:
    st.markdown("### 👤 User Profile")
    st.write(f"**Username:** {current_user['username']}")
    st.write(f"**Email:** {current_user['email']}")
    st.write(f"**Member since:** {current_user['created_at'][:10]}")
    
    st.markdown("---")
    
    if st.button("🚪 Logout", use_container_width=True):
        logout()
        st.rerun()
    
    st.markdown("---")
    st.info("💡 Use the pages menu above to navigate")

# ─── Header ────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🎓 AI Study Planner</h1>
    <p style='font-size: 1.2rem; margin-top: 0.5rem;'>
        Your Personal AI-Powered Study Assistant
    </p>
    <p style='font-size: 0.9rem; opacity: 0.9;'>
        🤖 Powered by Gemini API
    </p>
</div>
""", unsafe_allow_html=True)

# ─── Hero Section ──────────────────────────────────────────────
col1, col2 = st.columns([1.5, 1])

with col1:
    st.markdown("## 📚 Generate Personalized Study Plans")
    st.markdown("""
    Create intelligent study schedules tailored for:
    
    <span class="education-badge">📖 10th Standard</span>
    <span class="education-badge">📘 12th Standard</span>
    <span class="education-badge">🎓 B.Tech</span>
    <span class="education-badge">💼 MBA</span>
    """, unsafe_allow_html=True)
    
    st.markdown("### ✨ Key Features:")
    st.markdown("""
    - 🧠 **Smart AI Plans** - Hour-by-hour personalized schedules
    - ⚠️ **Weak Subject Focus** - Extra time for challenging topics
    - 📊 **Progress Tracking** - Monitor your study achievements
    - 💬 **AI Chat Assistant** - Get instant study help
    - 💡 **Motivation Boosts** - Daily encouragement
    """)

with col2:
    st.markdown("### 🚀 Quick Actions")
    
    if st.button("📅 Generate Study Plan", key="plan_btn"):
        st.switch_page("pages/1_📅_Study_Planner.py")
    
    if st.button("💬 Chat with AI Assistant", key="chat_btn"):
        st.switch_page("pages/2_💬_Chat.py")
    
    if st.button("📊 View Dashboard", key="dash_btn"):
        st.switch_page("pages/3_📊_Dashboard.py")
    
    st.info("👈 Use the sidebar to navigate between pages")

# ─── How It Works ──────────────────────────────────────────────
st.markdown("---")
st.markdown("## 🔄 How It Works")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>1️⃣ Input Details</h3>
        <p>Enter your education level, subjects, exam date, and study hours</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>2️⃣ AI Analysis</h3>
        <p>Gemini API analyzes your needs and creates optimal schedule</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>3️⃣ Get Plan</h3>
        <p>Receive detailed day-by-day study timetable with tasks</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-card">
        <h3>4️⃣ Track Progress</h3>
        <p>Mark tasks complete and monitor your achievement</p>
    </div>
    """, unsafe_allow_html=True)

# ─── Education Levels ──────────────────────────────────────────
st.markdown("---")
st.markdown("## 🎯 Supported Education Levels")

col1, col2 = st.columns(2)

with col1:
    with st.expander("📖 10th & 12th Standard"):
        st.markdown("""
        - **CBSE, ICSE, State Boards**
        - Core subjects: Math, Physics, Chemistry, Biology
        - Languages: English, Hindi, Regional
        - Board exam preparation
        """)
    
    with st.expander("🎓 B.Tech / Engineering"):
        st.markdown("""
        - All engineering streams
        - Semester exams & GATE preparation
        - Core: Programming, Math, Engineering subjects
        - Project planning & placement prep
        """)

with col2:
    with st.expander("💼 MBA & Management"):
        st.markdown("""
        - CAT, MAT, XAT preparation
        - MBA curriculum planning
        - Finance, Marketing, Operations, HR
        - Case study preparation
        """)
    
    with st.expander("🎯 Competitive Exams"):
        st.markdown("""
        - JEE, NEET, UPSC preparation
        - Banking exams (SSC, IBPS)
        - Custom exam schedules
        """)

# ─── Footer ────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>🎓 AI Study Planner © 2026 | Powered by Gemini API</p>
    <p style='font-size: 0.9rem;'>Built with Streamlit & Google Gemini AI</p>
</div>
""", unsafe_allow_html=True)
