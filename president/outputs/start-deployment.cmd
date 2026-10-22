@echo off
cd /d "%~dp0"
python serve-deployment.py --port 8794
pause
