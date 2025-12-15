# Actualizar Imágenes de Negocios en Railway

## Opción 1: Desde Railway Dashboard (Recomendado)

1. Ve a https://railway.app/dashboard
2. Selecciona tu proyecto "SantiaGo_backend"
3. Ve a la pestaña **"Deployments"**
4. En el deployment activo, haz clic en **"..."** → **"View Logs"**
5. Abre la pestaña **"Shell"** o **"Terminal"**
6. Ejecuta:

```bash
# Primero hacer dry-run para ver qué se actualizará
python manage.py update_business_images --dry-run

# Si todo se ve bien, ejecutar sin dry-run
python manage.py update_business_images
```

## Opción 2: Desde Railway CLI

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Conectar al proyecto
railway link

# Ejecutar comando
railway run python manage.py update_business_images
```

## Opción 3: Ejecutar localmente contra Railway DB

Si tienes las credenciales de la base de datos de Railway:

```bash
# En tu .env local, usar DATABASE_URL de Railway
python manage.py update_business_images
```

## Verificar Resultados

Después de ejecutar el comando, verifica en el frontend:
https://rutago-nine.vercel.app

Las imágenes deberían actualizarse automáticamente.

## Negocios que se actualizarán con imágenes específicas:

1. **Café Literario** 📚
   - Imagen: Café acogedor con libros en el fondo
   - Atmósfera: Literaria y cultural

2. **Librería Catalonia** 📖
   - Imagen: Estanterías llenas de libros coloridos
   - Atmósfera: Librería clásica y acogedora

3. **Patio Bellavista** 🍽️
   - Imagen: Restaurante con terraza y mesas al aire libre
   - Atmósfera: Casual y social

4. **Galería Artespacio** 🎨
   - Imagen: Galería de arte contemporáneo con obras exhibidas
   - Atmósfera: Artística y moderna

5. **Bar The Clinic** 🍺
   - Imagen: Bar moderno con iluminación cálida y ambiente nocturno
   - Atmósfera: Urbana y vibrante

Todas las imágenes son:
- **Específicas** para cada tipo de negocio
- **Alta calidad**: 1200px ancho, calidad 85
- **Profesionales**: Fotos de Unsplash con licencia libre
