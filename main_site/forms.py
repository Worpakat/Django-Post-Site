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
    
    def clean_username(self): #This works like a charm :D! Yeaap!
        username = self.cleaned_data["username"]

        if User.objects.filter(username=username).exists(): #If username already exists. 
            self.add_error(field="username", error="This username already exists. Please try another one.")
        
        return username
    
    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exists(): 
            self.add_error(field="email", error="This email already exists. Please try another one.")
        
        return email
    
    def clean(self):

        if self.cleaned_data["password1"] != self.cleaned_data["password2"]: 
            self.add_error(field=None, error="Passwords do not match.")
            # If field parameter is None, error will be inclueded to form errors.
        
        return self.cleaned_data

class PostForm(forms.ModelForm):
    class Meta:
        model = ImgPost
        exclude = ['publish_date', 'owner'] 
    
