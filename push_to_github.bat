@echo off
echo ========================================
echo   AI Study Planner - GitHub Setup
echo ========================================
echo.

cd "c:\Users\Nikhil\OneDrive\Documents\AI LAB\ai-study-planner-streamlit"

echo Step 1: Checking git status...
git status
echo.

echo Step 2: Adding remote repository...
echo Please create a new repository on GitHub first:
echo   1. Go to: https://github.com/new
echo   2. Repository name: ai-study-planner-streamlit
echo   3. Make it Public or Private (your choice)
echo   4. DO NOT initialize with README
echo   5. Click "Create repository"
echo.

set /p ready="Have you created the repository? (y/n): "
if /i "%ready%" neq "y" (
    echo Please create the repository first, then run this script again.
    pause
    exit /b
)

echo.
echo Step 3: Adding GitHub remote...
git remote add origin https://github.com/Nikhil1081/ai-study-planner-streamlit.git

echo.
echo Step 4: Renaming branch to main...
git branch -M main

echo.
echo Step 5: Pushing to GitHub...
git push -u origin main

echo.
echo ========================================
echo   Push Complete!
echo ========================================
echo.
echo Your code is now on GitHub at:
echo https://github.com/Nikhil1081/ai-study-planner-streamlit
echo.
echo Next steps:
echo 1. Visit your repository on GitHub
echo 2. Deploy to Streamlit Cloud (see DEPLOYMENT_GUIDE.md)
echo.
pause
