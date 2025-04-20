@echo off
echo Building Vue.js application using npx (no permanent Node.js installation required)...
echo.

REM Ensure vue_dist directory exists in Django project
mkdir djanoproject\vue_dist 2>nul

REM Navigate to Vue.js project directory
cd Vue

echo Downloading and using temporary Node.js via npx...

REM Install dependencies and build using npx
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://github.com/oven-sh/bun/releases/download/bun-v1.0.4/bun-windows-x64.zip' -OutFile 'bun.zip'; Expand-Archive -Path 'bun.zip' -DestinationPath '.bun' -Force; $env:Path += ';' + (Resolve-Path '.bun').Path; .\\.bun\\bun.exe add axios; .\\.bun\\bun.exe install; .\\.bun\\bun.exe run build:django; Remove-Item -Path 'bun.zip' -Force; Remove-Item -Path '.bun' -Recurse -Force}"

if %errorlevel% neq 0 (
    echo.
    echo Произошла ошибка при попытке сборки с помощью bun.
    echo Попробуем альтернативный метод с npx...
    echo.
    powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; npx.cmd --yes npm@latest install axios --save; npx.cmd --yes npm@latest install; npx.cmd --yes vite@latest build --outDir ../djanoproject/vue_dist/ --emptyOutDir}"
)

echo.
if %errorlevel% equ 0 (
    echo Vue.js build completed and moved to Django project.
    echo Now you can run the Django server with 'python djanoproject/manage.py runserver'
) else (
    echo Сборка не удалась. Рекомендуется установить Node.js с помощью install_nodejs.bat
)
echo. 