import sqlite3
import hashlib
import os
from datetime import datetime
import secrets

class AuthDB:
    """Database handler for user authentication"""
    
    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize the database with users table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL,
                last_login TEXT,
                reset_token TEXT,
                reset_token_expiry TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password):
        """Hash password using SHA256"""
        salt = "ai_study_planner_2026"  # In production, use unique salt per user
        return hashlib.sha256((password + salt).encode()).hexdigest()
    
    def register_user(self, username, email, password):
        """Register a new user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            password_hash = self.hash_password(password)
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, created_at)
                VALUES (?, ?, ?, ?)
            ''', (username, email, password_hash, created_at))
            
            conn.commit()
            conn.close()
            return True, "Registration successful!"
        
        except sqlite3.IntegrityError as e:
            if "username" in str(e):
                return False, "Username already exists!"
            elif "email" in str(e):
                return False, "Email already registered!"
            return False, "Registration failed!"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def login_user(self, username, password):
        """Verify user credentials"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            password_hash = self.hash_password(password)
            
            cursor.execute('''
                SELECT id, username, email, created_at
                FROM users
                WHERE username = ? AND password_hash = ?
            ''', (username, password_hash))
            
            user = cursor.fetchone()
            
            if user:
                # Update last login
                cursor.execute('''
                    UPDATE users
                    SET last_login = ?
                    WHERE username = ?
                ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), username))
                conn.commit()
                
                conn.close()
                return True, {
                    'id': user[0],
                    'username': user[1],
                    'email': user[2],
                    'created_at': user[3]
                }
            else:
                conn.close()
                return False, "Invalid username or password!"
        
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_user_info(self, username):
        """Get user information"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, username, email, created_at, last_login
                FROM users
                WHERE username = ?
            ''', (username,))
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return {
                    'id': user[0],
                    'username': user[1],
                    'email': user[2],
                    'created_at': user[3],
                    'last_login': user[4]
                }
            return None
        
        except Exception as e:
            return None
    
    def generate_reset_token(self, email):
        """Generate password reset token for email"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if email exists
            cursor.execute('SELECT id, username FROM users WHERE email = ?', (email,))
            user = cursor.fetchone()
            
            if not user:
                conn.close()
                return False, "Email not found!"
            
            # Generate reset token (6-digit code)
            reset_token = str(secrets.randbelow(900000) + 100000)
            
            # Token expires in 15 minutes
            from datetime import datetime, timedelta
            expiry = (datetime.now() + timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M:%S')
            
            # Store token
            cursor.execute('''
                UPDATE users
                SET reset_token = ?, reset_token_expiry = ?
                WHERE email = ?
            ''', (reset_token, expiry, email))
            
            conn.commit()
            conn.close()
            
            return True, {
                'username': user[1],
                'reset_token': reset_token,
                'expiry': expiry
            }
        
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def verify_reset_token(self, email, token):
        """Verify reset token"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT reset_token, reset_token_expiry
                FROM users
                WHERE email = ?
            ''', (email,))
            
            result = cursor.fetchone()
            conn.close()
            
            if not result or not result[0]:
                return False, "No reset token found!"
            
            stored_token, expiry = result
            
            # Check if token matches
            if stored_token != token:
                return False, "Invalid reset code!"
            
            # Check if token expired
            from datetime import datetime
            expiry_time = datetime.strptime(expiry, '%Y-%m-%d %H:%M:%S')
            if datetime.now() > expiry_time:
                return False, "Reset code expired! Please request a new one."
            
            return True, "Token verified!"
        
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def reset_password(self, email, new_password):
        """Reset password using verified email"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            password_hash = self.hash_password(new_password)
            
            cursor.execute('''
                UPDATE users
                SET password_hash = ?, reset_token = NULL, reset_token_expiry = NULL
                WHERE email = ?
            ''', (password_hash, email))
            
            conn.commit()
            conn.close()
            
            return True, "Password reset successful!"
        
        except Exception as e:
            return False, f"Error: {str(e)}"
