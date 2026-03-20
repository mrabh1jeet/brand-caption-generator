@echo off
echo Setting up Brand Caption Generation System...
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Python 3 is not installed. Please install Python 3.8+
    pause
    exit /b 1
)

REM Check Node
node --version >nul 2>&1
if errorlevel 1 (
    echo Node.js is not installed. Please install Node.js 16+
    pause
    exit /b 1
)

echo Python and Node.js found
echo.

REM Setup Backend
echo Setting up Backend...
cd backend

REM Create virtual environment
python -m venv venv
call venv\Scripts\activate.bat

REM Install dependencies
pip install -r requirements.txt

REM Create .env if it doesn't exist
if not exist .env (
    copy .env.example .env
    echo Please edit backend\.env and add your OPENAI_API_KEY
)

cd ..

echo Backend setup complete
echo.

REM Setup Frontend
echo Setting up Frontend...
cd frontend

call npm install

cd ..

echo Frontend setup complete
echo.

echo Setup complete!
echo.
echo To run the application:
echo.
echo Terminal 1 (Backend):
echo   cd backend
echo   venv\Scripts\activate
echo   python app.py
echo.
echo Terminal 2 (Frontend):
echo   cd frontend
echo   npm start
echo.
echo Don't forget to add your OPENAI_API_KEY to backend\.env
pause
