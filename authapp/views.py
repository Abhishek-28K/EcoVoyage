from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserForm, UserProfileForm
import re
def landingpage(request):
    return render(request, 'authapp/home.html')

def loginpage(request):
    try:    
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            if not User.objects.filter(username=username).exists():
                messages.error(request, 'Invalid Username')
                return redirect("login")

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("mappage")
            else:
                messages.error(request, "Invalid Credentials")
                return redirect("login")
    except Exception as e:
        print(e)
    return render(request, 'authapp/login.html')

def signuppage(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            try:
                if User.objects.filter(username=username).exists():
                    messages.info(request, "User with the same username already exists.")
                    return redirect("signup")
                user = User.objects.filter(email=email)
                if user.exists():
                    messages.info(request, "Email already exists.")
                    return redirect("signup")
                if len(password) < 8:
                    messages.error(request, "Password must be at least 8 characters long.")
                    return redirect("signup")
                if not re.search(r'[A-Za-z]', password):
                    messages.error(request, "Password must contain at least one letter.")
                    return redirect("signup")
                if not re.search(r'[0-9]', password):
                    messages.error(request, "Password must contain at least one number.")
                    return redirect("signup")
                else:
                    my_user = User.objects.create_user(username, email, password)
                    my_user.save()
                    messages.info(request, "Account created successfully. Please login to continue.")
                return redirect('login')
            except Exception as e:
                print(e)  
    except Exception as e:
        print(e)
    return render(request, 'authapp/signup.html')

def changepass(request):
    return render(request, 'authapp/changepass.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def view_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'authapp/view_profile.html', context)

@login_required
def edit_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('view_profile', user_id=user.id)
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=user.userprofile)
    return render(request, 'authapp/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})