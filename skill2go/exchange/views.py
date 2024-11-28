# ============= imports for User registration ============ 
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
# ============= imports for User registration ============ 
from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView
from .forms import UserLoginForm
from django.contrib.auth.views import LogoutView
# ============= imports for User update  ============ 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from .models import UserProfile
from django.contrib.auth.views import LoginView, LogoutView
# ============= imports for Dashboard   ============ 
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required  # Ensure the user is logged in
def dashboard(request):
    # You can pass any context you want to the template
    return render(request, 'dashboard.html')

@login_required
def profile_view(request):
    return render(request, 'profile.html')

class UserRegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name  = 'register.html'
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)

class UserLoginView(FormView):
    template_name = 'login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username = username, password = password)
        if user:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, "Invalid credentials")
            return self.form_invalid(form)
        
        
class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')  # Redirect to login page after logout


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    fields = ['skills_offered', 'skills_needed', 'profile_picture', 'location']
    template_name = 'edit_profile.html'
    success_url = reverse_lazy('dashboard')
    
    def get_object(self):
        try:
            return self.request.user.userprofile
        except UserProfile.DoesNotExist:
            # Redirect to a profile creation page if the user doesn't have a profile
            return redirect('create_profile')  # Adjust to your profile creation URL
    
    
class UserLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    
class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')