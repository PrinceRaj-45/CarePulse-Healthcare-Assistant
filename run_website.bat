@echo off
title CarePulse Healthcare Assistant
echo =======================================================
echo Starting CarePulse Healthcare Web Application...
echo Opening your browser at http://127.0.0.1:5000
echo =======================================================
timeout /t 2 >nul
start http://127.0.0.1:5000
python app.py
pause
