import streamlit as st
import requests
from datetime import datetime
import sys
sys.path.append('..')
from auth import require_auth, get_current_user, logout

# ─── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="💬",
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
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

# ─── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
    
    * { font-family: 'Poppins', sans-serif; }
    
    .stApp {
        background: linear-gradient(135deg, #000000 0%, #0a0a0a 25%, #001520 50%, #0a0a0a 75%, #000000 100%);
    }
    
    .chat-header {
        background: linear-gradient(135deg, #000000 0%, #00d9ff 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(0, 217, 255, 0.4);
        border: 2px solid rgba(0, 217, 255, 0.3);
    }
    
    .user-message {
        background: linear-gradient(135deg, #000000 0%, #00d9ff 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px 15px 5px 15px;
        margin: 1rem 0;
        margin-left: 20%;
        box-shadow: 0 4px 15px rgba(0, 217, 255, 0.3);
    }
    
    .bot-message {
        background: linear-gradient(135deg, rgba(255,255,255,0.98) 0%, rgba(240,240,240,0.98) 100%);
        padding: 1rem;
        border-radius: 15px 15px 15px 5px;
        margin: 1rem 0;
        margin-right: 20%;
        border-left: 4px solid #00d9ff;
        box-shadow: 0 4px 15px rgba(0, 217, 255, 0.2);
    }
    
    .category-card {
        background: linear-gradient(135deg, rgba(0, 217, 255, 0.1) 0%, rgba(0, 184, 212, 0.1) 100%);
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border: 2px solid rgba(0, 217, 255, 0.3);
        transition: all 0.3s ease;
    }
    
    .category-card:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 15px rgba(0, 217, 255, 0.4);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #000000 0%, #00d9ff 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.6rem 1rem !important;
        border-radius: 10px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 10px rgba(0, 217, 255, 0.3) !important;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #00b8d4 0%, #00ffea 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 15px rgba(0, 217, 255, 0.5) !important;
    }
</style>
""", unsafe_allow_html=True)

# ─── Initialize Session State ──────────────────────────────────
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [
        {
            'role': 'bot',
            'content': """👋 Hi! I'm your AI Study Assistant powered by Gemini API.

I can help you with:
- 📅 Study planning & timetables
- 📚 Subject-specific doubts
- 🧠 Memory & learning techniques
- 💡 Motivation & productivity tips
- ⏰ Time management strategies

What would you like help with today?""",
            'timestamp': datetime.now()
        }
    ]

# ─── Header ────────────────────────────────────────────────────
st.markdown("""
<div class="chat-header">
    <h1>💬 AI Study Chat Assistant</h1>
    <p>Get instant help with your studies powered by Gemini AI</p>
</div>
""", unsafe_allow_html=True)

# ─── Chat Interface ────────────────────────────────────────────
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("## 💭 Chat")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f"""
                <div class="user-message">
                    <strong>👤 You:</strong><br>
                    {message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="bot-message">
                    <strong>🤖 AI Assistant:</strong><br>
                    {message['content']}
                </div>
                """, unsafe_allow_html=True)
    
    # Chat input
    st.markdown("---")
    user_input = st.text_area(
        "Your message:",
        placeholder="Ask me anything about studying...",
        height=100,
        key="user_input"
    )
    
    col_send, col_clear = st.columns([1, 1])
    
    with col_send:
        send_button = st.button("📤 Send Message", use_container_width=True)
    
    with col_clear:
        clear_button = st.button("🗑️ Clear Chat", use_container_width=True)
    
    if send_button and user_input:
        # Add user message to history
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input,
            'timestamp': datetime.now()
        })
        
        # Build context-aware prompt
        prompt = f"""You are an AI Study Assistant helping students with their studies. 
Previous conversation context:
{chr(10).join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.chat_history[-3:]])}

Student's new question: {user_input}

Provide a helpful, encouraging, and informative response. Be specific and actionable."""
        
        # Get AI response
        with st.spinner("🤖 AI is thinking..."):
            response = call_gemini_api(prompt)
        
        # Add bot response to history
        st.session_state.chat_history.append({
            'role': 'bot',
            'content': response,
            'timestamp': datetime.now()
        })
        
        st.rerun()
    
    if clear_button:
        st.session_state.chat_history = [st.session_state.chat_history[0]]
        st.rerun()

with col2:
    st.markdown("## � Quick Planner")
    
    # Initialize education level in session state
    if 'selected_education_level' not in st.session_state:
        st.session_state.selected_education_level = "Class 10th"
    
    # Education level selector
    education_levels = [
        "📖 Class 10th",
        "📘 Class 12th - Science",
        "📙 Class 12th - Commerce", 
        "📕 Class 12th - Arts",
        "🎓 B.Tech - Computer Science",
        "🎓 B.Tech - Electrical/Electronics",
        "🎓 B.Tech - Mechanical",
        "🎓 B.Tech - Civil",
        "💼 MBA - All Streams",
        "🎯 Competitive Exams (JEE/NEET)"
    ]
    
    selected_level = st.selectbox(
        "Select Your Level:",
        options=education_levels,
        key="education_level_select"
    )
    
    st.markdown(f"### {selected_level}")
    
    # Quick planner actions
    col_a, col_b = st.columns(2)
    
    with col_a:
        if st.button("📅 Create Timetable", key="create_timetable", use_container_width=True):
            st.session_state.chat_history.append({
                'role': 'user',
                'content': f"Create a detailed study timetable for {selected_level}",
                'timestamp': datetime.now()
            })
            
            prompt = f"""You are an AI Study Assistant. Create a comprehensive daily study timetable for a {selected_level} student.

Include:
1. Optimal study hours (morning, afternoon, evening)
2. Subject allocation with time slots
3. Break times and duration
4. Revision sessions
5. Tips specific to this education level
6. Balanced schedule for weekdays and weekends

Make it practical and easy to follow!"""
            
            with st.spinner("🤖 Creating your timetable..."):
                response = call_gemini_api(prompt)
            
            st.session_state.chat_history.append({
                'role': 'bot',
                'content': response,
                'timestamp': datetime.now()
            })
            
            st.rerun()
    
    with col_b:
        if st.button("📋 Study Planner", key="create_planner", use_container_width=True):
            st.session_state.chat_history.append({
                'role': 'user',
                'content': f"Create a study plan for {selected_level}",
                'timestamp': datetime.now()
            })
            
            prompt = f"""You are an AI Study Assistant. Create a comprehensive study plan for a {selected_level} student.

Include:
1. Key subjects and topics to cover
2. Week-by-week breakdown
3. Important chapters/units priority
4. Revision strategy
5. Exam preparation timeline
6. Study resources and techniques

Make it detailed and motivating!"""
            
            with st.spinner("🤖 Preparing your study plan..."):
                response = call_gemini_api(prompt)
            
            st.session_state.chat_history.append({
                'role': 'bot',
                'content': response,
                'timestamp': datetime.now()
            })
            
            st.rerun()
    
    # Quick subject help
    st.markdown("#### 📚 Subject-Specific Help")
    
    subject_help_options = {
        "Class 10th": ["Math", "Science", "Social Studies", "English"],
        "Class 12th": ["Physics", "Chemistry", "Math", "Biology", "Economics", "Accounts"],
        "B.Tech": ["Programming", "Data Structures", "DBMS", "Operating Systems"],
        "MBA": ["Marketing", "Finance", "HR", "Operations"],
        "Competitive": ["Quantitative Aptitude", "Reasoning", "General Knowledge"]
    }
    
    # Determine subject category based on selected level
    subject_category = "Class 10th"
    if "12th" in selected_level:
        subject_category = "Class 12th"
    elif "B.Tech" in selected_level:
        subject_category = "B.Tech"
    elif "MBA" in selected_level:
        subject_category = "MBA"
    elif "Competitive" in selected_level:
        subject_category = "Competitive"
    
    subjects = subject_help_options.get(subject_category, ["Math", "Science", "English"])
    
    for subject in subjects[:3]:  # Show first 3 subjects
        if st.button(f"📖 {subject} Help", key=f"subject_{subject}", use_container_width=True):
            st.session_state.chat_history.append({
                'role': 'user',
                'content': f"How to study {subject} effectively for {selected_level}?",
                'timestamp': datetime.now()
            })
            
            prompt = f"""You are an AI Study Assistant. Provide effective study strategies for {subject} specifically for {selected_level} students.

Include:
1. Key topics to focus on
2. Best study methods for this subject
3. Common mistakes to avoid
4. Resource recommendations
5. Practice tips
6. Time management for this subject

Be specific and practical!"""
            
            with st.spinner("🤖 Preparing subject guidance..."):
                response = call_gemini_api(prompt)
            
            st.session_state.chat_history.append({
                'role': 'bot',
                'content': response,
                'timestamp': datetime.now()
            })
            
            st.rerun()
    
    st.markdown("---")
    st.markdown("## �🎯 Study Categories")
    
    # Category-based recommendations
    categories = {
        "📚 Study Techniques": [
            "Pomodoro Technique guide",
            "Active recall strategies",
            "Spaced repetition tips",
            "Feynman technique explained"
        ],
        "⏰ Time Management": [
            "Create effective timetable",
            "Beat procrastination",
            "Prioritize tasks",
            "Balance study & breaks"
        ],
        "📝 Exam Preparation": [
            "Last-minute revision tips",
            "Manage exam anxiety",
            "Practice test strategies",
            "Improve answer writing"
        ],
        "💪 Motivation": [
            "Stay motivated daily",
            "Overcome study burnout",
            "Set achievable goals",
            "Build study habits"
        ],
        "🧠 Memory & Focus": [
            "Boost concentration",
            "Memory improvement tricks",
            "Avoid distractions",
            "Deep work techniques"
        ]
    }
    
    selected_category = st.selectbox(
        "Choose a category:",
        options=list(categories.keys()),
        key="category_select"
    )
    
    st.markdown(f"### {selected_category}")
    
    for recommendation in categories[selected_category]:
        if st.button(f"💡 {recommendation}", key=recommendation, use_container_width=True):
            st.session_state.chat_history.append({
                'role': 'user',
                'content': f"{recommendation} (from {selected_category})",
                'timestamp': datetime.now()
            })
            
            # Enhanced prompt with category context
            prompt = f"""You are an AI Study Assistant. A student is asking about {recommendation} from the {selected_category} category.
            
Provide detailed, practical advice with:
1. Clear explanation
2. Step-by-step guide
3. Real examples
4. Common mistakes to avoid
5. Quick action tips

Make it engaging and actionable!"""
            
            with st.spinner("🤖 AI is preparing recommendations..."):
                response = call_gemini_api(prompt)
            
            st.session_state.chat_history.append({
                'role': 'bot',
                'content': response,
                'timestamp': datetime.now()
            })
            
            st.rerun()
    
    st.markdown("---")
    st.markdown("## 💡 Quick Topics")
    
    quick_questions = [
        "📝 How to make effective notes?",
        "🧠 Best memory techniques",
        "⏰ Create a study timetable",
        "😴 Deal with exam stress"
    ]
    
    for question in quick_questions:
        if st.button(question, key=question, use_container_width=True):
            st.session_state.chat_history.append({
                'role': 'user',
                'content': question.split(' ', 1)[1],
                'timestamp': datetime.now()
            })
            
            prompt = f"""You are an AI Study Assistant. Answer this question with practical, actionable advice:
{question.split(' ', 1)[1]}"""
            
            with st.spinner("🤖 AI is thinking..."):
                response = call_gemini_api(prompt)
            
            st.session_state.chat_history.append({
                'role': 'bot',
                'content': response,
                'timestamp': datetime.now()
            })
            
            st.rerun()
    
    st.markdown("---")
    st.info("💡 **Pro Tip:** Be specific with your questions for better answers!")
    
    # Chat stats
    st.markdown("### 📊 Chat Stats")
    st.metric("Messages", len(st.session_state.chat_history))
    st.metric("Your Questions", len([m for m in st.session_state.chat_history if m['role'] == 'user']))

# ─── Export Chat ───────────────────────────────────────────────
if len(st.session_state.chat_history) > 1:
    st.markdown("---")
    chat_export = "\n\n".join([
        f"[{msg['timestamp'].strftime('%Y-%m-%d %H:%M')}] {msg['role'].upper()}: {msg['content']}"
        for msg in st.session_state.chat_history
    ])
    
    st.download_button(
        label="📥 Download Chat History",
        data=chat_export,
        file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
        mime="text/plain"
    )
