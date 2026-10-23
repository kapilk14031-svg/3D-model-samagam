@echo off
set "PATH=C:\Users\anjuk\Desktop\mingit\cmd;C:\Users\anjuk\Desktop\mingit\mingw64\bin;%PATH%"
title Push Samagam 3D Model to GitHub
cd /d "c:\Users\anjuk\Desktop\president git"
echo =======================================================
echo   Samagam 3D Model - GitHub Push Tool
echo =======================================================
echo.
echo Target Repository: https://github.com/kapilk14031-svg/3D-model-samagam.git
echo.
echo Pushing committed files to GitHub origin main...
echo.
git.exe push origin main
echo.
if %ERRORLEVEL% EQU 0 (
    echo =======================================================
    echo [SUCCESS] Sabhi files, deployment data aur updates GitHub par push ho chuke hain!
    echo =======================================================
) else (
    echo =======================================================
    echo [ERROR] Push fail ho gaya. Kripya upar ka error check karein.
    echo =======================================================
)
echo.
echo Window band karne ke liye koi bhi key dabayein...
pause >nul
