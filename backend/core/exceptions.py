from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    """
    Manejador de excepciones personalizado para retornar respuestas consistentes
    """
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response = {
            'success': False,
            'message': 'Error en la solicitud',
            'errors': response.data
        }
        
        return Response(custom_response, status=response.status_code)
    
    return response
