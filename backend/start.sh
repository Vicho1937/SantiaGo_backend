#!/bin/bash
cd /app/backend
echo "📦 Recolectando archivos estáticos..."
python3 manage.py collectstatic --noinput
echo "🗄️  Aplicando migraciones..."
python3 manage.py migrate
echo "👤 Creando superusuario..."
python3 create_superuser.py
echo "🖼️  Actualizando imágenes de negocios..."
python3 manage.py update_business_images
echo "🚀 Iniciando servidor..."
exec python3 -m gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2
