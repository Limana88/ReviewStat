from django.shortcuts import render, redirect
from django.http import HttpResponse

from web.forms import RegistrationForm, AuthForm
from web.models import UserProfile

from django.contrib.auth import get_user_model, authenticate, login

User = get_user_model()


def main_view(request):
    return HttpResponse("Registration!")


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
            user.create()
            profile = UserProfile(
                user=user,
                name_company=form.cleaned_data['name_company']
            )
            profile.save()
            return redirect('main')
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
