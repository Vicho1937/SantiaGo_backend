"""
Servicio de integración con Google Gemini AI para RutaGO
"""
import os
import google.generativeai as genai
from django.conf import settings


class GeminiService:
    """Servicio para interactuar con Google Gemini AI"""

    def __init__(self):
        """Inicializa el servicio de Gemini"""
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY no está configurada en las variables de entorno")

        genai.configure(api_key=api_key)
        # Usar Gemini 3 Pro - El modelo más avanzado de Google (Noviembre 2025)
        # Superior en comprensión multimodal, razonamiento y desarrollo de agentes de IA
        try:
            self.model = genai.GenerativeModel('gemini-3-pro')
        except:
            # Fallback a Gemini 2.5 Pro o 1.5 Pro si 3 Pro no está disponible
            try:
                self.model = genai.GenerativeModel('gemini-2.5-pro')
            except:
                self.model = genai.GenerativeModel('gemini-1.5-pro')

        # Contexto del sistema para RutaGO
        self.system_context = """
Eres RutaGO, un asistente de inteligencia artificial experto en turismo y emprendimientos locales de Santiago, Chile.

Tu misión es ayudar a los usuarios a:
1. Descubrir negocios locales auténticos en Santiago
2. Crear rutas personalizadas de turismo
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
- Menciona negocios específicos cuando sea relevante
- Ofrece opciones y alternativas
- Pregunta por preferencias si necesitas más información

Recuerda: Estás aquí para hacer que la experiencia de descubrir Santiago sea memorable y auténtica.
"""

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
            # Construir el prompt completo con contexto e historial
            full_prompt = self._build_prompt(user_message, conversation_history)

            # Generar respuesta
            response = self.model.generate_content(full_prompt)

            return response.text

        except Exception as e:
            print(f"Error al generar respuesta con Gemini: {str(e)}")
            return "Lo siento, tuve un problema al procesar tu mensaje. ¿Podrías intentar de nuevo?"

    def _build_prompt(self, user_message: str, conversation_history: list = None) -> str:
        """Construye el prompt completo con contexto e historial"""
        prompt_parts = [self.system_context, "\n---\n"]

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
        prompt = f"""
Como RutaGO, crea una ruta turística personalizada para Santiago basada en estas preferencias:

Preferencias del usuario:
{self._format_preferences(preferences)}

Proporciona:
1. Un nombre atractivo para la ruta
2. 3-5 lugares específicos para visitar en orden lógico
3. Tiempo estimado en cada lugar
4. Breve descripción de por qué es especial cada lugar
5. Tips útiles (transporte, mejor horario, etc.)

Formato claro y fácil de seguir.
"""

        try:
            response = self.model.generate_content(prompt)
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


# Instancia global del servicio
gemini_service = GeminiService()
