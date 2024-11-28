from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.forms import AuthenticationForm


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    skills_offered = forms.CharField(widget=forms.Textarea, label="Skills Offered", required=False)
    skills_needed = forms.CharField(widget=forms.Textarea, label="Skills Needed", required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
    
    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['skills_offered', 'skills_needed', 'profile_picture', 'location']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        label="Username"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label="Password"
    )