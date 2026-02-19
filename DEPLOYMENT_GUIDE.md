# 🚀 GitHub & Streamlit Deployment Guide

## Step 1: Create GitHub Repository

### Option A: Using GitHub Web Interface (Recommended)

1. **Go to GitHub:**
   - Visit https://github.com/Nikhil1081
   - Sign in if needed

2. **Create New Repository:**
   - Click the **"+"** icon in top right
   - Select **"New repository"**

3. **Repository Settings:**
   - **Name:** `ai-study-planner-streamlit`
   - **Description:** AI Study Planner chatbot with Gemini API - Built with Streamlit
   - **Visibility:** Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
   - Click **"Create repository"**

4. **Copy Repository URL:**
   - You'll see a URL like: `https://github.com/Nikhil1081/ai-study-planner-streamlit.git`

### Option B: Using GitHub CLI

```bash
gh repo create ai-study-planner-streamlit --public --source=. --remote=origin --push
```

## Step 2: Push Your Code to GitHub

Open PowerShell/Terminal and run:

```bash
cd "c:\Users\Nikhil\OneDrive\Documents\AI LAB\ai-study-planner-streamlit"

# Add GitHub as remote (replace with YOUR actual repo URL)
git remote add origin https://github.com/Nikhil1081/ai-study-planner-streamlit.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

**If you get authentication error:**
- GitHub requires Personal Access Token (PAT) instead of password
- Create one at: https://github.com/settings/tokens
- Use the token as password when prompted

## Step 3: Deploy to Streamlit Cloud

### A. Sign Up for Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Click **"Sign up"** or **"Sign in"**
3. Choose **"Continue with GitHub"**
4. Authorize Streamlit to access your repositories

### B. Deploy Your App

1. Click **"New app"** button
2. Fill in the details:
   - **Repository:** `Nikhil1081/ai-study-planner-streamlit`
   - **Branch:** `main`
   - **Main file path:** `Home.py`
   - **App URL:** Choose a custom URL (e.g., `nikhil-study-planner`)

3. **Add Secrets (IMPORTANT):**
   - Click **"Advanced settings"**
   - Find **"Secrets"** section
   - Add:
   ```toml
   GEMINI_API_KEY = "AIzaSyBO3qiLuaIDE4lN5tfOe78owEw6onp5ZmU"
   ```
   - Click **"Save"**

4. Click **"Deploy!"**

5. Wait 2-3 minutes for deployment
   - Your app will be live at: `https://your-app-name.streamlit.app`

## Step 4: Update API Key References (Optional)

For better security on Streamlit Cloud, update the code to use secrets:

### In Home.py:
Replace:
```python
GEMINI_API_KEY = "AIzaSyBO3qiLuaIDE4lN5tfOe78owEw6onp5ZmU"
```

With:
```python
import streamlit as st
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "AIzaSyBO3qiLuaIDE4lN5tfOe78owEw6onp5ZmU")
```

Do the same for all page files.

Then push changes:
```bash
git add .
git commit -m "Use Streamlit secrets for API key"
git push origin main
```

## Step 5: Test Your Deployed App

1. Visit your Streamlit Cloud URL
2. Test all features:
   - ✅ Home page loads
   - ✅ Study Planner generates plans
   - ✅ Chat Assistant responds
   - ✅ Dashboard tracks tasks

## 🛠️ Troubleshooting

### Issue: Git push authentication fails
**Solution:**
1. Create Personal Access Token: https://github.com/settings/tokens
2. Use token as password
3. Or use: `git remote set-url origin https://YOUR_TOKEN@github.com/Nikhil1081/ai-study-planner-streamlit.git`

### Issue: Streamlit app crashes on startup
**Solution:**
1. Check logs in Streamlit Cloud dashboard
2. Verify GEMINI_API_KEY is set in secrets
3. Check requirements.txt has all dependencies

### Issue: API calls fail
**Solution:**
1. Verify API key is correct in Streamlit secrets
2. Check API quota limits
3. Test API key locally first

### Issue: Pages don't load
**Solution:**
1. Ensure folder structure is correct: `pages/1_📅_Study_Planner.py`
2. Check file naming matches exactly
3. Clear browser cache

## 📱 Share Your App

Once deployed, share your app URL:
- Direct link: `https://your-app-name.streamlit.app`
- Add to GitHub README
- Share on social media

## 🔄 Update Your App

To push updates:
```bash
# Make changes to your code
git add .
git commit -m "Description of changes"
git push origin main
```

Streamlit Cloud will automatically redeploy!

## 📊 Monitor Usage

- View app logs in Streamlit Cloud dashboard
- Check analytics for usage stats
- Monitor API usage in Google Cloud Console

## 🎉 You're Done!

Your AI Study Planner is now live and accessible worldwide!

### Next Steps:
- [ ] Test all features
- [ ] Share with friends
- [ ] Collect feedback
- [ ] Add more features
- [ ] Star the repo ⭐

---

**Need Help?**
- Streamlit Docs: https://docs.streamlit.io/
- GitHub Docs: https://docs.github.com/
- Gemini API Docs: https://ai.google.dev/docs
