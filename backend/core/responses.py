"""
Custom response handlers para mantener formato consistente
"""
from rest_framework.response import Response


def success_response(data=None, message="", status=200):
    """
    Formato de respuesta exitosa estándar
    
    Args:
        data: Datos a retornar
        message: Mensaje opcional
        status: HTTP status code
    
    Returns:
        Response con formato: {"success": True, "data": ..., "message": ...}
    """
    response_data = {
        "success": True,
        "data": data if data is not None else {},
    }
    
    if message:
        response_data["message"] = message
    
    return Response(response_data, status=status)


def error_response(message="Ha ocurrido un error", errors=None, status=400):
    """
    Formato de respuesta de error estándar
    
    Args:
        message: Mensaje de error principal
        errors: Diccionario de errores por campo
        status: HTTP status code
    
    Returns:
        Response con formato: {"success": False, "message": ..., "errors": ...}
    """
    response_data = {
        "success": False,
        "message": message,
    }
    
    if errors:
        response_data["errors"] = errors
    
    return Response(response_data, status=status)


def paginated_response(queryset, serializer_class, request, message=""):
    """
    Respuesta paginada estándar
    
    Args:
        queryset: QuerySet a paginar
        serializer_class: Clase del serializer
        request: Request object
        message: Mensaje opcional
    
    Returns:
        Response con datos paginados
    """
    from rest_framework.pagination import PageNumberPagination
    
    paginator = PageNumberPagination()
    paginator.page_size = int(request.query_params.get('per_page', 20))
    paginator.max_page_size = 100
    
    page = paginator.paginate_queryset(queryset, request)
    
    if page is not None:
        serializer = serializer_class(page, many=True, context={'request': request})
        
        response_data = {
            "success": True,
            "data": {
                "results": serializer.data,
                "pagination": {
                    "page": paginator.page.number,
                    "per_page": paginator.page_size,
                    "total": paginator.page.paginator.count,
                    "pages": paginator.page.paginator.num_pages,
                    "has_next": paginator.page.has_next(),
                    "has_prev": paginator.page.has_previous(),
                }
            }
        }
        
        if message:
            response_data["message"] = message
        
        return Response(response_data)
    
    # Si no hay paginación, retornar todos los resultados
    serializer = serializer_class(queryset, many=True, context={'request': request})
    return success_response(serializer.data, message)
