from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .models import Property, Appointment
from .forms import PropertyForm, AppointmentForm
from accounts.models import AgentProfile

def home(request):
    query = request.GET.get('q')
    properties = Property.objects.all().order_by('-published_at')
    
    if query:
        properties = properties.filter(
            Q(title__icontains=query) | 
            Q(city__icontains=query) |
            Q(description__icontains=query)
        )
        
    context = {
        'properties': properties
    }
    return render(request, 'home.html', context)

@login_required
def my_properties(request):
    if not hasattr(request.user, 'agent_profile'):
        messages.error(request, "Access denied. Agents only.")
        return redirect('home')
    
    properties = Property.objects.filter(agent=request.user.agent_profile).order_by('-published_at')
    return render(request, 'listings/my_properties.html', {'properties': properties})

def property_detail(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    return render(request, 'listings/property_detail.html', {'property': property_obj})

@login_required
def create_property(request):
    if not hasattr(request.user, 'agent_profile'):
        messages.error(request, "Only agents can add properties.")
        return redirect('home')
        
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            prop = form.save(commit=False)
            prop.agent = request.user.agent_profile
            prop.save()
            messages.success(request, "Property listed successfully!")
            return redirect('home')
    else:
        form = PropertyForm()
    return render(request, 'listings/create_property.html', {'form': form})

@login_required
def update_property(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    
    if not hasattr(request.user, 'agent_profile') or property_obj.agent != request.user.agent_profile:
        messages.error(request, "You do not have permission to edit this property.")
        return redirect('home')

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Property updated successfully!")
            return redirect('property_detail', pk=pk)
    else:
        form = PropertyForm(instance=property_obj)
    return render(request, 'listings/update_property.html', {'form': form})

@login_required
def delete_property(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    
    if not hasattr(request.user, 'agent_profile') or property_obj.agent != request.user.agent_profile:
        messages.error(request, "Permission denied.")
        return redirect('home')
        
    if request.method == 'POST':
        property_obj.delete()
        messages.success(request, "Property deleted.")
        return redirect('home')
    return render(request, 'listings/delete_property.html', {'property': property_obj})

@login_required
def book_appointment(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appt = form.save(commit=False)
            appt.requester_user = request.user
            appt.property = property_obj
            appt.agent = property_obj.agent
            
            appt.end_time = appt.start_time + timedelta(hours=1)
            
            appt.save()
            messages.success(request, "Appointment requested successfully!")
            return redirect('my_appointments')
    else:
        form = AppointmentForm()
    return render(request, 'listings/book_appointment.html', {'form': form, 'property': property_obj})

@login_required
def my_appointments(request):
    user = request.user
    
    if hasattr(user, 'agent_profile'):
        appointments = Appointment.objects.filter(agent=user.agent_profile)
        is_agent = True
    else:
        appointments = Appointment.objects.filter(requester_user=user)
        is_agent = False
        
    return render(request, 'listings/appointments.html', {'appointments': appointments, 'is_agent': is_agent})

@login_required
def update_appointment_status(request, pk, status):
    appt = get_object_or_404(Appointment, pk=pk)
    
    if not hasattr(request.user, 'agent_profile') or appt.agent != request.user.agent_profile:
        messages.error(request, "Permission denied.")
        return redirect('my_appointments')
        
    if status in ['confirmed', 'cancelled']:
        appt.status = status
        appt.save()
        messages.success(request, f"Appointment {status}.")
        
    return redirect('my_appointments')
