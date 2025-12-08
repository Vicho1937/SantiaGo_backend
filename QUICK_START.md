# 🚀 Quick Start - Ejecutar Backend Localmente

**Tiempo estimado:** 10-15 minutos

---

## ✅ Requisitos Previos

- Python 3.10+ instalado
- PostgreSQL 15+ instalado y corriendo
- Git

---

## 📋 Pasos Rápidos

### 1. Verificar Python (2 min)

```bash
# Verificar versión
python --version
# o
python3 --version

# Debe ser 3.10 o superior
```

---

### 2. Clonar y Navegar (1 min)

```bash
# Si aún no lo has clonado
git clone <url-del-repo>
cd SantiaGo_backend
```

---

### 3. Crear Entorno Virtual (2 min)

```bash
# Crear entorno virtual
python -m venv venv

# Activar en Windows
venv\Scripts\activate

# Activar en Linux/Mac
source venv/bin/activate

# Deberías ver (venv) en tu terminal
```

---

### 4. Instalar Dependencias (3 min)

```bash
cd backend

# Instalar dependencias de desarrollo
pip install -r requirements/development.txt

# Esperar a que termine...
```

---

### 5. Crear Base de Datos PostgreSQL (2 min)

```bash
# Opción A: Con psql
psql -U postgres
CREATE DATABASE rutalocal_dev;
\q

# Opción B: Con pgAdmin
# Crear nueva base de datos llamada "rutalocal_dev"

# Opción C: Usar SQLite (más fácil para desarrollo)
# Ver sección "Alternativa: SQLite" abajo
```

---

### 6. Configurar Variables de Entorno (2 min)

```bash
# En la carpeta backend/
# Copiar el ejemplo
cp .env.example .env

# O crear manualmente
# Windows: crear archivo .env en backend/
# Linux/Mac: touch .env
```

**Editar `backend/.env` con estos valores mínimos:**

```bash
# Django
DEBUG=True
SECRET_KEY=django-insecure-local-dev-key-12345
ALLOWED_HOSTS=localhost,127.0.0.1

# Database - PostgreSQL
DB_NAME=rutalocal_dev
DB_USER=postgres
DB_PASSWORD=tu-password-postgres
DB_HOST=localhost
DB_PORT=5432

# Database - SQLite (alternativa - comentar si usas PostgreSQL)
# DATABASE_URL=sqlite:///db.sqlite3

# JWT
JWT_SECRET_KEY=local-dev-jwt-secret-12345
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=10080

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Mapbox
MAPBOX_ACCESS_TOKEN=pk.eyJ1IjoibmFjaG8yNTQiLCJhIjoiY21pdGxyZjhnMHRlYjNnb243bnA1OG81ayJ9.BPTKLir4w184eLNzsao9XQ
```

---

### 7. Ejecutar Migraciones (2 min)

```bash
# Crear las tablas en la base de datos
python manage.py migrate
```

**Deberías ver:**
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
  Applying reviews.0001_initial... OK
```

---

### 8. Cargar Datos Iniciales (1 min)

```bash
# Cargar categorías
python manage.py loaddata fixtures/01_categories.json

# Cargar features
python manage.py loaddata fixtures/02_features.json
```

**Deberías ver:**
```
Installed 12 object(s) from 1 fixture(s)
Installed 10 object(s) from 1 fixture(s)
```

---

### 9. Crear Superusuario (1 min)

```bash
python manage.py createsuperuser

# Te pedirá:
Email: admin@test.com
Username: admin
Password: admin123  (o el que quieras)
Password (again): admin123
```

---

### 10. Ejecutar Servidor (30 seg)

```bash
python manage.py runserver
```

**Deberías ver:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

## ✅ Verificar que Funciona

### 1. Admin Panel

Abre en navegador: http://localhost:8000/admin

- Email: admin@test.com
- Password: admin123

Deberías ver el panel de Django admin.

---

### 2. API Endpoints

**Categorías:**
```bash
http://localhost:8000/api/businesses/categories/
```

Deberías ver JSON con las 12 categorías.

---

### 3. Swagger/API Docs (si está configurado)

```bash
http://localhost:8000/api/schema/swagger-ui/
```

---

## 🎯 Script Automatizado

**O usa el script que creé:**

```bash
# Desde la raíz del proyecto
QUICK_SETUP.bat

