#!/bin/bash
echo "Building Vue.js application for Django integration..."

# Проверяем наличие Node.js
if ! command -v node &> /dev/null; then
    echo "Node.js не найден в системе. Проверьте:"
    echo "1. Установлен ли Node.js на вашем компьютере"
    echo "2. Добавлен ли путь к Node.js в переменную PATH"
    echo ""
    echo "Вы можете установить Node.js с https://nodejs.org/"
    echo "или указать полный путь к npm в этом скрипте."
    echo ""
    exit 1
fi

# Ensure vue_dist directory exists in Django project
mkdir -p djanoproject/vue_dist

# Navigate to Vue.js project directory
cd Vue

# Проверяем наличие пакета axios
echo "Проверка наличия зависимости axios..."
if ! npm list axios &> /dev/null; then
    echo "Установка пакета axios..."
    npm install axios --save
fi

# Install dependencies
npm install

# Build the Vue.js application for Django
npm run build:django

echo ""
echo "Vue.js build completed and moved to Django project."
echo "Now you can run the Django server with 'python djanoproject/manage.py runserver'"
echo "" 