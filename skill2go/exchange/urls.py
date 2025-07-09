from django.urls import path
from .views import UserRegisterView, UserLoginView, UserLogoutView, ProfileEditView, HomePageView, SkillPageView,  add_skill, verify_skill, ai_chat, manage_skills
from .views import user_preferences, language_preferences, SkillPostAPI
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),
    path('skill/', SkillPageView.as_view(), name='skill'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('edit_profile/', ProfileEditView.as_view(), name='edit_profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('search/', views.search_view, name='search'),
    path('add_skill/', add_skill, name='add_skill'),
    path('accept_skill_exchange/', views.accept_skill_exchange, name='accept_skill_exchange'),
    path('create_skill_exchange/', views.create_skill_exchange, name='create_skill_exchange'),
    path('get_skill_providers/<int:skill_id>/', views.get_skill_providers, name='get_skill_providers'),
    path('ai_chat/', views.ai_chat, name='ai_chat'),
    # AI CHAT
    path("preferences/", user_preferences, name="user_preferences"),
    path("language/", language_preferences, name="language"),
    # Dashboard posts
    path("generate-skill-posts/", SkillPostAPI.as_view(), name="generate-skill-posts"),
    # verify skill exchange
    path('verify-skill/<int:skill_id>/', verify_skill, name='verify_skill'),
    path('manage-skills/', manage_skills, name='manage_skills'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
