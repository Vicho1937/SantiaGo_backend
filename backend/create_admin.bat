@echo off
echo ===============================================
echo    Creando Superusuario para Ruta Local
echo ===============================================
echo.

cd /d "C:\Users\Vicente\Documents\GitHub\SantiaGo_backend\backend"
call venv\Scripts\activate.bat

echo Ejecutando script de creacion...
python create_superuser.py

echo.
echo ===============================================
echo    Proceso completado
echo ===============================================
echo.
pause
