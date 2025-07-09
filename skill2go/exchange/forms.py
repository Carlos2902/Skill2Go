from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Skill, SkillCategory, SkillProvider, SkillCertification
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'cover_page', 'location','about_me', 'linkedin', 'facebook', 'instagram']
        
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        label="Username"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label="Password"
    )
    
class SkillForm(forms.ModelForm):
    custom_title = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter new skill name'}),
        label="New Skill Title"
    )
    class Meta:
        model = Skill
        fields = ['title', 'description', 'category', 'image']
    # Adding a custom widget for category dropdowns
    category = forms.ModelChoiceField(
        queryset=SkillCategory.objects.all(),
        empty_label="Select a Category",
    )
    image = forms.ImageField(
        required=True,
        label="Upload Skill Image"
    )
    title_choices = [("", "Choose an option...")] + [(skill.title, skill.title) for skill in Skill.objects.all()]
    title = forms.ChoiceField(
        choices=title_choices,
        label="Skill Title",
        required=False, 
    )
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  
        super(SkillForm, self).__init__(*args, **kwargs)
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        custom_title = cleaned_data.get("custom_title")
        image = cleaned_data.get("image")
        description = cleaned_data.get("description")
        if len(description) < 100:
            raise forms.ValidationError("Please provide a description of at least 100 characters.")
        if len(description) > 210:
            raise forms.ValidationError("Please provide a description of at most 210 characters")
        if title and custom_title:
            raise forms.ValidationError("Please provide either an existing skill title or a new skill title, not both.")
        if not title and not custom_title:
            raise forms.ValidationError("Please provide either an existing skill title or a new skill title.")
        if image:
            if not image.name.endswith(('png', 'jpeg', 'jpg')):
                raise forms.ValidationError("Please upload a valid png, jpeg, or jpg format for your image.")
        return cleaned_data


class SkillCertificationForm(forms.ModelForm):
    class Meta:
        model = SkillCertification
        fields = ['skill', 'document']
        widgets = {
            'skill': forms.HiddenInput(),
        }
    
    document = forms.FileField(
        required=True,
        label="Upload Certification Document",
        help_text="Accepted formats: PDF, JPG, PNG"
    )
    
    skill = forms.ModelChoiceField(
        queryset=Skill.objects.all(),
        empty_label="Select a Skill",
        label="Skill"
    )
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(SkillCertificationForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields['skill'].queryset = Skill.objects.filter(providers__user=self.user)
            
    def clean_document(self):
        document = self.cleaned_data.get("document")
        if document:
            allowed_formats = ['.pdf', '.jpg', '.jpeg', '.png']
            if not any(document.name.lower().endswith(ext) for ext in allowed_formats):
                raise forms.ValidationError("Please upload a valid PDF, JPG, or PNG file.")

        return document