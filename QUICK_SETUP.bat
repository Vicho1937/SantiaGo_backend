@echo off
echo ========================================
echo   RUTA LOCAL - Backend Quick Setup
echo ========================================
echo.

cd backend

echo [1/5] Activando entorno virtual...
call venv\Scripts\activate.bat

echo.
echo [2/5] Creando migraciones...
python manage.py makemigrations

echo.
echo [3/5] Aplicando migraciones...
python manage.py migrate

echo.
echo [4/5] Cargando fixtures de categorias...
python manage.py loaddata fixtures\01_categories.json

echo.
echo [5/5] Cargando fixtures de features...
python manage.py loaddata fixtures\02_features.json

echo.
echo ========================================
echo   Setup completado exitosamente!
echo ========================================
echo.
echo Para iniciar el servidor:
echo   python manage.py runserver
echo.
echo Para crear superusuario:
echo   python manage.py createsuperuser
echo.
pause
