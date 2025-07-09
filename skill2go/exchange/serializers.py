from rest_framework import serializers
from .models import UserPreference

class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        fields = ['preferred_language', 'skill_level', 'learning_goals']

class UserPreferenceDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        fields = '__all__'