import streamlit as st
from auth_db import AuthDB
import re

def init_auth():
    """Initialize authentication session state"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_info' not in st.session_state:
        st.session_state.user_info = None
    if 'auth_page' not in st.session_state:
        st.session_state.auth_page = 'login'
    if 'reset_email' not in st.session_state:
        st.session_state.reset_email = None
    if 'reset_token_sent' not in st.session_state:
        st.session_state.reset_token_sent = False
    if 'stored_reset_token' not in st.session_state:
        st.session_state.stored_reset_token = None

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_username(username):
    """Validate username (3-20 chars, alphanumeric + underscore)"""
    pattern = r'^[a-zA-Z0-9_]{3,20}$'
    return re.match(pattern, username) is not None

def validate_password(password):
    """Validate password strength (min 6 chars)"""
    return len(password) >= 6

def show_login_page():
    """Display beautiful login page"""
    st.markdown("""
    <div class="auth-logo">
        <div class="auth-logo-icon">🎓</div>
        <h1 class="auth-title">Welcome Back!</h1>
        <p class="auth-subtitle">Sign in to continue your learning journey</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("👤 Username", placeholder="Enter your username")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("🚀 Login", use_container_width=True)
        with col2:
            register_btn = st.form_submit_button("📝 Sign Up", use_container_width=True)
        
        if submit:
            if not username or not password:
                st.markdown('<div class="error-msg">❌ Please fill in all fields!</div>', unsafe_allow_html=True)
            else:
                db = AuthDB()
                success, result = db.login_user(username, password)
                
                if success:
                    st.session_state.logged_in = True
                    st.session_state.user_info = result
                    st.markdown(f'<div class="success-msg">✅ Welcome back, {result["username"]}!</div>', unsafe_allow_html=True)
                    st.balloons()
                    st.rerun()
                else:
                    st.markdown(f'<div class="error-msg">❌ {result}</div>', unsafe_allow_html=True)
        
        if register_btn:
            st.session_state.auth_page = 'register'
            st.rerun()
    
    # Forgot password link
    st.markdown('<div class="auth-divider"><span>OR</span></div>', unsafe_allow_html=True)
    
    if st.button("🔑 Forgot Password?", use_container_width=True):
        st.session_state.auth_page = 'forgot'
        st.rerun()
    
    # Features 
    st.markdown("""
    <div class="info-box">
        <div class="feature-item">
            <span class="feature-icon">🎯</span>
            <span>AI-Powered Study Plans</span>
        </div>
        <div class="feature-item">
            <span class="feature-icon">💬</span>
            <span>Smart Chat Assistant</span>
        </div>
        <div class="feature-item">
            <span class="feature-icon">📊</span>
            <span>Progress Tracking</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_register_page():
    """Display beautiful registration page"""
    st.markdown("""
    <div class="auth-logo">
        <div class="auth-logo-icon">🌟</div>
        <h1 class="auth-title">Join Us!</h1>
        <p class="auth-subtitle">Create your account and start learning smarter</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("register_form", clear_on_submit=False):
        username = st.text_input("👤 Username", placeholder="Choose a unique username (3-20 chars)")
        email = st.text_input("📧 Email", placeholder="your.email@example.com")
        password = st.text_input("🔒 Password", type="password", placeholder="Minimum 6 characters")
        confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Re-enter password")
        
        st.markdown("""
        <div class="info-box">
            <strong>Password Requirements:</strong><br>
            • Minimum 6 characters<br>
            • Use a strong password
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("✅ Create Account", use_container_width=True)
        with col2:
            back_btn = st.form_submit_button("🔙 Back to Login", use_container_width=True)
        
        if submit:
            if not username or not email or not password or not confirm_password:
                st.markdown('<div class="error-msg">❌ Please fill in all fields!</div>', unsafe_allow_html=True)
            elif not validate_username(username):
                st.markdown('<div class="error-msg">❌ Username must be 3-20 characters (letters, numbers, underscore only)</div>', unsafe_allow_html=True)
            elif not validate_email(email):
                st.markdown('<div class="error-msg">❌ Please enter a valid email address!</div>', unsafe_allow_html=True)
            elif not validate_password(password):
                st.markdown('<div class="error-msg">❌ Password must be at least 6 characters!</div>', unsafe_allow_html=True)
            elif password != confirm_password:
                st.markdown('<div class="error-msg">❌ Passwords don\'t match!</div>', unsafe_allow_html=True)
            else:
                db = AuthDB()
                success, message = db.register_user(username, email, password)
                
                if success:
                    st.markdown('<div class="success-msg">✅ Registration successful! Please login.</div>', unsafe_allow_html=True)
                    st.balloons()
                    st.session_state.auth_page = 'login'
                    st.rerun()
                else:
                    st.markdown(f'<div class="error-msg">❌ {message}</div>', unsafe_allow_html=True)
        
        if back_btn:
            st.session_state.auth_page = 'login'
            st.rerun()

def show_forgot_password_page():
    """Display forgot password page with email verification"""
    st.markdown("""
    <div class="auth-logo">
        <div class="auth-logo-icon">🔑</div>
        <h1 class="auth-title">Reset Password</h1>
        <p class="auth-subtitle">Enter your email to receive a reset code</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.reset_token_sent:
        # Step 1: Request reset code
        with st.form("forgot_form"):
            email = st.text_input("📧 Email Address", placeholder="your.email@example.com")
            
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("📨 Send Reset Code", use_container_width=True)
            with col2:
                back_btn = st.form_submit_button("🔙 Back to Login", use_container_width=True)
            
            if submit:
                if not email or not validate_email(email):
                    st.markdown('<div class="error-msg">❌ Please enter a valid email!</div>', unsafe_allow_html=True)
                else:
                    db = AuthDB()
                    success, result = db.generate_reset_token(email)
                    
                    if success:
                        st.session_state.reset_email = email
                        st.session_state.stored_reset_token = result['reset_token']
                        st.session_state.reset_token_sent = True
                        
                        # Display code (in production, send via email)
                        st.markdown(f'''
                        <div class="success-msg">
                            ✅ Reset code generated!<br>
                            <strong>Your reset code: {result["reset_token"]}</strong><br>
                            <small>(In production, this would be sent to your email)</small>
                        </div>
                        ''', unsafe_allow_html=True)
                        st.rerun()
                    else:
                        st.markdown(f'<div class="error-msg">❌ {result}</div>', unsafe_allow_html=True)
            
            if back_btn:
                st.session_state.auth_page = 'login'
                st.session_state.reset_token_sent = False
                st.rerun()
    
    else:
        # Step 2: Verify code and reset password
        st.markdown(f"""
        <div class="info-box">
            📧 Reset code sent to: <strong>{st.session_state.reset_email}</strong><br>
            Code: <strong>{st.session_state.stored_reset_token}</strong>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("reset_form"):
            reset_code = st.text_input("🔢 Enter 6-Digit Code", placeholder="Enter the code", max_chars=6)
            new_password = st.text_input("🔒 New Password", type="password", placeholder="Enter new password")
            confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Confirm new password")
            
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("✅ Reset Password", use_container_width=True)
            with col2:
                cancel_btn = st.form_submit_button("❌ Cancel", use_container_width=True)
            
            if submit:
                if not reset_code or not new_password or not confirm_password:
                    st.markdown('<div class="error-msg">❌ Please fill in all fields!</div>', unsafe_allow_html=True)
                elif len(reset_code) != 6:
                    st.markdown('<div class="error-msg">❌ Reset code must be 6 digits!</div>', unsafe_allow_html=True)
                elif not validate_password(new_password):
                    st.markdown('<div class="error-msg">❌ Password must be at least 6 characters!</div>', unsafe_allow_html=True)
                elif new_password != confirm_password:
                    st.markdown('<div class="error-msg">❌ Passwords don\'t match!</div>', unsafe_allow_html=True)
                else:
                    db = AuthDB()
                    # Verify token
                    verified, msg = db.verify_reset_token(st.session_state.reset_email, reset_code)
                    
                    if verified:
                        # Reset password
                        success, message = db.reset_password(st.session_state.reset_email, new_password)
                        
                        if success:
                            st.markdown('<div class="success-msg">✅ Password reset successful! Please login with your new password.</div>', unsafe_allow_html=True)
                            st.balloons()
                            st.session_state.auth_page = 'login'
                            st.session_state.reset_token_sent = False
                            st.session_state.reset_email = None
                            st.session_state.stored_reset_token = None
                            st.rerun()
                        else:
                            st.markdown(f'<div class="error-msg">❌ {message}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="error-msg">❌ {msg}</div>', unsafe_allow_html=True)
            
            if cancel_btn:
                st.session_state.auth_page = 'login'
                st.session_state.reset_token_sent = False
                st.session_state.reset_email = None
                st.session_state.stored_reset_token = None
                st.rerun()

def show_auth_page():
    """Main authentication page handler with beautiful UI"""
    init_auth()
    
    # Load custom CSS
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
        
        * { font-family: 'Poppins', sans-serif; }
        
        .stApp {
            background: linear-gradient(135deg, #000000 0%, #0a0a0a 20%, #001a1a 40%, #00152e 60%, #0a0a0a 80%, #000000 100%);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .main .block-container {
            max-width: 600px;
            padding: 2rem 1rem;
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(10px);
            border-radius: 30px;
            box-shadow: 0 20px 60px rgba(0, 217, 255, 0.3), 0 0 40px rgba(0, 217, 255, 0.1);
            margin: 2rem auto;
            border: 2px solid rgba(0, 217, 255, 0.4);
        }
        
        .auth-logo { text-align: center; margin-bottom: 2rem; }
        
        .auth-logo-icon {
            font-size: 4rem;
            animation: pulse 2s ease-in-out infinite;
            filter: drop-shadow(0 0 20px rgba(0, 217, 255, 0.6));
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        
        .auth-title {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #000000 0%, #00d9ff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 1rem 0 0.5rem 0;
            filter: drop-shadow(0 2px 4px rgba(0, 217, 255, 0.3));
        }
        
        .auth-subtitle {
            color: #555555;
            font-size: 1rem;
            margin-bottom: 2rem;
        }
        
        .stTextInput>div>div>input {
            border-radius: 15px !important;
            border: 2px solid #e0e0e0 !important;
            padding: 0.8rem 1rem !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
            background: white !important;
        }
        
        .stTextInput>div>div>input:focus {
            border-color: #00d9ff !important;
            box-shadow: 0 0 0 3px rgba(0, 217, 255, 0.2) !important;
        }
        
        .stButton>button {
            border-radius: 15px !important;
            padding: 0.8rem 2rem !important;
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            background: linear-gradient(135deg, #000000 0%, #00d9ff 100%) !important;
            color: white !important;
            border: none !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(0, 217, 255, 0.4);
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(0, 217, 255, 0.6) !important;
            background: linear-gradient(135deg, #00b8d4 0%, #00ffea 100%) !important;
        }
        
        .success-msg {
            background: linear-gradient(135deg, #000000 0%, #00b8d4 100%);
            color: white;
            padding: 1rem;
            border-radius: 15px;
            margin: 1rem 0;
            text-align: center;
            font-weight: 600;
            animation: slideIn 0.5s ease;
            border: 2px solid #00d9ff;
            box-shadow: 0 4px 20px rgba(0, 217, 255, 0.5);
        }
        
        .error-msg {
            background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%);
            color: white;
            padding: 1rem;
            border-radius: 15px;
            margin: 1rem 0;
            text-align: center;
            font-weight: 600;
            animation: shake 0.5s ease;
            border: 2px solid #ff3366;
            box-shadow: 0 4px 15px rgba(255, 51, 102, 0.3);
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-10px); }
            75% { transform: translateX(10px); }
        }
        
        .auth-divider {
            text-align: center;
            margin: 2rem 0;
            position: relative;
        }
        
        .auth-divider::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 0;
            right: 0;
            height: 1px;
            background: #dee2e6;
        }
        
        .auth-divider span {
            background: rgba(255, 255, 255, 0.95);
            padding: 0 1rem;
            position: relative;
            color: #6c757d;
            font-weight: 600;
        }
        
        .info-box {
            background: linear-gradient(135deg, rgba(0, 217, 255, 0.08) 0%, rgba(0, 184, 212, 0.08) 100%);
            border-left: 4px solid #00d9ff;
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
            box-shadow: 0 2px 10px rgba(0, 217, 255, 0.1);
        }
        
        .feature-item {
            display: flex;
            align-items: center;
            margin: 0.5rem 0;
            color: #495057;
        }
        
        .feature-icon {
            font-size: 1.5rem;
            margin-right: 0.5rem;
        }
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)
    
    if st.session_state.logged_in:
        return True
    
    # Show appropriate page
    if st.session_state.auth_page == 'login':
        show_login_page()
    elif st.session_state.auth_page == 'register':
        show_register_page()
    elif st.session_state.auth_page == 'forgot':
        show_forgot_password_page()
    
    return False

def logout():
    """Logout current user"""
    st.session_state.logged_in = False
    st.session_state.user_info = None
    st.session_state.auth_page = 'login'
    st.session_state.reset_email = None
    st.session_state.reset_token_sent = False
    st.session_state.stored_reset_token = None
    # Clear other session state variables
    for key in list(st.session_state.keys()):
        if key not in ['logged_in', 'user_info', 'auth_page', 'reset_email', 'reset_token_sent', 'stored_reset_token']:
            del st.session_state[key]

def require_auth():
    """Decorator-like function to protect pages"""
    init_auth()
    
    if not st.session_state.logged_in:
        st.warning("⚠️ Please login to access this page")
        show_auth_page()
        st.stop()
    
    return True

def get_current_user():
    """Get current logged in user info"""
    if st.session_state.get('logged_in', False):
        return st.session_state.get('user_info', None)
    return None
