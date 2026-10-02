from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-food/', views.add_food, name='add_food'),
    path('register/', views.register, name='register'),

    path('my-requests/', views.my_requests, name='my_requests'),
    path('request-food/<int:food_id>/', views.request_food, name='request_food'),

    path('manage-requests/', views.manage_requests, name='manage_requests'),
    path('accept-request/<int:request_id>/', views.accept_request, name='accept_request'),
    path('reject-request/<int:request_id>/', views.reject_request, name='reject_request'),

    path('my-pickups/', views.my_pickups, name='my_pickups'),
    path(
    'delivered-pickup/<int:pickup_id>/',
    views.delivered_pickup,
    name='delivered_pickup'
),
]