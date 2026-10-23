@echo off
title Push Samagam 3D Model to GitHub
cd /d "c:\Users\anjuk\Desktop\president git"
echo =======================================================
echo   Samagam 3D Model - GitHub Push Tool
echo =======================================================
echo.
echo Pushing committed files to https://github.com/kapilk14031-svg/3D-model-samagam.git ...
echo.
"C:\Users\anjuk\Desktop\mingit\cmd\git.exe" push origin main
echo.
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Sabhi files, deployment data aur updates GitHub par push ho chuke hain!
) else (
    echo [ERROR] Push fail ho gaya. Kripya upar ka error dekhein.
)
echo.
echo Press any key to exit...
pause >nul
