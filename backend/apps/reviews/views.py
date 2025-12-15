from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Count, Q, Avg
from apps.businesses.models import Business
from .models import Review, ReviewHelpful
from .serializers import ReviewSerializer, ReviewCreateSerializer, ReviewUpdateSerializer


class ReviewListView(generics.ListAPIView):
    """Listar reviews de un negocio"""
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        business_id = self.kwargs.get('business_id')
        queryset = Review.objects.filter(
            business_id=business_id,
            is_approved=True
        ).select_related('user', 'business')
        
        # Filtro por rating
        rating = self.request.query_params.get('rating')
        if rating:
            queryset = queryset.filter(rating=rating)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        business_id = kwargs.get('business_id')
        
        # Obtener estadísticas de reviews
        reviews = self.get_queryset()
        
        # Calcular distribución de ratings
        rating_distribution = {}
        for i in range(1, 6):
            rating_distribution[str(i)] = reviews.filter(rating=i).count()
        
        # Paginar resultados
        page = self.paginate_queryset(reviews)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            
            return Response({
                'success': True,
                'data': {
                    'results': paginated_response.data['results'],
                    'pagination': {
                        'page': request.query_params.get('page', 1),
                        'per_page': self.pagination_class.page_size,
                        'total': paginated_response.data['count'],
                        'pages': (paginated_response.data['count'] + self.pagination_class.page_size - 1) // self.pagination_class.page_size
                    },
                    'stats': {
                        'average_rating': round(reviews.aggregate(Avg('rating'))['rating__avg'] or 0, 2),
                        'total_reviews': reviews.count(),
                        'rating_distribution': rating_distribution
                    }
                }
            })
        
        serializer = self.get_serializer(reviews, many=True)
        return Response({
            'success': True,
            'data': {
                'results': serializer.data,
                'stats': {
                    'average_rating': round(reviews.aggregate(Avg('rating'))['rating__avg'] or 0, 2),
                    'total_reviews': reviews.count(),
                    'rating_distribution': rating_distribution
                }
            }
        })


class MyReviewsView(generics.ListAPIView):
    """Listar reviews del usuario autenticado"""
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Review.objects.filter(
            user=self.request.user
        ).select_related('user', 'business').order_by('-created_at')
    
    def list(self, request, *args, **kwargs):
        reviews = self.get_queryset()
        
        # Paginar resultados
        page = self.paginate_queryset(reviews)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return Response({
                'success': True,
                'data': {
                    'results': serializer.data,
                    'total': reviews.count()
                }
            })
        
        serializer = self.get_serializer(reviews, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request, business_id):
    """Crear una nueva review"""
    try:
        business = Business.objects.get(id=business_id, is_active=True)
    except Business.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Negocio no encontrado'
        }, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ReviewCreateSerializer(
        data=request.data,
        context={'request': request, 'business': business}
    )
    
    if serializer.is_valid():
        review = serializer.save()
        return Response({
            'success': True,
            'data': ReviewSerializer(review).data,
            'message': 'Reseña creada exitosamente'
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'errors': serializer.errors,
        'message': 'Error en la validación'
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_review(request, review_id):
    """Actualizar una review"""
    try:
        review = Review.objects.get(id=review_id, user=request.user)
    except Review.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Reseña no encontrada'
        }, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ReviewUpdateSerializer(review, data=request.data, partial=True)
    
    if serializer.is_valid():
        review = serializer.save()
        return Response({
            'success': True,
            'data': ReviewSerializer(review).data,
            'message': 'Reseña actualizada exitosamente'
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'errors': serializer.errors,
        'message': 'Error en la validación'
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request, review_id):
    """Eliminar una review"""
    try:
        review = Review.objects.get(id=review_id, user=request.user)
        business = review.business
        review.delete()
        
        # Actualizar rating del negocio
        business.update_rating()
        
        return Response({
            'success': True,
            'message': 'Reseña eliminada exitosamente'
        }, status=status.HTTP_200_OK)
    
    except Review.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Reseña no encontrada'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_helpful(request, review_id):
    """Marcar review como útil"""
    try:
        review = Review.objects.get(id=review_id)
    except Review.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Reseña no encontrada'
        }, status=status.HTTP_404_NOT_FOUND)
    
    helpful, created = ReviewHelpful.objects.get_or_create(
        review=review,
        user=request.user
    )
    
    if created:
        # Incrementar contador
        from django.db import models
        Review.objects.filter(id=review_id).update(helpful_count=models.F('helpful_count') + 1)
        
        return Response({
            'success': True,
            'message': 'Marcado como útil'
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': True,
        'message': 'Ya has marcado esta reseña como útil'
    }, status=status.HTTP_200_OK)
