from django.contrib import admin
from .models import SkillCategory, SkillProvider, Skill, SkillExchange

# Register models
admin.site.register(SkillCategory)
admin.site.register(SkillProvider)
admin.site.register(Skill)

admin.site.register(SkillExchange)
