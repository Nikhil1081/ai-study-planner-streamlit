# 🔐 Authentication System - User Guide

## ✅ What's New

Your AI Study Planner now has a complete authentication system!

### Features Added:
- ✅ **User Registration** - Create account with username, email, and password
- ✅ **Secure Login** - Password hashing with SHA256
- ✅ **Session Management** - Stay logged in during your session
- ✅ **User Profile** - View your info in sidebar
- ✅ **Protected Pages** - All pages require authentication
- ✅ **SQLite Database** - Local user data storage
- ✅ **Logout Functionality** - Secure logout from any page

## 🚀 How to Use

### First Time User - Registration

1. **Open the App** at http://localhost:8502 (or your deployed URL)

2. **Click "Create Account"** button

3. **Fill in the registration form:**
   - **Username:** 3-20 characters (letters, numbers, underscore)
   - **Email:** Valid email address
   - **Password:** Minimum 6 characters
   - **Confirm Password:** Must match password

4. **Click "Register"** - You'll see success message

5. **You'll be redirected to login page**

### Returning User - Login

1. **Enter your credentials:**
   - Username
   - Password

2. **Click "Login"** button

3. **Access granted!** You'll see:
   - Home page with all features
   - Your username in sidebar
   - Logout button

### Navigation

Once logged in:
- 🏠 **Home** - Main dashboard
- 📅 **Study Planner** - Generate AI study plans
- 💬 **Chat** - AI assistant for study help
- 📊 **Dashboard** - Track your progress

### Logout

Click the **🚪 Logout** button in any page's sidebar to:
- End your session
- Clear all session data
- Return to login page

## 🔒 Security Features

### Password Protection
- Passwords are hashed using SHA256
- Never stored in plain text
- Secure comparison for login

### Session Management
- Uses Streamlit's secure session state
- Session data cleared on logout
- Automatic session timeout on browser close

### Database
- SQLite database stores user data
- Located at: `users.db`
- **Not committed to Git** (.gitignore protected)
- Unique username and email enforcement

## 📁 New Files

```
ai-study-planner-streamlit/
├── auth.py              # Authentication UI & logic
├── auth_db.py           # Database operations
└── users.db             # User database (auto-created)
```

## 🛠️ Technical Details

### User Database Schema

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL,
    last_login TEXT
)
```

### Authentication Flow

1. **Registration:**
   ```
   User Input → Validation → Password Hash → Database Insert → Success
   ```

2. **Login:**
   ```
   User Input → Hash Password → DB Query → Compare Hash → Session Create
   ```

3. **Page Access:**
   ```
   Page Load → Check Session → If Not Logged In → Redirect to Login
   ```

## 🐛 Troubleshooting

### "Username already exists"
- Choose a different username
- Each username must be unique

### "Email already registered"
- Use a different email
- One email per account

### "Invalid username or password"
- Check spelling and caps lock
- Passwords are case-sensitive
- Try registering if you're new

### Can't access pages
- Make sure you're logged in
- Check for session timeout
- Try logging out and back in

### Database locked error
- Close other instances of the app
- Wait a moment and try again

## 🔄 For Developers

### Import authentication in new pages:

```python
import sys
sys.path.append('..')
from auth import require_auth, get_current_user, logout

# Require authentication
require_auth()

# Get current user
current_user = get_current_user()
print(current_user['username'])
```

### User object structure:

```python
{
    'id': 1,
    'username': 'john_doe',
    'email': 'john@example.com',
    'created_at': '2026-02-19 10:30:00'
}
```

## 📊 Testing

### Test Account (for demo)

Create your own test account:
- Username: `test_user`
- Email: `test@example.com`
- Password: `test123`

## 🚀 Deployment Note

When deploying to Streamlit Cloud:
- Database will be created automatically
- Each deployment has its own user database
- Users need to register on the deployed instance

## ✨ Future Enhancements (Optional)

Ideas for improvement:
- [ ] Password reset functionality
- [ ] Email verification
- [ ] Google OAuth integration
- [ ] Remember me checkbox
- [ ] Password strength meter
- [ ] User profile editing
- [ ] Admin dashboard

## 📝 Notes

- **Database File:** `users.db` is in `.gitignore` - it won't be pushed to GitHub
- **Test Locally First:** Register and login locally before deploying
- **Production:** Consider using PostgreSQL for production deployment
- **Backup:** Regularly backup `users.db` if you have important user data

---

**Built with ❤️ | Secure Authentication | Happy Studying! 🎓**
