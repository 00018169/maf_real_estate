from django.db import models
from django.contrib.auth.models import User

class AgentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agent_profile')
    bio = models.TextField(blank=True)
    agency_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    
    def __str__(self):
        return f"Agent: {self.user.username}"

class BuyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer_profile')
    phone = models.CharField(max_length=20)
    
    def __str__(self):
        return f"Buyer: {self.user.username}"
