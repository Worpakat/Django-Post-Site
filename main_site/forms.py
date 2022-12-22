from django import forms
from django.contrib.auth.models import User
from .models import ImgPost

class LoginForm(forms.Form):
    username = forms.CharField(max_length=64, label="Username")
    password = forms.CharField(max_length=64, label="Password", widget=forms.PasswordInput)

class RegisterationForm(forms.Form):
    username = forms.CharField(max_length=64, label="Username")
    email = forms.EmailField(max_length=200)
    password1 = forms.CharField(max_length=64, min_length=8, label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=64, min_length=8, label="Password Again", widget=forms.PasswordInput)
    

class PostForm(forms.ModelForm):
    class Meta:
        model = ImgPost
        exclude = ['publish_date', 'owner'] 
        #'fields' listine modelımıznı forma eklenecek fieldlarının adlarını gireriz.
        #Django'da bize ona uygun formu oluşturur.
    
