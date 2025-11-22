from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import AgentProfile, BuyerProfile

class AgentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=True)
    agency_name = forms.CharField(max_length=100, required=True)
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'agency_name', 'bio']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            AgentProfile.objects.create(
                user=user,
                phone=self.cleaned_data['phone'],
                agency_name=self.cleaned_data['agency_name'],
                bio=self.cleaned_data['bio']
            )
            # Add to group
            group, _ = Group.objects.get_or_create(name='Agent')
            user.groups.add(group)
        return user

class BuyerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            BuyerProfile.objects.create(
                user=user,
                phone=self.cleaned_data['phone']
            )
            # Add to group
            group, _ = Group.objects.get_or_create(name='Buyer')
            user.groups.add(group)
        return user

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class AgentProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = AgentProfile
        fields = ['phone', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }

class BuyerProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = BuyerProfile
        fields = ['phone']
