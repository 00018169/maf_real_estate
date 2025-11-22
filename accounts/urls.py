from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('register/agent/', views.register_agent, name='register_agent'),
    path('register/buyer/', views.register_buyer, name='register_buyer'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
