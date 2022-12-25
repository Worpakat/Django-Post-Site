# Create your views here.

from django.shortcuts import render, redirect
from .models import ImgPost 
from .forms import LoginForm, PostForm, SignUpForm, PasswordChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages, auth
from django.contrib.auth.models import User, Group, GroupManager
from django.contrib.auth.decorators import login_required, permission_required

def home_page(request):
    
    if request.method == "POST":
        user = request.user 
        post_is_be_deleted = ImgPost.objects.get(pk=request.POST["post_id"])
        
        if user == post_is_be_deleted.owner or user.has_perm("main_site.delete_imgpost"):
            post_is_be_deleted.delete()

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

def logout(request):

    auth.logout(request=request)

    return redirect("home_page")

def sign_up(request): 

    sign_up_form = SignUpForm(request.POST or None)
    
    if request.method == "POST":

        if sign_up_form.is_valid(): 
            new_user = sign_up_form.save()

            auth.login(request=request, user=new_user)
            
            default_group = Group.objects.get(name="default")
            default_group.user_set.add(new_user) #We added new_user to 'default' Group
            
            return redirect("/")

    return render(request=request, template_name='sign_up.html', context={"sign_up_form":sign_up_form})


@login_required(login_url="/login")
@permission_required(perm="main_site.add_imgpost", raise_exception=True)
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


@login_required(login_url="/login")
def password_change(request): 

    pass_change_form = PasswordChangeForm(user=request.user, data=request.POST or None)

    if request.method == "POST":

        if pass_change_form.is_valid(): 
            pass_change_form.save()
           
            messages.info(request,"Your password changed successfully.")

    return render(request=request, template_name='password_change.html', context={"pass_change_form":pass_change_form})

@permission_required(perm="auth.change_user", raise_exception=True)
def user_banning(request):

    if request.method == "POST":
        user = User.objects.get(pk=request.POST["user_id"])
        groups = Group.objects.filter(name__in=["default", "banned_users"])
        
        if user.has_perm("main_site.add_imgpost"):
            groups[0].user_set.add(user) #We added user to 'banned_users' Group
            groups[1].user_set.remove(user) #We removed user from 'default' Group
        else:
            groups[1].user_set.add(user) #We added user to 'default' Group
            groups[0].user_set.remove(user) #We removed user from 'banned_users' Group


    users = User.objects.filter(groups__name__in=["default", "banned_users"])
    user_perm_list = []
    
    for user in users:
        user_perm_list.append((user, user.has_perm("main_site.add_imgpost")))
        
    return render(request,"user_banning.html",{"user_perm_list":user_perm_list})

    