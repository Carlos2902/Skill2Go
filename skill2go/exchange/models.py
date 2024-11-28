from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills_offered = models.TextField()
    skills_needed = models.TextField()
    profile_picture = models.ImageField(upload_to="profile_pics/", null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)


class Skill(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    
class SkillExchange(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requests")
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name="provides")
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[("Pending", "Pending"), ("Completed", "Completed")])
    created_at = models.DateTimeField(auto_now_add=True)
