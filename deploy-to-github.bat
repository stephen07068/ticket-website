@echo off
echo ========================================
echo   TicketHubLive - GitHub Deployment
echo ========================================
echo.

REM Check if git is initialized
if not exist .git (
    echo Initializing Git repository...
    git init
    echo.
)

REM Add all files
echo Adding files to Git...
git add .
echo.

REM Commit
echo Enter commit message (or press Enter for default):
set /p COMMIT_MSG="Commit message: "
if "%COMMIT_MSG%"=="" set COMMIT_MSG=Update TicketHubLive platform

echo Committing changes...
git commit -m "%COMMIT_MSG%"
echo.

REM Check if remote exists
git remote -v | findstr origin >nul
if errorlevel 1 (
    echo.
    echo ========================================
    echo   GitHub Repository Setup Required
    echo ========================================
    echo.
    echo 1. Go to https://github.com/new
    echo 2. Create a new repository named: tickethublive
    echo 3. DO NOT initialize with README
    echo 4. Copy the repository URL
    echo.
    echo Enter your GitHub repository URL:
    echo Example: https://github.com/username/tickethublive.git
    set /p REPO_URL="Repository URL: "
    
    echo.
    echo Adding remote origin...
    git remote add origin !REPO_URL!
    echo.
)

REM Set main branch
echo Setting main branch...
git branch -M main
echo.

REM Push to GitHub
echo Pushing to GitHub...
git push -u origin main
echo.

if errorlevel 1 (
    echo.
    echo ========================================
    echo   Push Failed - Possible Solutions:
    echo ========================================
    echo.
    echo 1. Make sure you're logged into GitHub
    echo 2. Check your repository URL is correct
    echo 3. Try: git push -u origin main --force
    echo.
    pause
) else (
    echo.
    echo ========================================
    echo   SUCCESS! Deployed to GitHub!
    echo ========================================
    echo.
    echo Your code is now on GitHub!
    echo.
    echo Next steps:
    echo 1. View your repository on GitHub
    echo 2. Deploy to Render.com, Railway, or PythonAnywhere
    echo 3. See DEPLOYMENT.md for hosting instructions
    echo.
    pause
)
