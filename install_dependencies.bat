@echo off
setlocal
cd /d "%~dp0"

echo.
echo Installing dependencies for Gurks Advanced AI Trading Bot
echo Folder: %CD%
echo.

where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    set PYTHON_CMD=python
) else (
    where py >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        set PYTHON_CMD=py -3
    ) else (
        echo Python was not found. Install Python 3.11+ first.
        pause
        exit /b 1
    )
)

if not exist "venv" (
    echo Creating virtual environment...
    %PYTHON_CMD% -m venv venv
)

call "venv\Scripts\activate.bat"
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Done. Start with:
echo   venv\Scripts\activate
echo   streamlit run bot.py --server.address 0.0.0.0 --server.port 8501
echo.
pause

