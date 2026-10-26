@echo off
echo ========================================================
echo   FROM FARM TO FORK - Food Adulteration Awareness
echo   Backend Server Launcher (FastAPI + SQLite)
echo ========================================================
cd /d "%~dp0"

echo Starting FastAPI server on http://localhost:8000 ...

IF EXIST "C:\Users\hp\AppData\Local\Python\bin\python.exe" (
    "C:\Users\hp\AppData\Local\Python\bin\python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
) ELSE (
    where py >nul 2>&1
    IF ERRORLEVEL 1 (
        python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ) ELSE (
        py -3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    )
)

pause
