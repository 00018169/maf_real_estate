from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AgentRegistrationForm, BuyerRegistrationForm, UserUpdateForm, AgentProfileUpdateForm, BuyerProfileUpdateForm

def register(request):
    return render(request, 'registration/register_choice.html')

def register_agent(request):
    if request.method == 'POST':
        form = AgentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = AgentRegistrationForm()
    return render(request, 'registration/register.html', {'form': form, 'type': 'Agent'})

def register_buyer(request):
    if request.method == 'POST':
        form = BuyerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = BuyerRegistrationForm()
    return render(request, 'registration/register.html', {'form': form, 'type': 'Buyer'})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = None
        
        if hasattr(request.user, 'agent_profile'):
            p_form = AgentProfileUpdateForm(request.POST, instance=request.user.agent_profile)
        elif hasattr(request.user, 'buyer_profile'):
            p_form = BuyerProfileUpdateForm(request.POST, instance=request.user.buyer_profile)
            
        if u_form.is_valid() and (p_form is None or p_form.is_valid()):
            u_form.save()
            if p_form:
                p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = None
        if hasattr(request.user, 'agent_profile'):
            p_form = AgentProfileUpdateForm(instance=request.user.agent_profile)
        elif hasattr(request.user, 'buyer_profile'):
            p_form = BuyerProfileUpdateForm(instance=request.user.buyer_profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'accounts/edit_profile.html', context)
