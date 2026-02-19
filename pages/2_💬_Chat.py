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
    .chat-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .user-message {
        background: #667eea;
        color: white;
        padding: 1rem;
        border-radius: 10px 10px 0 10px;
        margin: 1rem 0;
        margin-left: 20%;
    }
    .bot-message {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 10px 10px 10px 0;
        margin: 1rem 0;
        margin-right: 20%;
        border-left: 4px solid #667eea;
    }
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 1rem;
        border: 1px solid #ddd;
        border-radius: 10px;
        background: white;
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
    st.markdown("## 💡 Quick Topics")
    
    quick_questions = [
        "📝 How to make effective notes?",
        "🧠 Best memory techniques",
        "⏰ Create a study timetable",
        "😴 Deal with exam stress",
        "📊 Improve focus and concentration",
        "🎯 Set study goals",
        "📚 Active recall techniques",
        "✍️ Exam preparation tips"
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
