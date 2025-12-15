# Geocodificar Negocios Existentes

## 🎯 Propósito

Este comando geocodifica todos los negocios existentes que tienen coordenadas incorrectas o por defecto, para que aparezcan correctamente en el mapa interactivo.

---

## 📍 Tu Negocio de Renca

**Dirección:** Bravo de Saravia 2980, Renca
**Coordenadas Correctas:**
- Latitud: `-33.406065`
- Longitud: `-70.682074`

✅ **Esta dirección SÍ está dentro del área de Santiago**
✅ **Aparecerá en el mapa después de ejecutar este comando**

---

## 🚀 Cómo Ejecutar

### Opción 1: En Railway (Recomendado)

1. **Ir a Railway Dashboard:**
   - https://railway.app
   - Selecciona tu proyecto `SantiaGo_backend`

2. **Abrir la consola:**
   - Click en tu servicio
   - Tab "Settings"
   - Scroll hasta "Service Settings"
   - Click "Open Railway CLI" o usa el botón de terminal

3. **Ejecutar comando de prueba (DRY RUN):**
   ```bash
   python manage.py geocode_existing_businesses --dry-run
   ```

   Esto te mostrará qué negocios se geocodificarían **sin hacer cambios reales**.

4. **Si todo se ve bien, ejecutar el comando real:**
   ```bash
   python manage.py geocode_existing_businesses
   ```

### Opción 2: En Local (si tienes el proyecto en local)

```bash
cd /home/ignvvcio254/SantiaGo_backend/backend
python manage.py geocode_existing_businesses --dry-run
python manage.py geocode_existing_businesses
```

---

## 📋 Opciones del Comando

### `--dry-run`
Muestra qué se haría sin hacer cambios reales. **Siempre ejecuta esto primero.**

```bash
python manage.py geocode_existing_businesses --dry-run
```

**Salida esperada:**
```
======================================================================
🗺️  GEOCODIFICACIÓN DE NEGOCIOS EXISTENTES
======================================================================

⚠️  Modo DRY RUN - No se harán cambios reales

📊 Negocios que necesitan geocodificación: 5
📊 Negocios totales: 10

[1/5] Tu Negocio en Renca
  📍 Dirección: Bravo de Saravia 2980, Renca
  ℹ️  Razón: Coordenadas por defecto (centro de Santiago)
  🔍 Geocodificando: Bravo De Saravia 2980, Renca, Santiago, Chile
  ✓ Encontrado: Bravo De Saravia 2980, Renca, Santiago Metropolitan Region, Chile
  📌 Coordenadas: -33.406065, -70.682074
  🔄 No guardado (dry-run)

...

======================================================================
📊 RESUMEN DE GEOCODIFICACIÓN
======================================================================
Total procesados:  5
✅ Exitosos:       5
❌ Fallidos:       0
⏭️  Omitidos:       0

⚠️  DRY RUN - No se hicieron cambios reales
   Ejecuta sin --dry-run para aplicar los cambios
======================================================================
```

### `--force-all`
Geocodifica TODOS los negocios, incluso los que ya tienen coordenadas.

```bash
python manage.py geocode_existing_businesses --force-all
```

Útil si quieres asegurarte de que todos los negocios tengan las coordenadas más precisas.

### `--batch-size N`
Procesa N negocios a la vez (default: 10).

```bash
python manage.py geocode_existing_businesses --batch-size 20
```

### `--delay SECONDS`
Delay en segundos entre geocodificaciones para no saturar la API (default: 0.2).

```bash
python manage.py geocode_existing_businesses --delay 0.5
```

---

## 🔍 ¿Qué Negocios se Geocodifican?

El comando identifica automáticamente negocios que necesitan actualización:

### 1. Sin Coordenadas
```python
latitude = None
longitude = None
```

### 2. Coordenadas por Defecto (Centro de Santiago)
```python
latitude ≈ -33.4372  # Plaza de Armas
longitude ≈ -70.6506
```

Si un negocio tiene estas coordenadas (±0.01 grados), probablemente sean defaults y necesita geocodificación.

### 3. Force-All
Con `--force-all`, geocodifica todos los negocios activos.

---

## 📊 Ejemplo de Ejecución Completa

