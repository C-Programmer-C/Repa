@echo off
echo Скрипт установки Node.js
echo ========================
echo.

REM Проверяем наличие Node.js
where node >nul 2>nul
if %errorlevel% equ 0 (
    echo Node.js уже установлен.
    node -v
    echo.
    echo Путь к Node.js:
    where node
    echo.
    choice /c YN /m "Желаете продолжить установку?"
    if %errorlevel% equ 2 exit /b 0
)

echo Загрузка установщика Node.js...
echo.

REM Используем PowerShell для загрузки файла
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://nodejs.org/dist/v18.17.1/node-v18.17.1-x64.msi' -OutFile 'node_setup.msi'}"

if not exist "node_setup.msi" (
    echo Не удалось загрузить установщик. Проверьте подключение к интернету.
    pause
    exit /b 1
)

echo Запуск установки...
echo.
echo ВНИМАНИЕ: Обязательно выберите опцию добавления Node.js в PATH!
echo.
start /wait msiexec /i node_setup.msi /passive /norestart

echo.
echo Установка завершена. Проверка Node.js...
echo.

REM Перезагружаем PATH из системного реестра
call RefreshEnv.cmd 2>nul || echo Требуется перезапуск командной строки для обновления PATH

where node >nul 2>nul
if %errorlevel% equ 0 (
    echo Node.js успешно установлен:
    node -v
    echo.
    echo Путь к Node.js:
    where node
    
    echo.
    echo Установка пакета axios...
    cd Vue
    call npm install axios --save
    cd ..
) else (
    echo Node.js установлен, но не найден в текущей сессии командной строки.
    echo Пожалуйста, закройте и откройте командную строку заново, или перезагрузите компьютер.
)

echo.
echo Удаление установщика...
del node_setup.msi

echo.
echo Готово! Теперь вы можете запустить build_vue.bat
pause 