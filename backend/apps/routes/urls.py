from django.urls import path
from . import views

app_name = 'routes'

urlpatterns = [
    path('', views.RouteListView.as_view(), name='route-list'),
    path('create/', views.RouteCreateView.as_view(), name='route-create'),
    path('<uuid:id>/', views.RouteDetailView.as_view(), name='route-detail'),
    path('<uuid:id>/update/', views.RouteUpdateView.as_view(), name='route-update'),
    path('<uuid:id>/delete/', views.RouteDeleteView.as_view(), name='route-delete'),
    path('<uuid:route_id>/like/', views.like_route, name='route-like'),
    path('<uuid:route_id>/unlike/', views.unlike_route, name='route-unlike'),
]
