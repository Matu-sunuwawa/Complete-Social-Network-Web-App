from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
