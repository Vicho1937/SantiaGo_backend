"""
Servicio de integración con Google Gemini AI para RutaGO
"""
import os
import json
import google.generativeai as genai
from django.conf import settings
from apps.businesses.models import Business, Category
from apps.routes.models import Route


class GeminiService:
    """Servicio para interactuar con Google Gemini AI"""

    def __init__(self):
        """Inicializa el servicio de Gemini"""
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY no está configurada en las variables de entorno")

        genai.configure(api_key=api_key)
        # Usar Gemini 1.5 Pro - Modelo avanzado con mejor contexto y razonamiento
        # Gemini 1.5 Pro ofrece ventana de contexto de 2M tokens y mejor comprensión
        self.model = genai.GenerativeModel('gemini-1.5-pro')

        # Contexto del sistema para RutaGO
        self.system_context = """
Eres RutaGO, un asistente de inteligencia artificial experto en turismo y emprendimientos locales de Santiago, Chile.

Tu misión es ayudar a los usuarios a:
1. Descubrir negocios locales auténticos en Santiago
2. Crear rutas personalizadas de turismo basadas en negocios reales de nuestra base de datos
3. Recomendar experiencias basadas en sus preferencias
4. Proporcionar información cultural e histórica de Santiago
5. Sugerir actividades según categorías: gastronomía, hospedaje, turismo

Características de tu personalidad:
- Amigable y entusiasta sobre Santiago
- Conocedor de la cultura local chilena
- Proactivo en hacer sugerencias
- Conciso pero informativo
- Usa lenguaje casual chileno cuando sea apropiado

Cuando respondas:
- Sé breve y directo (máximo 3-4 párrafos)
- Usa emojis ocasionalmente para darle vida
- Menciona negocios específicos cuando sea relevante usando datos reales
- Ofrece opciones y alternativas
- Pregunta por preferencias si necesitas más información

IMPORTANTE - Reglas de Seguridad:
- NUNCA menciones emails, teléfonos o datos de contacto personales de negocios o usuarios
- NUNCA reveles información privada o sensible de la base de datos
- Solo menciona información pública: nombres de negocios, direcciones, categorías, descripciones, ratings
- Si te piden información sensible, responde educadamente que no puedes proporcionar ese tipo de datos

Cuando sugier as rutas:
- Usa negocios reales que te proporciono en el contexto
- Considera ubicaciones geográficas para crear rutas lógicas
- Ten en cuenta ratings y categorías para mejores recomendaciones
- Propón rutas de 3-5 lugares ordenados geográficamente

Recuerda: Estás aquí para hacer que la experiencia de descubrir Santiago sea memorable y auténtica usando información real de negocios locales.
"""

    def _get_safe_business_data(self, business):
        """Extrae solo datos seguros y públicos de un negocio"""
        return {
            'name': business.name,
            'category': business.category.name,
            'description': business.short_description,
            'neighborhood': business.neighborhood,
            'comuna': business.comuna,
            'address': business.address,
            'price_range': '$' * business.price_range,
            'rating': float(business.rating),
            'review_count': business.review_count,
            'verified': business.verified,
            # NO incluir: email, phone, owner, coordinates exactas
        }

    def _fetch_relevant_businesses(self, user_message: str, limit=10):
        """Busca negocios relevantes basados en el mensaje del usuario"""
        # Palabras clave para categorías
        category_keywords = {
            'comida': ['comida', 'restaurant', 'comer', 'almuerzo', 'cena', 'café', 'cafetería'],
            'turismo': ['turismo', 'visitar', 'museo', 'atracción', 'tour', 'paseo'],
            'hospedaje': ['hotel', 'hospedaje', 'dormir', 'hostal', 'alojamiento'],
        }

        # Detectar categoría en el mensaje
        message_lower = user_message.lower()
        matched_categories = []

        for category, keywords in category_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                matched_categories.append(category)

        # Buscar negocios
        businesses = Business.objects.filter(is_active=True)

        # Filtrar por categorías si se detectaron
        if matched_categories:
            categories = Category.objects.filter(slug__in=matched_categories)
            if categories.exists():
                businesses = businesses.filter(category__in=categories)

        # Ordenar por rating y limitar resultados
        businesses = businesses.order_by('-rating', '-review_count')[:limit]

        # Retornar datos seguros
        return [self._get_safe_business_data(b) for b in businesses]

    def _fetch_public_routes(self, limit=5):
        """Obtiene rutas públicas destacadas"""
        routes = Route.objects.filter(
            is_public=True,
            is_featured=True
        ).order_by('-created_at')[:limit]

        routes_data = []
        for route in routes:
            routes_data.append({
                'name': route.name,
                'description': route.description,
                'stops_count': route.stops_count,
                'duration': route.estimated_duration,
                'distance': route.total_distance,
                # NO incluir: user info
            })

        return routes_data

    def generate_response(self, user_message: str, conversation_history: list = None) -> str:
        """
        Genera una respuesta usando Gemini basada en el mensaje del usuario

        Args:
            user_message: Mensaje del usuario
            conversation_history: Lista de mensajes previos [{"role": "user"|"assistant", "content": "..."}]

        Returns:
            str: Respuesta generada por Gemini
        """
        try:
            # Obtener contexto de negocios relevantes
            businesses_context = self._fetch_relevant_businesses(user_message)

            # Construir el prompt completo con contexto e historial
            full_prompt = self._build_prompt(
                user_message,
                conversation_history,
                businesses_context
            )

            # Generar respuesta
            response = self.model.generate_content(full_prompt)

            return response.text

        except Exception as e:
            error_msg = str(e)
            print(f"Error al generar respuesta con Gemini: {error_msg}")
            
            # Log más detallado para debugging
            import traceback
            traceback.print_exc()
            
            # Mensaje de error más específico para el usuario
            if "API key" in error_msg.lower() or "authentication" in error_msg.lower():
                return "⚠️ Lo siento, hay un problema con la configuración del servicio. Por favor, contacta al administrador."
            elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
                return "⚠️ El servicio está temporalmente saturado. Por favor, intenta de nuevo en unos minutos."
            else:
                return "Lo siento, tuve un problema al procesar tu mensaje. ¿Podrías intentar de nuevo?"

    def _build_prompt(self, user_message: str, conversation_history: list = None, businesses_context: list = None) -> str:
        """Construye el prompt completo con contexto e historial"""
        prompt_parts = [self.system_context, "\n---\n"]

        # Agregar contexto de negocios si existe
        if businesses_context and len(businesses_context) > 0:
            prompt_parts.append("NEGOCIOS DISPONIBLES EN SANTIAGO (usa estos datos reales):\n")
            for i, business in enumerate(businesses_context, 1):
                prompt_parts.append(f"\n{i}. {business['name']}\n")
                prompt_parts.append(f"   - Categoría: {business['category']}\n")
                prompt_parts.append(f"   - Ubicación: {business['address']}, {business['neighborhood']}, {business['comuna']}\n")
                prompt_parts.append(f"   - Descripción: {business['description']}\n")
                prompt_parts.append(f"   - Precio: {business['price_range']}\n")
                prompt_parts.append(f"   - Rating: {business['rating']}/5.0 ({business['review_count']} reseñas)\n")
                if business['verified']:
                    prompt_parts.append(f"   - ✓ Negocio verificado\n")
            prompt_parts.append("\n---\n\n")

        # Agregar historial de conversación si existe
        if conversation_history:
            prompt_parts.append("Historial de conversación:\n")
            for msg in conversation_history[-5:]:  # Solo últimos 5 mensajes
                role = "Usuario" if msg["role"] == "user" else "RutaGO"
                prompt_parts.append(f"{role}: {msg['content']}\n")
            prompt_parts.append("\n")

        # Agregar mensaje actual del usuario
        prompt_parts.append(f"Usuario: {user_message}\n")
        prompt_parts.append("RutaGO:")

        return "".join(prompt_parts)

    def suggest_route(self, preferences: dict) -> str:
        """
        Sugiere una ruta basada en las preferencias del usuario

        Args:
            preferences: Dict con preferencias como categorías, duración, presupuesto, etc.

        Returns:
            str: Sugerencia de ruta personalizada
        """
        # Obtener negocios basados en preferencias
        businesses = Business.objects.filter(is_active=True)

        # Filtrar por categorías si se especificaron
        if 'categories' in preferences and preferences['categories']:
            categories = Category.objects.filter(slug__in=preferences['categories'])
            if categories.exists():
                businesses = businesses.filter(category__in=categories)

        # Ordenar por rating
        businesses = businesses.order_by('-rating', '-review_count')[:10]

        # Convertir a datos seguros
        businesses_data = [self._get_safe_business_data(b) for b in businesses]

        prompt_parts = [self.system_context, "\n---\n"]
        prompt_parts.append("NEGOCIOS DISPONIBLES (usa estos para crear la ruta):\n")

        for i, business in enumerate(businesses_data, 1):
            prompt_parts.append(f"\n{i}. {business['name']}\n")
            prompt_parts.append(f"   - Categoría: {business['category']}\n")
            prompt_parts.append(f"   - Ubicación: {business['address']}, {business['neighborhood']}, {business['comuna']}\n")
            prompt_parts.append(f"   - Descripción: {business['description']}\n")
            prompt_parts.append(f"   - Precio: {business['price_range']}\n")
            prompt_parts.append(f"   - Rating: {business['rating']}/5.0\n")

        prompt_parts.append(f"""

Como RutaGO, crea una ruta turística personalizada para Santiago usando SOLO los negocios listados arriba:

Preferencias del usuario:
{self._format_preferences(preferences)}

Proporciona:
1. Un nombre atractivo para la ruta
2. 3-5 lugares de la lista anterior en orden lógico geográfico
3. Tiempo estimado en cada lugar
4. Breve descripción de por qué es especial cada lugar
5. Tips útiles (transporte, mejor horario, etc.)

IMPORTANTE: USA SOLO NEGOCIOS DE LA LISTA PROPORCIONADA.
Formato claro y fácil de seguir.
""")

        try:
            response = self.model.generate_content("".join(prompt_parts))
            return response.text
        except Exception as e:
            print(f"Error al sugerir ruta: {str(e)}")
            return "No pude generar una ruta en este momento. Por favor, intenta de nuevo."

    def _format_preferences(self, preferences: dict) -> str:
        """Formatea las preferencias del usuario para el prompt"""
        formatted = []
        if 'categories' in preferences:
            formatted.append(f"- Categorías de interés: {', '.join(preferences['categories'])}")
        if 'budget' in preferences:
            formatted.append(f"- Presupuesto: {preferences['budget']}")
        if 'duration' in preferences:
            formatted.append(f"- Duración: {preferences['duration']}")
        if 'group_size' in preferences:
            formatted.append(f"- Tamaño del grupo: {preferences['group_size']}")

        return "\n".join(formatted) if formatted else "Sin preferencias específicas"


# Función para obtener instancia del servicio (lazy loading)
_gemini_service_instance = None

def get_gemini_service():
    """Obtiene la instancia del servicio Gemini (lazy loading)"""
    global _gemini_service_instance
    if _gemini_service_instance is None:
        _gemini_service_instance = GeminiService()
    return _gemini_service_instance
