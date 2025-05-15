from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from .forms import RegisterForm, LoginForm
from novels.models import Novel, SavedNovel
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

@login_required
def toggle_save_novel(request, novel_id):
    novel = get_object_or_404(Novel, id=novel_id)
    saved, created = SavedNovel.objects.get_or_create(user=request.user, novel=novel)
    if not created:
        saved.delete()
    return redirect('novels:novel_detail', novel_id=novel.id)

@login_required
def saved_novels(request):
    saved = request.user.saved_novels.select_related('novel')
    return render(request, 'users/saved.html', {'saved_novels': saved})
