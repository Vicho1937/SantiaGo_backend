# 🎨 Guía de Integración para el Frontend

Esta es una guía rápida para que el equipo del frontend integre Google Auth con el backend.

---

## 📦 Lo que necesitas

### 1. Credenciales de Supabase

Ve a [Supabase Dashboard](https://supabase.com/dashboard) → Settings → API:

```bash
NEXT_PUBLIC_SUPABASE_URL=https://[tu-proyecto-id].supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<pregunta_al_equipo_backend>
```

### 2. URL del Backend

```bash
# Desarrollo
NEXT_PUBLIC_API_URL=http://localhost:8000/api

# Producción
NEXT_PUBLIC_API_URL=https://tu-backend-desplegado.railway.app/api
```

---

## 🚀 Implementación Rápida

### Paso 1: Instalar Supabase

```bash
npm install @supabase/supabase-js
```

### Paso 2: Configurar Supabase Client

```typescript
// lib/supabase.ts
import { createClient } from '@supabase/supabase-js'

export const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)
```

### Paso 3: Botón de Login con Google

```typescript
// components/GoogleLoginButton.tsx
'use client'

import { supabase } from '@/lib/supabase'

export function GoogleLoginButton() {
  const handleLogin = async () => {
    const { error } = await supabase.auth.signInWithOAuth({
      provider: 'google',
      options: {
        redirectTo: `${window.location.origin}/auth/callback`,
      },
    })

    if (error) {
      console.error('Error:', error.message)
    }
  }

  return (
    <button
      onClick={handleLogin}
      className="flex items-center gap-2 px-4 py-2 bg-white border rounded-lg hover:bg-gray-50"
    >
      <img src="/google-icon.svg" alt="Google" className="w-5 h-5" />
      Continuar con Google
    </button>
  )
}
```

### Paso 4: Página de Callback

```typescript
// app/auth/callback/page.tsx (App Router)
'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { supabase } from '@/lib/supabase'

export default function AuthCallback() {
  const router = useRouter()

  useEffect(() => {
    const handleCallback = async () => {
      try {
        // 1. Obtener sesión de Supabase
        const { data: { session }, error } = await supabase.auth.getSession()

        if (error) throw error

        if (!session?.access_token) {
          throw new Error('No se recibió token de autenticación')
        }

        // 2. Enviar token al backend
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/google`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            access_token: session.access_token,
          }),
        })

        const data = await response.json()

        if (!data.success) {
          throw new Error(data.message || 'Error en autenticación')
        }

        // 3. Guardar tokens del backend
        localStorage.setItem('access_token', data.tokens.accessToken)
        localStorage.setItem('refresh_token', data.tokens.refreshToken)
        localStorage.setItem('user', JSON.stringify(data.user))

        // 4. Redirigir según si es usuario nuevo o existente
        if (data.isNewUser) {
          router.push('/onboarding') // Primera vez
        } else {
          router.push('/dashboard') // Usuario existente
        }
      } catch (error) {
        console.error('Error en callback:', error)
        router.push('/login?error=auth_failed')
      }
    }

    handleCallback()
  }, [router])

  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto"></div>
        <p className="mt-4 text-gray-600">Procesando autenticación...</p>
      </div>
    </div>
  )
}
```

---

## 🔐 Usar el Token en Requests

```typescript
// lib/api.ts
export async function fetchWithAuth(endpoint: string, options: RequestInit = {}) {
  const token = localStorage.getItem('access_token')

  return fetch(`${process.env.NEXT_PUBLIC_API_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      ...options.headers,
    },
  })
}

// Ejemplo de uso
const response = await fetchWithAuth('/businesses/')
const businesses = await response.json()
```

---

## 📊 Respuesta del Backend

Cuando el usuario se autentica, el backend devuelve:

```typescript
interface AuthResponse {
  success: boolean
  message: string
  user: {
    id: string
    email: string
    username: string
    name: string
    first_name: string
    last_name: string
    avatar: string
    role: 'user' | 'staff' | 'admin'
    emailVerified: boolean
    // ... más campos
  }
  tokens: {
    accessToken: string
    refreshToken: string
    tokenType: 'Bearer'
    expiresIn: number // segundos
  }
  isNewUser: boolean
}
```

---

## ⚠️ Usuarios de Prueba

**IMPORTANTE**: La app está en modo de prueba en Google Cloud Console.

Solo estos usuarios pueden hacer login:
- Agrega tu email en: [Google Cloud Console](https://console.cloud.google.com) → OAuth consent screen → Test users

Para agregar más usuarios de prueba, contacta al equipo de backend.

---

## 🧪 Testing Local

```bash
# 1. Frontend
npm run dev
# http://localhost:3000

# 2. Backend (en otra terminal)
cd backend
python manage.py runserver
# http://localhost:8000

# 3. Prueba el flujo:
# - Ve a http://localhost:3000/login
# - Click en "Continuar con Google"
# - Inicia sesión con una cuenta de prueba
# - Verifica que redirija correctamente
```

---

## 🐛 Errores Comunes

### "Error en callback: No se recibió token de autenticación"
- Verifica que `NEXT_PUBLIC_SUPABASE_URL` y `NEXT_PUBLIC_SUPABASE_ANON_KEY` estén configurados
- Verifica que Google Auth esté habilitado en Supabase Dashboard

### "CORS error"
- Verifica que el backend tenga tu dominio en `CORS_ALLOWED_ORIGINS`
- En desarrollo debe incluir: `http://localhost:3000`

### "Token de Supabase inválido o expirado"
- El token de Supabase tiene 1 hora de duración
- Si pasa mucho tiempo entre el login y el callback, puede expirar

---

## 📞 Contacto

Si tienes problemas con la integración:
1. Revisa la documentación completa en `GOOGLE_AUTH_SUPABASE.md`
2. Verifica los logs del navegador (Console)
3. Contacta al equipo de backend

---

**✅ Backend Ready**: El endpoint está funcionando y listo para recibir requests
**🔗 Endpoint**: `POST /api/auth/google`
