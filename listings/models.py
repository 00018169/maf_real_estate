from django.db import models
from django.contrib.auth.models import User
from accounts.models import AgentProfile

class Property(models.Model):
    TYPES = (
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
    )
    
    agent = models.ForeignKey(AgentProfile, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=200)
    description = models.TextField()
    property_type = models.CharField(max_length=10, choices=TYPES, default='sale', verbose_name="Type")
    price = models.DecimalField(max_digits=12, decimal_places=2)
    
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    area = models.DecimalField(max_digits=8, decimal_places=2, help_text="Square meters")
    floors_total = models.IntegerField()
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    
    # Booleans
    has_gas = models.BooleanField(default=False)
    has_electricity = models.BooleanField(default=False)
    has_internet = models.BooleanField(default=False)
    
    year_built = models.IntegerField()
    last_major_renovation_at = models.DateField(blank=True, null=True)
    
    published_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='properties/', blank=True, null=True)
    
    def __str__(self):
        return self.title

class Appointment(models.Model):
    STATUS = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )
    
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='appointments')
    requester_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    agent = models.ForeignKey(AgentProfile, on_delete=models.CASCADE, related_name='agent_appointments')
    
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    message = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-start_time']
        
    def __str__(self):
        return f"Appt: {self.requester_user.username} with {self.agent.user.username}"