```bash
$ python manage.py geocode_existing_businesses

======================================================================
🗺️  GEOCODIFICACIÓN DE NEGOCIOS EXISTENTES
======================================================================

📊 Negocios que necesitan geocodificación: 3
📊 Negocios totales: 8

[1/3] Café Central
  📍 Dirección: Lastarria 305, Santiago Centro
  ℹ️  Razón: Coordenadas por defecto (centro de Santiago)
  🔍 Geocodificando: Lastarria 305, Santiago Centro, Santiago, Chile
  ✓ Encontrado: Lastarria 305, Santiago Centro, Santiago, Chile
  📌 Coordenadas: -33.437198, -70.638956
  💾 Guardado en base de datos

[2/3] Negocio en Renca
  📍 Dirección: Bravo de Saravia 2980, Renca
  ℹ️  Razón: Coordenadas por defecto (centro de Santiago)
  🔍 Geocodificando: Bravo De Saravia 2980, Renca, Santiago, Chile
  ✓ Encontrado: Bravo De Saravia 2980, Renca, Chile
  📌 Coordenadas: -33.406065, -70.682074
  💾 Guardado en base de datos

[3/3] Restaurante Providencia
  📍 Dirección: Providencia 1208
  ℹ️  Razón: Sin coordenadas
  🔍 Geocodificando: Providencia 1208, Santiago, Chile
  ✓ Encontrado: Providencia 1208, Providencia, Santiago, Chile
  📌 Coordenadas: -33.431623, -70.611789
  💾 Guardado en base de datos

======================================================================
📊 RESUMEN DE GEOCODIFICACIÓN
======================================================================
Total procesados:  3
✅ Exitosos:       3
❌ Fallidos:       0
⏭️  Omitidos:       0

✅ Geocodificación completada

💡 Los negocios actualizados ahora deberían aparecer correctamente en el mapa
======================================================================
```

---

## ✅ Verificar que Funcionó

### 1. Verificar en Django Admin
```
https://santiagov1-production.up.railway.app/admin/businesses/business/
```

Busca tu negocio y verifica que las coordenadas se actualizaron:
- Latitude: `-33.406065`
- Longitude: `-70.682074`

### 2. Verificar en el Mapa
```
https://tuapp.vercel.app/
```

Tu negocio debería aparecer en Renca (noroeste de Santiago) en el mapa interactivo.

### 3. Verificar en la API
```bash
curl https://santiagov1-production.up.railway.app/api/businesses/ | grep -A 10 "Renca"
```

---

## ❌ Troubleshooting

### Error: "MAPBOX_ACCESS_TOKEN no configurado"

**Solución:** Agregar variable de entorno en Railway:
```
MAPBOX_ACCESS_TOKEN=pk.eyJ1IjoibmFjaG8yNTQiLCJhIjoiY21pdGxyZjhnMHRlYjNnb243bnA1OG81ayJ9.BPTKLir4w184eLNzsao9XQ
```

### Error: "No se pudo geocodificar la dirección"

**Causa:** Dirección no válida o no existe.

**Solución:**
1. Verificar que la dirección sea real
2. Verificar que incluya número de calle
3. Agregar manualmente en Django Admin si es necesario

### Negocio no aparece en el mapa después de geocodificar

**Verificar:**
1. Status del negocio sea `published`
2. Coordenadas estén en rango de Santiago
3. Campo `is_active=True`
4. Refrescar caché del frontend (Ctrl+Shift+R)

---

## 📈 Impacto Esperado

**Antes:**
- ❌ Negocios con coordenadas incorrectas
- ❌ Todos aparecen en el centro de Santiago
- ❌ Mapa confuso y poco útil

**Después:**
- ✅ Cada negocio en su ubicación real
- ✅ Mapa preciso y útil
- ✅ Usuarios encuentran negocios cerca de ellos
- ✅ Tu negocio en Renca visible para usuarios de esa zona

---

## 🔮 Mantenimiento Futuro

### Negocios Nuevos
Los nuevos negocios se geocodifican **automáticamente** al crearlos. No necesitas ejecutar este comando para ellos.

### Re-geocodificar Todo
Si en el futuro quieres actualizar todas las coordenadas:
```bash
python manage.py geocode_existing_businesses --force-all
```

### Verificar Negocios
Para ver qué negocios necesitarían geocodificación sin hacerlo:
```bash
python manage.py geocode_existing_businesses --dry-run
```

---

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs de Railway
2. Verifica que la variable MAPBOX_ACCESS_TOKEN esté configurada
3. Ejecuta con --dry-run primero para diagnóstico

---

**¡Listo!** Ejecuta el comando y tu negocio de Renca aparecerá en el mapa. 🗺️✨
