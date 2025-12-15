from django.urls import path
from . import views

app_name = 'businesses'

urlpatterns = [
    # Categories
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    
    # Businesses públicos
    path('', views.BusinessListView.as_view(), name='business-list'),
    path('<slug:slug>/', views.BusinessDetailView.as_view(), name='business-detail'),
    path('<uuid:business_id>/favorite/', views.favorite_business, name='favorite-business'),
    path('<uuid:business_id>/unfavorite/', views.unfavorite_business, name='unfavorite-business'),
    path('<uuid:business_id>/visit/', views.register_visit, name='register-visit'),
    
    # Owner endpoints
    path('owner/profile/', views.owner_profile, name='owner-profile'),
    path('owner/my-businesses/', views.my_businesses, name='my-businesses'),
    path('owner/my-businesses/create/', views.create_my_business, name='create-my-business'),
    path('owner/my-businesses/<uuid:business_id>/', views.update_my_business, name='update-my-business'),
    path('owner/my-businesses/<uuid:business_id>/dashboard/', views.my_business_dashboard, name='my-business-dashboard'),
]
