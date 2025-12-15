# 🚀 Guía Rápida: Actualizar Imágenes en Railway

## Método 1: Comando Django (Recomendado)

1. Abre Railway Dashboard
2. Ve a tu proyecto backend
3. Abre el **Terminal** del deployment
4. Ejecuta:
```bash
python manage.py update_business_images
```

## Método 2: SQL Directo (Más Rápido)

1. Abre Railway Dashboard
2. Ve a la pestaña **Database**
3. Haz clic en **Query**
4. Copia y pega el contenido de `UPDATE_IMAGES.sql`
5. Haz clic en **Run Query**

## ¿Cuál usar?

- **Comando Django**: Más seguro, con validaciones
- **SQL Directo**: Más rápido, cambios inmediatos

## Verificar Resultados

1. Espera 5 segundos
2. Recarga https://rutago-nine.vercel.app
3. Verás cada negocio con su imagen específica:
   - ☕ Café Literario → Café con libros
   - 📖 Librería → Estanterías
   - 🍽️ Restaurante → Terraza
   - 🎨 Galería → Arte
   - 🍺 Bar → Ambiente nocturno
