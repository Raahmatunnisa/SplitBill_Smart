@echo off
set ROOT=%~dp0..
cd /d "%ROOT%"
call venv\Scripts\activate.bat

echo Migrating User Service...
cd services\user_service
python manage.py makemigrations accounts
python manage.py migrate
cd ..\..

echo Migrating Group Service...
cd services\group_service
python manage.py makemigrations groups
python manage.py migrate
cd ..\..

echo Migrating Bill Service...
cd services\bill_service
python manage.py makemigrations bills
python manage.py migrate
cd ..\..

echo Migrating Settlement Service...
cd services\settlement_service
python manage.py makemigrations settlement
python manage.py migrate
cd ..\..

echo Migrating Receipt OCR Service...
cd services\receipt_ocr_service
python manage.py makemigrations ocr
python manage.py migrate
cd ..\..

echo Migrating Notification Service...
cd services\notification_service
python manage.py makemigrations notifications
python manage.py migrate
cd ..\..

echo Migrating API Gateway...
cd services\api_gateway
python manage.py migrate
cd ..\..

echo All migrations complete!
