@echo off
title WhatsApp Business Bot Server
cd /d "D:\whatsapp-business-bot"

echo ========================================================
echo        WhatsApp Business Bot is Starting...
echo ========================================================
echo.
echo Opening WhatsApp Simulator and Admin Panel in Browser...
echo.

:: Automatically open browser after 2 seconds
start "" powershell -Command "Start-Sleep -Seconds 2; Start-Process 'http://127.0.0.1:8000/simulator'; Start-Process 'http://127.0.0.1:8000/admin'"

:: Start the Python server
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload

pause
