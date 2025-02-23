from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post
from django.contrib.auth.models import Group

# Create your views here.


# HOME
def home(request):
    posts = Post.objects.all()
    return render(request, "first/home.html", {'posts': posts})

# About


def about(request):
    return render(request, "first/about.html")


# Contact
def contact(request):
    return render(request, "first/contact.html")


# Dashboard
def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        ip = request.session.get("ip", 0)
        return render(request, "first/dashboard.html", {'posts': posts, 'full_name': full_name, 'groups': gps, 'ip':ip})
    else:
        return HttpResponseRedirect("/login/")

# Logout


def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")

# Signup


def user_signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(
                request, "Congratulations!! You have become a Author....")
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form = SignUpForm()
    return render(request, "first/signup.html", {'form': form})


# Login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, "logged in Successfully")
                    return HttpResponseRedirect("/dashboard/")
        else:
            form = LoginForm()
        return render(request, "first/login.html", {'form': form})
    else:
        return HttpResponseRedirect("/dashboard/")


# add new post
def add_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                pst = Post(title=title, desc=desc)
                pst.save()
                form = PostForm()
        else:
            form = PostForm()
        return render(request, "first/addpost.html", {'form': form})
    else:
        return HttpResponseRedirect("/login/")


# Update  post
def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request, "first/updatepost.html", {'form': form})
    else:
        return HttpResponseRedirect("/login/")


# Delete  post
def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect("/dashboard/")
    else:
        return HttpResponseRedirect("/login/")
