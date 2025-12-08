from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('businesses/<uuid:business_id>/reviews/', views.ReviewListView.as_view(), name='review-list'),
    path('businesses/<uuid:business_id>/reviews/create/', views.create_review, name='review-create'),
    path('reviews/<uuid:review_id>/update/', views.update_review, name='review-update'),
    path('reviews/<uuid:review_id>/delete/', views.delete_review, name='review-delete'),
    path('reviews/<uuid:review_id>/helpful/', views.mark_helpful, name='review-helpful'),
]
