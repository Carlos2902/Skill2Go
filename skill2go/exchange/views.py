# ============= imports for User registration ============ 
from pyexpat.errors import messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
# ============= imports for User registration ============ 
from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView
from .forms import UserLoginForm, UserProfileForm
from django.contrib.auth.views import LogoutView
# ============= imports for User update  ============ 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from .models import UserProfile
from django.contrib.auth.views import LoginView, LogoutView
# ============= imports for Dashboard   ============ 
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# ============= imports for searching   ============ 
from .models import Skill
# ============= imports for homepage   ============ 
from django.views.generic import TemplateView
# ============= imports for the skillForm  ============ 
from .forms import SkillForm
# ============= imports for the skill page  ============ 
from django.views.generic import ListView
from .models import Skill, SkillCategory, SkillProvider  
from django.db.models import Count, Prefetch
from django.shortcuts import render, redirect
from .models import Skill, SkillProvider
from .forms import SkillForm
from django.db import transaction
# import for not authenticated user:
from django.contrib.auth.mixins import UserPassesTestMixin


@login_required  
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def profile_view(request):
    user = request.user
    skills = Skill.objects.none()  # Default to an empty queryset
    
    # Check if user is associated with a SkillProvider
    try:
        skill_provider = SkillProvider.objects.get(user=user)
        skills = Skill.objects.filter(providers=skill_provider)
    except SkillProvider.DoesNotExist:
        pass
    
    context = {
        'user': user,
        'skills': skills,
    }
    return render(request, 'profile.html', context)

class HomePageView(TemplateView):
    template_name = 'homepage.html'
    
class SkillPageView(ListView):
    model = Skill
    template_name = 'skill.html'
    context_object_name = 'skills'

    # Filter skills by category with at least one provider
    def get_queryset(self):
        category_id = self.request.GET.get('category')

        # Prefetch providers to avoid extra queries
        queryset = Skill.objects.annotate(provider_count=Count('providers')).filter(provider_count__gt=0).prefetch_related(
            Prefetch(
                'providers',  # Related name for Skill -> SkillProvider
                queryset=SkillProvider.objects.select_related('user')  # Fetch user data with providers
            )
        )
        
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        return queryset

    


class UserRegisterView(UserPassesTestMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('edit_profile')

    def test_func(self):
        return not self.request.user.is_authenticated  # Deny access if user is authenticated

    def handle_no_permission(self):
        return redirect('profile')  # Redirect to profile if user is already logged in
    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response
    
    
class UserLoginView(FormView):
    template_name = 'login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('login')
    
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
    form_class = UserProfileForm  # Use the existing form for profile updates
    template_name = 'edit_profile.html'
    success_url = reverse_lazy('profile')
    
    def get_object(self):
        return self.request.user.userprofile

class UserLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    
class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')
    
def search_view(request):
    query = request.GET.get('q', '')
    results = Skill.objects.filter(
        name__icontains=query
    )
    return render(request, 'search_results.html', {'results': results, 'query': query})


@login_required
def add_skill(request):
    if request.method == 'POST':
        form = SkillForm(request.POST, request.FILES, user=request.user)
        print(f"User: {request.user}")
        print(f"User Profile: {getattr(request.user, 'userprofile', 'No profile found')}")

        if form.is_valid():
            title = form.cleaned_data['title']
            custom_title = form.cleaned_data['custom_title']
            description = form.cleaned_data['description']
            category = form.cleaned_data['category']
            image = form.cleaned_data['image']
            
            # Automatically assign the logged-in user as the provider
            provider_instance, created = SkillProvider.objects.get_or_create(user=request.user)

            # Check if we're creating a new skill or updating an existing one
            if custom_title:  # If a custom skill is providedq
                new_skill = Skill(
                    title=custom_title,
                    description=description,
                    category=category,
                    image=image
                )
                new_skill.save()  # Save the new skill

                # Link the skill to the provider (logged-in user)
                new_skill.providers.add(provider_instance) 

                print("New Skill Saved:", new_skill)  # Debugging line
                return redirect('profile')  # Redirect after successful creation

            else:  # If an existing skill is selected
                existing_skill = Skill.objects.filter(title=title).first()
                if existing_skill:
                    existing_skill.description = description
                    existing_skill.category = category
                    existing_skill.image = image
                    existing_skill.save()  # Update the existing skill

                    # Link the skill to the provider (logged-in user)
                    existing_skill.providers.add(provider_instance)

                    print("Existing Skill Updated:", existing_skill)  # Debugging line
                    return redirect('profile')  # Redirect after update

                else:
                    form.add_error('title', "The selected skill does not exist.")
                    return render(request, 'add_skill.html', {'form': form})

        else:
            # If form is not valid, print errors
            print(f"Form errors: {form.errors}")  # Debugging line
            return render(request, 'homepage.html', {'form': form})

    else:
        form = SkillForm(user=request.user)
        return render(request, 'add_skill.html', {'form': form})


def edit_about_me(request):
    return render(request, '404.html')