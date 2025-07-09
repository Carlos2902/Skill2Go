# ============= imports for User registration ============ 
import json
from pyexpat.errors import messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from .forms import UserRegistrationForm 
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
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from dotenv import load_dotenv
import os
from .models import UserPreferenceDashboard
# ============= imports for SkillExchange   ============ 
from .models import SkillExchange
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
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
# ============= imports for the user preferences dashboard   ============ 
from .models import UserPreference
from .serializers import UserPreferenceSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# ============= imports for skill verification ============ 
from .forms import SkillCertificationForm
from .models import SkillCertification
from django.utils import timezone
from exchange.utils import hash_document
from blockchain.blockchain_integration import record_certification_on_chain
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')

@login_required
def dashboard(request):
    skill_requests = SkillExchange.objects.filter(providers__user=request.user, status="Pending").distinct()
    return render(request, 'dashboard.html', {'skill_requests': skill_requests})

class SkillPostAPI(APIView):
    permission_classes = [IsAuthenticated]
    MIXTRAL_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
    HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

    def get_user_preferences(self, user):
        preferences = UserPreferenceDashboard.objects.filter(user=user).first()        
        if not preferences:
            return None
        return {
            "skill_type": preferences.skill_type,
            "frequency": preferences.frequency,
            "personality": preferences.personality,
        }

    def save_user_preferences(self, user, preferences_data):
        preferences, created = UserPreferenceDashboard.objects.get_or_create(user=user)
        preferences.skill_type = preferences_data.get('skillType')
        preferences.frequency = preferences_data.get('frequency')
        preferences.personality = preferences_data.get('personality')
        preferences.save()

    def generate_prompt(self, preferences):
        return (
            f"Generate 2 engaging skill posts for someone interested in {preferences['skill_type']}. "
            f"The user prefers {preferences['frequency']} skill sessions and has a {preferences['personality']} personality. "
            "Each post should be in JSON format with a title, content, and an image URL." 
            "Make sure to get a random image link address based on the topic of the post."
        )
        

    def post(self, request):
        if request.data.get('skillType') and request.data.get('frequency') and request.data.get('personality'):
            self.save_user_preferences(request.user, request.data)
        user_preferences = self.get_user_preferences(request.user)
        if not user_preferences:
            return Response({'error': 'User preferences not found'}, status=404)
        prompt = self.generate_prompt(user_preferences)
        payload = {"inputs": prompt}
        response = requests.post(self.MIXTRAL_API_URL, headers=self.HEADERS, json=payload)
        if response.status_code == 200:
            return Response({"posts": response.json()}, status=200)
        return Response({"error": "Failed to generate posts"}, status=response.status_code)

@login_required
def profile_view(request):
    user = request.user
    skills = Skill.objects.none()  
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
    # skills by category with at least one provider
    def get_queryset(self):
        category_id = self.request.GET.get('category')
        queryset = Skill.objects.annotate(provider_count=Count('providers')).filter(provider_count__gt=0).prefetch_related(
            Prefetch(
                'providers',  # Related name for Skill -> SkillProvider
                queryset=SkillProvider.objects.select_related('user')  
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
                return not self.request.user.is_authenticated  
            def handle_no_permission(self):
                return redirect('profile') 
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
    next_page = reverse_lazy('login') 
    
class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm  
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
            provider_instance, created = SkillProvider.objects.get_or_create(user=request.user)
            # Check for creating a new skill or updating an existing one
            if custom_title: 
                new_skill = Skill(
                    title=custom_title,
                    description=description,
                    category=category,
                    image=image
                )
                new_skill.save() 
                new_skill.providers.add(provider_instance) 
                return redirect('profile') 
            else:  
                existing_skill = Skill.objects.filter(title=title).first()
                if existing_skill:
                    existing_skill.description = description
                    existing_skill.category = category
                    existing_skill.image = image
                    existing_skill.save() 
                    existing_skill.providers.add(provider_instance)
                    print("Existing Skill Updated:", existing_skill)  
                    return redirect('profile') 
                else:
                    form.add_error('title', "The selected skill does not exist.")
                    return render(request, 'add_skill.html', {'form': form})
        else:
            return render(request, 'homepage.html', {'form': form})
    else:
        form = SkillForm(user=request.user)
        return render(request, 'add_skill.html', {'form': form})
    
def manage_skills(request):
    user_skills = Skill.objects.filter(providers__user=request.user)
    return render(request, 'manage_skills.html', {'skills': user_skills})

from web3 import Web3

@login_required
def verify_skill(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id, providers__user=request.user)
    if request.method == 'POST':
        form = SkillCertificationForm(request.POST, request.FILES)
        if form.is_valid():
            certification = form.save(commit=False)
            certification.user = request.user
            certification.skill = skill
            certification.status = "Pending"
            certification.created_at = timezone.now()
            # checksum format applied to user address
            user_address = request.user.userprofile.ethereum_address  
            checksum_address = Web3.to_checksum_address(user_address.lower()) 
            document_hash = hash_document(certification.document)  
            tx_hash,cert_id = record_certification_on_chain(checksum_address, 
                                                            skill.title, 
                                                            document_hash)
            certification.blockchain_tx = tx_hash
            certification.on_chain_id = cert_id
            certification.save()
            return redirect('profile')
        else:
            print("Form errors:", form.errors)
    else:
        form = SkillCertificationForm(initial={'skill': skill})
    return render(request, 'verify_skill.html', {'form': form, 'skill': skill})


@csrf_exempt
def accept_skill_exchange(request, exchange_id):
    if request.method == 'POST': 
        exchange = get_object_or_404(SkillExchange, id=exchange_id)
        if request.user != exchange.requester and not exchange.providers.filter(user=request.user).exists():
            return JsonResponse({'error': 'You are not authorized to accept this request'}, status=403)
        exchange.status = "Accepted" 
        exchange.save()  
        return JsonResponse({'success': True, 'status': exchange.status})  
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def create_skill_exchange(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            skill_id = data.get('skill_id')
            provider_id = data.get('provider_id')
            skill = Skill.objects.get(id=skill_id)
            provider = SkillProvider.objects.get(id=provider_id)
            exchange = SkillExchange.objects.create(
                requester=request.user,
                skill=skill,
                status="Pending" 
            )
            exchange.providers.add(provider)
            exchange.save()  
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