# Hace todo automáticamente:
# - Activa venv
# - Corre migraciones
# - Carga fixtures
```

---

## 🐛 Troubleshooting

### Error: "No module named 'environ'"

**Solución:**
```bash
pip install -r requirements/development.txt
```

---

### Error: "django.db.utils.OperationalError: FATAL: password authentication failed"

**Solución:**
Verifica en `.env`:
```bash
DB_PASSWORD=tu-password-correcto-de-postgres
```

---

### Error: "relation does not exist"

**Solución:**
```bash
python manage.py migrate
```

---

### Error: Puerto 8000 ya en uso

**Solución:**
```bash
# Usar otro puerto
python manage.py runserver 8001

# O matar el proceso que usa el 8000
# Windows: netstat -ano | findstr :8000
# Linux/Mac: lsof -ti:8000 | xargs kill
```

---

## 📦 Alternativa: SQLite (Más Fácil)

Si no quieres instalar PostgreSQL para desarrollo local:

**1. En `backend/.env`:**
```bash
# Comentar PostgreSQL
# DB_NAME=...
# DB_USER=...

# Agregar SQLite
DATABASE_URL=sqlite:///db.sqlite3
```

**2. Correr migraciones:**
```bash
python manage.py migrate
```

**3. Todo lo demás igual**

SQLite crea un archivo `db.sqlite3` en la carpeta backend.

---

## 🔄 Workflow de Desarrollo

### Cada vez que trabajas:

```bash
# 1. Activar entorno virtual
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 2. Ejecutar servidor
python manage.py runserver

# 3. Trabajar...

# 4. Cuando termines
# CTRL + C para detener servidor
deactivate  # Desactivar venv
```

---

### Si actualizas modelos:

```bash
# 1. Crear migraciones
python manage.py makemigrations

# 2. Aplicar migraciones
python manage.py migrate
```

---

### Si instalas nuevas dependencias:

```bash
pip install nombre-paquete
pip freeze > requirements/development.txt
```

---

## 🧪 Probar con Frontend Local

### 1. Backend corriendo en 8000

```bash
python manage.py runserver
# http://localhost:8000
```

---

### 2. Frontend corriendo en 3000

En otra terminal, en el proyecto del frontend:

```bash
npm run dev
# http://localhost:3000
```

---

### 3. Verificar CORS

En `backend/.env`:
```bash
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

---

### 4. Frontend apuntando al backend

En frontend `.env.local`:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_BASE_PATH=/api
NEXT_PUBLIC_DEV_MODE=false
```

---

## 📝 Comandos Útiles

```bash
# Ver rutas disponibles
python manage.py show_urls  # Si tienes django-extensions

# Shell interactivo
python manage.py shell

# Crear app nueva
python manage.py startapp nombre_app apps/nombre_app

# Limpiar base de datos
python manage.py flush

# Cargar fixtures
python manage.py loaddata fixtures/archivo.json

# Crear fixtures desde DB
python manage.py dumpdata app.Model --indent 2 > fixtures/archivo.json

# Ver migraciones
python manage.py showmigrations

# Rollback migración
python manage.py migrate app_name numero_migracion
```

---

## ✅ Checklist Completo

- [ ] Python 3.10+ instalado
- [ ] PostgreSQL corriendo (o usar SQLite)
- [ ] Entorno virtual creado
- [ ] Dependencias instaladas
- [ ] .env configurado
- [ ] Migraciones aplicadas
- [ ] Fixtures cargadas
- [ ] Superusuario creado
- [ ] Servidor corriendo
- [ ] Admin panel accesible
- [ ] API endpoints responden
- [ ] (Opcional) Frontend conectado

---

## 🎉 ¡Listo!

Tu backend está corriendo localmente en: http://localhost:8000

**Endpoints disponibles:**
- Admin: http://localhost:8000/admin
- API Root: http://localhost:8000/api/
- Categorías: http://localhost:8000/api/businesses/categories/
- Businesses: http://localhost:8000/api/businesses/

---

## 🔄 Próximos Pasos

1. ✅ Backend local funcionando
2. 🔧 Hacer cambios y probar localmente
3. 🚀 Cuando esté listo, hacer deploy a Railway/Render
4. 🌐 Conectar con frontend en producción

---

**¿Tienes algún error? Consulta la sección Troubleshooting o pregunta.** 😊
