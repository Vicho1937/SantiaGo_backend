# 🔐 Autenticación con Google usando Supabase

Este documento describe cómo funciona la autenticación con Google OAuth a través de Supabase en el proyecto RutaGo.

---

## 📋 Resumen

- **Frontend (Next.js)**: Usa Supabase Auth para autenticar usuarios con Google
- **Supabase**: Maneja el flujo OAuth con Google y emite tokens JWT
- **Backend (Django)**: Valida los tokens JWT de Supabase y sincroniza usuarios

---

## 🔧 Configuración Completada

### ✅ Google Cloud Console
- **Proyecto**: Tu proyecto de Google Cloud
- **Client ID**: `[TU_CLIENT_ID].apps.googleusercontent.com` (Ver en .env)
- **Client Secret**: `GOCSPX-[TU_SECRET]` (Ver en .env)
- **Callback URL**: `https://[tu-proyecto-id].supabase.co/auth/v1/callback`

### ✅ Supabase Dashboard
- **Project ID**: Tu proyecto de Supabase (Ver en .env)
- **Project URL**: `https://[tu-proyecto-id].supabase.co` (Ver en .env)
- **JWT Secret**: Configurado en variables de entorno
- **Google Provider**: Habilitado con las credenciales de Google Cloud

### ✅ Backend Django
- **Endpoint**: `POST /api/auth/google`
- **Validación**: JWT token de Supabase
- **Sincronización**: Crea/actualiza usuarios automáticamente

---

## 🔄 Flujo de Autenticación

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐         ┌──────────────┐
│             │         │              │         │             │         │              │
│   Usuario   │────────▶│   Frontend   │────────▶│  Supabase   │────────▶│    Google    │
│             │  Click  │  (Next.js)   │  OAuth  │    Auth     │  OAuth  │    OAuth     │
│             │         │              │         │             │         │              │
└─────────────┘         └──────────────┘         └─────────────┘         └──────────────┘
                               │                       │
                               │  access_token (JWT)   │
                               │◀──────────────────────│
                               │
                               │  POST /api/auth/google
                               │  { access_token }
                               ▼
                        ┌──────────────┐
                        │              │
                        │   Backend    │──▶ Valida JWT con SUPABASE_JWT_SECRET
                        │   (Django)   │──▶ Extrae datos del usuario
                        │              │──▶ Crea/actualiza User en Django
                        └──────────────┘──▶ Devuelve tokens JWT de Django
                               │
                               │  { user, tokens }
                               ▼
                        ┌──────────────┐
                        │   Frontend   │
                        │  (Guardado)  │
                        └──────────────┘
```

---

## 💻 Implementación en el Frontend

### 1. Instalación de Supabase Client

```bash
npm install @supabase/supabase-js
```

### 2. Configuración de Supabase

```typescript
// lib/supabase.ts
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseAnonKey)
```

### 3. Variables de Entorno (.env.local)

```bash
NEXT_PUBLIC_SUPABASE_URL=https://[tu-proyecto-id].supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
NEXT_PUBLIC_API_URL=https://tu-backend.railway.app/api
```

### 4. Implementación del Login con Google

```typescript
// components/GoogleLoginButton.tsx
import { supabase } from '@/lib/supabase'

export function GoogleLoginButton() {
  const handleGoogleLogin = async () => {
    try {
      // 1. Iniciar sesión con Google vía Supabase
      const { data, error } = await supabase.auth.signInWithOAuth({
        provider: 'google',
        options: {
          redirectTo: `${window.location.origin}/auth/callback`,
        },
      })

      if (error) throw error

      // Supabase redirigirá automáticamente a Google
    } catch (error) {
      console.error('Error al iniciar sesión con Google:', error)
    }
  }

  return (
    <button onClick={handleGoogleLogin}>
      Continuar con Google
    </button>
  )
}
```

### 5. Callback Handler

```typescript
// app/auth/callback/route.ts (App Router)
// o pages/auth/callback.tsx (Pages Router)

