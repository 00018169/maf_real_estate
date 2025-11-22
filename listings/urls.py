from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import views_api

router = DefaultRouter()
router.register(r'properties', views_api.PropertyViewSet)
router.register(r'appointments', views_api.AppointmentViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('property/create/', views.create_property, name='create_property'),
    path('property/update/<int:pk>/', views.update_property, name='update_property'),
    path('property/delete/<int:pk>/', views.delete_property, name='delete_property'),
    
    path('property/<int:pk>/book/', views.book_appointment, name='book_appointment'),
    path('my-properties/', views.my_properties, name='my_properties'),
    path('appointments/', views.my_appointments, name='my_appointments'),
    path('appointments/<int:pk>/<str:status>/', views.update_appointment_status, name='update_appointment_status'),
    
    # API
    path('api/', include(router.urls)),
]

