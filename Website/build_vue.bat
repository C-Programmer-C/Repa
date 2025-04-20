@echo off
echo Building Vue.js application for Django integration...

REM Проверяем наличие Node.js 
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo Node.js не найден в системе. Проверьте:
    echo 1. Установлен ли Node.js на вашем компьютере
    echo 2. Добавлен ли путь к Node.js в переменную PATH
    echo.
    echo Вы можете установить Node.js с https://nodejs.org/
    echo или указать полный путь к npm в этом скрипте.
    echo.
    pause
    exit /b 1
)

REM Ensure vue_dist directory exists in Django project
mkdir djanoproject\vue_dist 2>nul

REM Navigate to Vue.js project directory
cd Vue

REM Проверяем наличие пакета axios
echo Проверка наличия зависимости axios...
call npm list axios >nul 2>nul
if %errorlevel% neq 0 (
    echo Установка пакета axios...
    call npm install axios --save
)

REM Install dependencies
call npm install

REM Build the Vue.js application for Django
call npm run build:django

echo.
echo Vue.js build completed and moved to Django project.
echo Now you can run the Django server with 'python djanoproject/manage.py runserver'
echo. 