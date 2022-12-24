from django import forms
from django.contrib.auth.models import User
from .models import ImgPost
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField(max_length=64, label="Username")
    password = forms.CharField(max_length=64, label="Password", widget=forms.PasswordInput)

class SignUpForm(UserCreationForm):
    
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        
    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exists(): 
            self.add_error(field="email", error="A user with that email address already exists.")
        
        return email 

class PostForm(forms.ModelForm):
    class Meta:
        model = ImgPost
        exclude = ['publish_date', 'owner'] 
    
