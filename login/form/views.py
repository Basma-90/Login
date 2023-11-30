from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.urls import reverse
from django.core.mail import send_mail
from login import settings


def home(request):
    return render(request, 'home.html')
    

def signup(request):
    if request.method == 'POST':
        print(request.POST)
        
        username = request.POST['username']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('signup')
        
        if not username.isalnum():
            messages.error(request, 'Username should only contain letters and numbers')
            return redirect('signup')

        if len(username) < 4:
            messages.error(request, 'Username must be at least 4 characters')
            return redirect('signup')

        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters')
            return redirect('signup')

        if password != confirmpassword:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')

        if not any(char.isalpha() for char in password):
            messages.error(request, 'Password must contain at least one alphabet')
            return redirect('signup')
    
        user = User.objects.create_user(username=username,first_name=first_name,last_name=last_name, email=email, password=password)
        user.save()
        messages.success(request,'User created successfully')
        return redirect('login')
    else:
        return render(request, 'sign_up.html')

def login(request): 
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            f_name=user.first_name
            auth_login(request, user)
            messages.success(request, f'Logged in successfully, {f_name}')
            return render(request, 'home.html', {'f_name': f_name})
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('home')