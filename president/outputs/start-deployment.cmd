@echo off
title Gyan Mansarovar 3D Viewer & Security Deployment
cd /d "%~dp0"

echo ========================================================
echo  Starting Gyan Mansarovar 3D Viewer & Security Server...
echo ========================================================

:: Check if Python is installed and has sqlite3
where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    if exist "serve-deployment.py" (
        echo [INFO] Python detected. Checking environment...
        python -c "import sqlite3" >nul 2>nul
        if %ERRORLEVEL% equ 0 (
            echo [INFO] Starting Python backend server...
            start "" http://localhost:8794/gyan-mansarovar-3d.html
            python serve-deployment.py --port 8794
            goto :end
        )
    )
)

:: Universal Windows fallback using PowerShell server
echo [INFO] Starting universal high-performance web server...
start "" http://localhost:8080/gyan-mansarovar-3d.html
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0server.ps1"

:end
pause
