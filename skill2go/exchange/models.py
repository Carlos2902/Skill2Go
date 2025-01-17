from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills_offered = models.ManyToManyField('Skill', related_name="offered_by_users", blank=True)
    skills_needed = models.ManyToManyField('Skill', related_name="needed_by_users", blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='assets/default_images/default-profile.png')
    cover_page = models.ImageField(upload_to='cover_pages/', default='assets/default_images/default-cover.png')
    location = models.CharField(max_length=255, null=True, blank=True)
    about_me = models.TextField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)


class SkillCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    


class SkillProvider(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user.email}"


class Skill(models.Model):
    title = models.CharField(max_length=255,  default='Default Skill Title')
    description = models.TextField()
    category = models.ForeignKey(
        'SkillCategory',
        on_delete=models.CASCADE,
        default=1,  
    )
    providers = models.ManyToManyField('SkillProvider', blank=True)  # Many-to-many relationship
    image = models.ImageField(upload_to='skill_images/', null=True, blank=True)
    def __str__(self):
        return self.title


    
class SkillExchange(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requests")
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name="provides")
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[("Pending", "Pending"), ("Completed", "Completed")])
    created_at = models.DateTimeField(auto_now_add=True)




