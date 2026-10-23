@echo off
title Gyan Mansarovar 3D Viewer & Security Deployment
cd /d "%~dp0"

echo ========================================================
echo  Starting Gyan Mansarovar 3D Viewer & Security Server...
echo ========================================================

start "" http://localhost:8080/gyan-mansarovar-3d.html
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0server.ps1"

pause
