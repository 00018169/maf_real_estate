from django.contrib import admin
from .models import Property, Appointment

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'city', 'agent', 'published_at')
    list_filter = ('city', 'property_type', 'has_gas', 'has_internet')
    search_fields = ('title', 'city', 'address')

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('property', 'requester_user', 'agent', 'start_time', 'status')
    list_filter = ('status', 'start_time')

admin.site.register(Property, PropertyAdmin)
admin.site.register(Appointment, AppointmentAdmin)
