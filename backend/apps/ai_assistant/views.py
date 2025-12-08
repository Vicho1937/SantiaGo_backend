"""
Vistas para el asistente AI RutaGO
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .services import get_gemini_service


@api_view(['POST'])
@permission_classes([AllowAny])  # Permitir acceso sin autenticación para el chatbot
def chat_view(request):
    """
    Endpoint para chat con RutaGO

    Body:
    {
        "message": "¿Qué lugares puedo visitar en Providencia?",
        "conversation_history": [
            {"role": "user", "content": "Hola"},
            {"role": "assistant", "content": "¡Hola! ¿Cómo puedo ayudarte?"}
        ]
    }
    """
    message = request.data.get('message')
    conversation_history = request.data.get('conversation_history', [])

    if not message:
        return Response({
            'error': 'El campo "message" es requerido'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Generar respuesta con Gemini
        gemini_service = get_gemini_service()
        response_text = gemini_service.generate_response(
            user_message=message,
            conversation_history=conversation_history
        )

        return Response({
            'response': response_text,
            'success': True
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'error': str(e),
            'success': False
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def suggest_route_view(request):
    """
    Endpoint para sugerencias de rutas personalizadas

    Body:
    {
        "preferences": {
            "categories": ["gastronomia", "turismo"],
            "budget": "medio",
            "duration": "4 horas",
            "group_size": "2-3 personas"
        }
    }
    """
    preferences = request.data.get('preferences', {})

    try:
        # Generar sugerencia de ruta
        gemini_service = get_gemini_service()
        route_suggestion = gemini_service.suggest_route(preferences)

        return Response({
            'route': route_suggestion,
            'success': True
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'error': str(e),
            'success': False
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check_view(request):
    """Verificar que el servicio de AI está funcionando"""
    try:
        # Test simple
        test_response = gemini_service.generate_response("Hola")
        return Response({
            'status': 'ok',
            'message': 'Gemini AI está funcionando correctamente',
            'test_response': test_response[:100] + "..."  # Primeros 100 caracteres
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
