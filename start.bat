@echo off
echo ========================================
echo   TicketHubLive - Starting Server
echo ========================================
echo.
echo Installing dependencies...
pip install -r requirements.txt -q
echo.
echo Starting Flask server...
echo.
echo  Website : http://localhost:5000
echo  API     : http://localhost:5000/api/events
echo  Admin   : http://localhost:5000/admin-login.html
echo.
echo Admin credentials: admin@tickethublive.com / Admin@1234
echo.
start "" http://localhost:5000
python app.py
pause
