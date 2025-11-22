from rest_framework import serializers
from .models import Property, Appointment
from accounts.models import AgentProfile

class AgentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    class Meta:
        model = AgentProfile
        fields = ['id', 'username', 'agency_name', 'phone']

class PropertySerializer(serializers.ModelSerializer):
    agent = AgentSerializer(read_only=True)
    
    class Meta:
        model = Property
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

