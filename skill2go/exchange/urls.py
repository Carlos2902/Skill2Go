from django.urls import path
from .views import UserRegisterView, UserLoginView, UserLogoutView, ProfileEditView
from . import views
urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/edit/', ProfileEditView.as_view(), name='edit_profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
]