import { supabase } from '@/lib/supabase'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export default function AuthCallback() {
  const router = useRouter()

  useEffect(() => {
    const handleCallback = async () => {
      try {
        // 2. Obtener la sesión de Supabase después del redirect
        const { data: { session }, error } = await supabase.auth.getSession()

        if (error) throw error

        if (session?.access_token) {
          // 3. Enviar el token al backend Django
          const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/google`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              access_token: session.access_token,
              refresh_token: session.refresh_token,
            }),
          })

          const data = await response.json()

          if (data.success) {
            // 4. Guardar tokens de Django en localStorage/cookies
            localStorage.setItem('access_token', data.tokens.accessToken)
            localStorage.setItem('refresh_token', data.tokens.refreshToken)
            localStorage.setItem('user', JSON.stringify(data.user))

            // 5. Redirigir al dashboard
            router.push('/dashboard')
          } else {
            throw new Error(data.message)
          }
        }
      } catch (error) {
        console.error('Error en callback:', error)
        router.push('/login?error=auth_failed')
      }
    }

    handleCallback()
  }, [router])

  return <div>Procesando autenticación...</div>
}
```

---

## 🔌 API del Backend

### Endpoint: `POST /api/auth/google`

**Request:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." // Opcional
}
```

**Response (200 OK - Usuario existente):**
```json
{
  "success": true,
  "message": "Autenticación exitosa",
  "user": {
    "id": "uuid",
    "email": "usuario@gmail.com",
    "username": "usuario",
    "name": "Juan Pérez",
    "first_name": "Juan",
    "last_name": "Pérez",
    "avatar": "https://lh3.googleusercontent.com/...",
    "role": "user",
    "emailVerified": true,
    // ... más campos
  },
  "tokens": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "tokenType": "Bearer",
    "expiresIn": 3600
  },
  "isNewUser": false
}
```

**Response (201 Created - Usuario nuevo):**
```json
{
  "success": true,
  "message": "Usuario creado exitosamente",
  "user": { ... },
  "tokens": { ... },
  "isNewUser": true
}
```

**Response (401 Unauthorized - Token inválido):**
```json
{
  "success": false,
  "message": "Token de Supabase inválido o expirado"
}
```

---

## 🔒 Seguridad

### Backend
- ✅ Valida tokens JWT de Supabase con `SUPABASE_JWT_SECRET`
- ✅ Verifica firma, expiración y audiencia del token
- ✅ Usa transacciones atómicas para crear/actualizar usuarios
- ✅ No expone credenciales sensibles en respuestas

### Frontend
- ✅ Usa HTTPS en producción
- ✅ Tokens almacenados de forma segura
- ✅ Redirect URI validado en Google Cloud Console
- ✅ CORS configurado correctamente

---

## 🧪 Testing

### 1. Agregar Usuarios de Prueba en Google Cloud Console

Como la app está en modo de prueba, solo usuarios específicos pueden autenticarse:

1. Ve a [Google Cloud Console](https://console.cloud.google.com)
2. OAuth consent screen
3. Test users → Add Users
4. Agrega emails para testing

### 2. Probar el Flujo

```bash
# 1. Frontend
npm run dev

# 2. Backend
cd backend
python manage.py runserver

# 3. Navega a http://localhost:3000/login
# 4. Click en "Continuar con Google"
# 5. Selecciona tu cuenta de Google
# 6. Verifica que redirija a /auth/callback
# 7. Verifica que se guarden los tokens y redirija a /dashboard
```

### 3. Verificar en el Backend

```bash
# Ver usuarios creados
python manage.py shell

from apps.authentication.models import User
users = User.objects.filter(google_id__isnull=False)
for user in users:
    print(f"{user.email} - {user.first_name} {user.last_name}")
```

---

## 📝 Variables de Entorno Requeridas

### Backend (.env)
```bash
# Supabase
SUPABASE_URL=https://[tu-proyecto-id].supabase.co
SUPABASE_JWT_SECRET=tu_jwt_secret_de_supabase

# Google OAuth (opcional - solo si quieres validar directamente)
GOOGLE_CLIENT_ID=[TU_CLIENT_ID].apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-[TU_SECRET]

# CORS
CORS_ALLOWED_ORIGINS=https://rutago-nine.vercel.app,http://localhost:3000
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_SUPABASE_URL=https://hdshccvnvizoaumqpepq.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=tu_anon_key_de_supabase
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

---

## 🚀 Deployment

### Backend (Railway/Render)
1. Agrega las variables de entorno en el dashboard
2. Asegúrate de que `CORS_ALLOWED_ORIGINS` incluya el dominio de producción del frontend
3. Deploy!

### Frontend (Vercel)
1. Agrega las variables de entorno en Project Settings
2. `NEXT_PUBLIC_API_URL` debe apuntar al backend desplegado
3. Deploy!

---

## 🐛 Troubleshooting

### "Token de Supabase inválido o expirado"
- Verifica que `SUPABASE_JWT_SECRET` sea correcto
- Verifica que el token no haya expirado (vida útil: 1 hora por defecto)

### "No se pudo obtener el email del usuario"
- Verifica que el scope de Google incluya `email`
- Verifica que el usuario haya dado permiso para compartir su email

### "CORS error"
- Verifica que el dominio del frontend esté en `CORS_ALLOWED_ORIGINS`
- En desarrollo: `http://localhost:3000`
- En producción: `https://rutago-nine.vercel.app`

### "Redirect URI mismatch"
- Verifica que la URI en Google Cloud Console coincida exactamente con:
  `https://hdshccvnvizoaumqpepq.supabase.co/auth/v1/callback`

---

## 📚 Referencias

- [Supabase Auth Documentation](https://supabase.com/docs/guides/auth)
- [Google OAuth 2.0](https://developers.google.com/identity/protocols/oauth2)
- [Django REST Framework JWT](https://django-rest-framework-simplejwt.readthedocs.io/)

---

**✅ Status**: Configuración completa y lista para testing
**📅 Fecha**: 13 de Diciembre de 2025
**👨‍💻 Implementado por**: Claude Code
