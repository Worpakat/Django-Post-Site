# Create your views here.

from django.shortcuts import render, redirect
from .models import ImgPost 
from .forms import LoginForm, RegisterationForm,PostForm
from django.contrib import messages, auth
from django.contrib.auth.models import User

def home_page(request):
    
    if request.method == "POST":
        if "logout" in request.POST: #if 'LOGOUT' btn is clicked... 
            auth.logout(request)

    posts = ImgPost.objects.order_by("-publish_date") #Descending ordered by publish_date
    # SOURCE: https://docs.djangoproject.com/en/4.1/ref/models/querysets/#order-by
    context = {"posts":posts}
    
    return render(request=request, template_name='index.html', context=context)

def login(request):
    
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        
        if login_form.is_valid():
            post_data = login_form.cleaned_data
            user = auth.authenticate(request=request, username=post_data["username"], password=post_data["password"])
            
            if user:
                auth.login(request=request, user=user)
                return redirect("/")

            else:
                print("test")
                messages.error(request,"Username or/and password invalid.")
    
    else:
        login_form = LoginForm()

    context = {"login_form":login_form}

    return render(request=request, template_name='login.html', context=context)

def sign_up(request): #!!!!SIGNUP METHODU DEĞİŞTİRİLECEK: MUHTEMELEN UYGUN Bİ MODELFORM OLAYIYLA YAPILACAK!!!!

    if request.method == "POST":
        
        sign_up_form = RegisterationForm(request.POST)

        if sign_up_form.is_valid():
            post_info = sign_up_form.cleaned_data
            user_instantiable = True
            
            if post_info["password1"] != post_info["password2"]: #Passwordlar eşleşmiyorsa
                messages.warning(request=request, message="Passwords aren't matching.")
                user_instantiable = False
            
            if User.objects.filter(email=post_info["email"]).exists(): #Email zaten kayıtlı ise
                # https://docs.djangoproject.com/en/4.1/ref/models/querysets/#exists
                messages.warning(request=request, message="This email already used.")
                user_instantiable = False

            if User.objects.filter(username=post_info["username"]).exists(): #Username zaten kayıtlı ise
                messages.warning(request=request, message="This username already used.")
                user_instantiable = False

            if user_instantiable: #Add New User
                new_user = User.objects.create_user(
                    username=post_info["username"], 
                    email=post_info["email"],
                    password=post_info["password1"]
                    )
                new_user.save()
                auth.login(request=request, user=new_user)
                return redirect("/")
        else:
            messages.warning(request=request, message="An error occurred, sign up process is not succesfull.")
    else:
        sign_up_form = RegisterationForm()

    return render(request=request, template_name='sign_up.html', context={"sign_up_form":sign_up_form})

def post(request):

    if request.method == "POST":
        
        post_form = PostForm(request.POST, request.FILES)

        if post_form.is_valid():
            new_img_post = post_form.save(commit=False) #Because of we haven't assign user yet, we aren't commiting it for now.
            new_img_post.owner = auth.get_user(request) # Logged in user is assigned to post's owner.
            new_img_post.save()

            return redirect("home_page")
        else:
            messages.warning(request,"An error occurred, your post couldn't save.")
    else:
        post_form = PostForm()


    return render(request=request, template_name='post.html', context={"post_form":post_form})
    