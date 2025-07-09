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
    ethereum_address = models.CharField(max_length=42, unique=True, null=True, blank=True)

    
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
    providers = models.ManyToManyField('SkillProvider', blank=True)  
    image = models.ImageField(upload_to='skill_images/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    def __str__(self):
        return self.title
    
class SkillExchange(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requests")
    providers = models.ManyToManyField('SkillProvider', blank=True)  
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[("Pending", "Pending"), ("Accepted", "Accepted"), ("Completed", "Completed")])
    blockchain_tx = models.CharField(max_length=255, null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Exchange {self.requester.username} - {self.skill.title}"
    
class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="preference")
    preferred_language = models.CharField(max_length=50, choices=[
        ("es", "Spanish"),
        ("fr", "French"),
        ("en", "English"),
    ])
    skill_level = models.CharField(max_length=50, choices=[
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ])
    learning_goals = models.TextField(blank=False, null=False, default = "")
    
    def __str__(self):
        return f"{self.user.username} Preferences"
    
class UserPreferenceDashboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skill_type = models.CharField(max_length=255)
    frequency = models.CharField(max_length=255)
    personality = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} Dashboard Preferences"

class SkillCertification(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Verified', 'Verified'),
        ('Rejected', 'Rejected'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    document = models.FileField(upload_to='certifications/')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    blockchain_tx = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    # solving the uint certiDication issue
    on_chain_id = models.PositiveBigIntegerField(null=True, blank=True, unique=True) 
    def __str__(self):
        return f"Certification for {self.user.username} in {self.skill.title}"
    

class BlockchainContract(models.Model):
    contract_address = models.CharField(max_length=255, unique=True)
    deployer_address = models.CharField(max_length=255, unique=True, null=True, blank=True)  # ✅ New Field
    deployed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contract at {self.contract_address} (Deployer: {self.deployer_address})"
    
