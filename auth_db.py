import sqlite3
import hashlib
import os
from datetime import datetime

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
                last_login TEXT
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
