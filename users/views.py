from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('novels:novel_list')
    else:
        form = RegisterForm()
    return render(request, 'users/auth.html', {'form': form, 'type': 'register'})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('novels:novel_list')
    else:
        form = LoginForm()
    return render(request, 'users/auth.html', {'form': form, 'type': 'login'})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    return render(request, 'users/profile.html', {'user': request.user})
