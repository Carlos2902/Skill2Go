from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Skill, SkillCategory, SkillProvider
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

    # Dropdown for existing skills
    title_choices = [("", "Choose an option...")] + [(skill.title, skill.title) for skill in Skill.objects.all()]
    title = forms.ChoiceField(
        choices=title_choices,
        label="Skill Title",
        required=False,  # Allow empty if the user is adding a custom skill
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Pop the user argument
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
        
        # Ensure only one of title or custom_title is provided for new skills
        if title and custom_title:
            raise forms.ValidationError("Please provide either an existing skill title or a new skill title, not both.")
        if not title and not custom_title:
            raise forms.ValidationError("Please provide either an existing skill title or a new skill title.")

        # Img validation
        if image:
            if not image.name.endswith(('png', 'jpeg', 'jpg')):
                raise forms.ValidationError("Please upload a valid png, jpeg, or jpg format for your image.")

        return cleaned_data
