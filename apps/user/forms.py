from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

from .models import UserProfile

User = get_user_model()

class EmailUserCreationForm(UserCreationForm):
    # Add bio manually since it's on the UserProfile model, not User
    bio = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Tell us about yourself (optional)...',
            'rows': 3,
            'class': 'form-control rounded-4'
        }),
        required=False,
        label="Bio"
    )

    class Meta:
        model = User
        fields = ("email", "username") # Added username here

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control rounded-pill py-2', 'placeholder': 'Email address'})
        self.fields['username'].widget.attrs.update({'class': 'form-control rounded-pill py-2', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control rounded-pill py-2', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control rounded-pill py-2', 'placeholder': 'Confirm Password'})

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            bio = self.cleaned_data.get('bio')
            if bio:
                profile, created = UserProfile.objects.get_or_create(user=user)
                profile.bio = bio
                profile.save()
        return user

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
