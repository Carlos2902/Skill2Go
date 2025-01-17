from django.urls import path
from .views import UserRegisterView, UserLoginView, UserLogoutView, ProfileEditView, HomePageView, SkillPageView,  add_skill
from . import views

# import settings and static
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


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
