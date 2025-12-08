from django.urls import path
from . import views

app_name = 'businesses'

urlpatterns = [
    # Categories
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    
    # Businesses
    path('', views.BusinessListView.as_view(), name='business-list'),
    path('<slug:slug>/', views.BusinessDetailView.as_view(), name='business-detail'),
    path('<uuid:business_id>/favorite/', views.favorite_business, name='favorite-business'),
    path('<uuid:business_id>/unfavorite/', views.unfavorite_business, name='unfavorite-business'),
    path('<uuid:business_id>/visit/', views.register_visit, name='register-visit'),
]
