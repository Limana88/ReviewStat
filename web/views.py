from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from web.forms import RegistrationForm, AuthForm
from web.models import UserProfile, Analyze

from django.contrib.auth import get_user_model, authenticate, login, logout

User = get_user_model()


def welcome_view(request):
    return HttpResponse("welcome")


@login_required
def main_view(request):
    user = request.user
    if request.user.is_authenticated:
        profile = get_object_or_404(UserProfile, user=user)
        return render(request, 'web/main_page.html', {'profile': profile})


def registration_view(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email']

            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            profile = UserProfile(
                user=user,
                name_company=form.cleaned_data['name_company']
            )
            profile.save()
            # login(request, user)
            # return redirect("auth")
            message = 'Регистрация прошла успешно!'
            messages.success(request, message)
            return redirect('auth')
    return render(request, 'web/registration.html', {'form': form})


def auth_view(request):
    form = AuthForm()
    if request.method == 'POST':
        form = AuthForm(data=request.POST)
        if form.is_valid():
            user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user is None:
                print(user)
            else:
                login(request, user)
                return redirect("main")
    return render(request, 'web/auth.html', {'form': form})


@login_required
def profile_view(request):
    user = request.user
    profile = get_object_or_404(UserProfile, user=user)
    return render(request, 'web/profile.html', {'profile': profile, 'user': user})


@login_required
def logout_view(request):
    logout(request)
    return redirect("auth")


@login_required
def delete_profile_view(request):
    user = get_object_or_404(User, id=request.user.id)
    user.delete()
    return redirect('registration')

@login_required
def analyze_view(request):
    user = get_object_or_404(User, id=request.user.id)
    profile = get_object_or_404(UserProfile, user=user)
    print(profile.name_company)
    analyze = get_object_or_404(Analyze, name_company=profile.name_company)
    return render(request, 'web/main_page.html', {'profile': profile, 'analyze': analyze})


