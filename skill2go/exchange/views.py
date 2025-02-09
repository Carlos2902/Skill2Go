# ============= imports for User registration ============ 
import json
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
# ============= imports for SkillExchange   ============ 
from .models import SkillExchange
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
    # Query skill exchanges where the current user is the provider
    skill_requests = SkillExchange.objects.filter(providers__user=request.user, status="Pending").distinct()
    
    return render(request, 'dashboard.html', {'skill_requests': skill_requests})

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
                try:
                    response = super().form_valid(form)
                    user = form.save()
                    login(self.request, user)
                    return response
                except Exception as e:
                    return JsonResponse({'error':str(e)}, status=500)

    
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



@csrf_exempt
def accept_skill_exchange(request, exchange_id):
    if request.method == 'POST':  # Fix typo
        exchange = get_object_or_404(SkillExchange, id=exchange_id)
        
        if request.user != exchange.requester and not exchange.providers.filter(user=request.user).exists():
            return JsonResponse({'error': 'You are not authorized to accept this request'}, status=403)
        
        exchange.status = "Accepted"  # Update status to Accepted
        exchange.save()  # Save the change
        
        return JsonResponse({'success': True, 'status': exchange.status})  # Fix typo in 'status'
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def create_skill_exchange(request):
    if request.method == 'POST':
        try:
            # Get the skill ID from the POST data
            data = json.loads(request.body)
            skill_id = data.get('skill_id')
            provider_id = data.get('provider_id')

            # Log the skill_id and provider_id for debugging
            print(f"Received Skill ID: {skill_id} and Provider ID: {provider_id}")

            # Get the skill and provider instances
            skill = Skill.objects.get(id=skill_id)
            provider = SkillProvider.objects.get(id=provider_id)

            # Log the skill and provider to check their values
            print(f"Skill: {skill.title}, Provider: {provider.user.username}")

            exchange = SkillExchange.objects.create(
                requester=request.user,
                skill=skill,
                status="Pending"  # Add status explicitly if it's required
            )

            # Add the provider to the ManyToManyField
            exchange.providers.add(provider)
            exchange.save()  # Save to ensure the relationship is persisted
            return JsonResponse({'success': True, 'message': 'Skill exchange request created'}, status=201)
        except Skill.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Skill Not Found'}, status=400)
        except SkillProvider.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Skill Provider Not Found'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)





def get_skill_providers(request, skill_id):
    try:
        skill = Skill.objects.get(id=skill_id)
        providers = [
            {
                'id': provider.id,
                'username': provider.user.username,
                'profile_picture_url': provider.user.userprofile.profile_picture.url if provider.user.userprofile.profile_picture else None
            }
            for provider in skill.providers.all()
        ]
        return JsonResponse({'providers': providers})
    except Skill.DoesNotExist:
        return JsonResponse({'error': 'Skill not found'}, status=404)
    except AttributeError as e:
        return JsonResponse({'error': f'Attribute error: {str(e)}'}, status=500)
    

@login_required
def ai_chat(request):

    user_language = "en" 
    try:
        user_preference = UserPreference.objects.get(user=request.user)
        user_language = user_preference.preferred_language  
    except UserPreference.DoesNotExist:
        pass 
    
    return render(request, 'ai_chat.html', {'user_language': user_language})

from .models import UserPreference
from .serializers import UserPreferenceSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response



@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def user_preferences(request):
    if request.method == "GET":
        preferences, created = UserPreference.objects.get_or_create(user = request.user)
        serializer = UserPreferenceSerializer(preferences)
        return Response (serializer.data)
    
    elif request.method == "POST":
        try:
            preference = request.user.preference
        except:
            if UserPreference.DoesNotExist:
                preference = None
                
        if not preference:
            preference = UserPreference(user=request.user)     
        serializer = UserPreferenceSerializer(data = request.data, instance = preference)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response (serializer.data)
        else:
            return Response (serializer.errors, status = 400)
         
 
@login_required(login_url="/login/")
def language_preferences(request):
    return render(request, 'language_preferences.html')