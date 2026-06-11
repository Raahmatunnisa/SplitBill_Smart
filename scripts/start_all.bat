@echo off
echo ========================================
echo SplitBill Smart - Start All Services
echo ========================================

set ROOT=%~dp0..
cd /d "%ROOT%"

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat
pip install -r requirements.txt -q

echo.
echo Running migrations...
call scripts\migrate_all.bat

echo.
echo Starting services in separate windows...

start "User Service :8001" cmd /k "cd /d %ROOT%\services\user_service && %ROOT%\venv\Scripts\python.exe manage.py runserver 8001"
timeout /t 2 /nobreak > nul

start "Group Service :8002" cmd /k "cd /d %ROOT%\services\group_service && %ROOT%\venv\Scripts\python.exe manage.py runserver 8002"
timeout /t 1 /nobreak > nul

start "Bill Service :8003" cmd /k "cd /d %ROOT%\services\bill_service && %ROOT%\venv\Scripts\python.exe manage.py runserver 8003"
timeout /t 1 /nobreak > nul

start "Settlement Service :8004" cmd /k "cd /d %ROOT%\services\settlement_service && %ROOT%\venv\Scripts\python.exe manage.py runserver 8004"
timeout /t 1 /nobreak > nul

start "Receipt OCR Service :8005" cmd /k "cd /d %ROOT%\services\receipt_ocr_service && %ROOT%\venv\Scripts\python.exe manage.py runserver 8005"
timeout /t 1 /nobreak > nul

start "Notification Service :8006" cmd /k "cd /d %ROOT%\services\notification_service && %ROOT%\venv\Scripts\python.exe manage.py runserver 8006"
timeout /t 1 /nobreak > nul

start "API Gateway :8000" cmd /k "cd /d %ROOT%\services\api_gateway && %ROOT%\venv\Scripts\python.exe manage.py runserver 8000"
timeout /t 2 /nobreak > nul

echo.
echo Starting frontend...
start "Frontend :5173" cmd /k "cd /d %ROOT%\frontend && npm install && npm run dev"

echo.
echo All services started!
echo API Gateway: http://localhost:8000
echo Frontend:    http://localhost:5173
echo.
echo Run seed data: python scripts\seed_data.py
pause
