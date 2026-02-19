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
    """Display login page"""
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 2rem; border-radius: 10px; text-align: center; margin-bottom: 2rem;'>
        <h1>🎓 Welcome Back!</h1>
        <p>Sign in to access your AI Study Planner</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        st.subheader("🔐 Login")
        
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("🚀 Login", use_container_width=True)
        with col2:
            if st.form_submit_button("📝 Create Account", use_container_width=True):
                st.session_state.auth_page = 'register'
                st.rerun()
        
        if submit:
            if not username or not password:
                st.error("❌ Please fill in all fields!")
            else:
                db = AuthDB()
                success, result = db.login_user(username, password)
                
                if success:
                    st.session_state.logged_in = True
                    st.session_state.user_info = result
                    st.success(f"✅ Welcome back, {result['username']}!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(f"❌ {result}")
    
    # Demo credentials
    with st.expander("ℹ️ Demo Info"):
        st.info("First time here? Click 'Create Account' to register!")

def show_register_page():
    """Display registration page"""
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 2rem; border-radius: 10px; text-align: center; margin-bottom: 2rem;'>
        <h1>🎓 Join AI Study Planner!</h1>
        <p>Create your account and start learning smarter</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("register_form"):
        st.subheader("📝 Create Account")
        
        username = st.text_input("Username", placeholder="Choose a unique username (3-20 chars)")
        email = st.text_input("Email", placeholder="your.email@example.com")
        password = st.text_input("Password", type="password", placeholder="Minimum 6 characters")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
        
        st.markdown("**Password Requirements:**")
        st.caption("• Minimum 6 characters")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("✅ Register", use_container_width=True)
        with col2:
            if st.form_submit_button("🔙 Back to Login", use_container_width=True):
                st.session_state.auth_page = 'login'
                st.rerun()
        
        if submit:
            # Validation
            if not username or not email or not password or not confirm_password:
                st.error("❌ Please fill in all fields!")
            elif not validate_username(username):
                st.error("❌ Username must be 3-20 characters (letters, numbers, underscore only)")
            elif not validate_email(email):
                st.error("❌ Please enter a valid email address!")
            elif not validate_password(password):
                st.error("❌ Password must be at least 6 characters!")
            elif password != confirm_password:
                st.error("❌ Passwords don't match!")
            else:
                db = AuthDB()
                success, message = db.register_user(username, email, password)
                
                if success:
                    st.success("✅ Registration successful! Please login.")
                    st.balloons()
                    st.session_state.auth_page = 'login'
                    st.rerun()
                else:
                    st.error(f"❌ {message}")

def show_auth_page():
    """Main authentication page handler"""
    init_auth()
    
    if st.session_state.logged_in:
        return True  # User is authenticated
    
    # Show login or register based on state
    if st.session_state.auth_page == 'login':
        show_login_page()
    else:
        show_register_page()
    
    return False  # User needs to authenticate

def logout():
    """Logout current user"""
    st.session_state.logged_in = False
    st.session_state.user_info = None
    st.session_state.auth_page = 'login'
    # Clear other session state variables
    for key in list(st.session_state.keys()):
        if key not in ['logged_in', 'user_info', 'auth_page']:
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
