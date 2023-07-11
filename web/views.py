from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json

from web.forms import RegistrationForm, AuthForm
from web.models import UserProfile, Analyze, DataAnalyze

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
    analyze = get_object_or_404(Analyze, name_company=profile.name_company)
    data_analyze_rating_distribution = get_object_or_404(DataAnalyze, name_company=profile.name_company, title='rating_distribution')
    data_analyze_avg_rating = get_object_or_404(DataAnalyze, name_company=profile.name_company, title='avg_rating')
    data_analyze_bigrams_bad_grades = get_object_or_404(DataAnalyze, name_company=profile.name_company, title='bigrams_bad_grades')
    data_analyze_bigrams_good_grades = get_object_or_404(DataAnalyze, name_company=profile.name_company,title='bigrams_good_grades')

    data_rating_distribution = {
        'labels': data_analyze_rating_distribution.labels,
        'values': data_analyze_rating_distribution.values,
        'label': data_analyze_rating_distribution.name_analyze
    }
    data_avg_rating = {
        'labels': data_analyze_avg_rating.labels,
        'values': data_analyze_avg_rating.values,
        'label': data_analyze_avg_rating.name_analyze
    }

    data_bigrams_bad_grades = {
        'labels': data_analyze_bigrams_bad_grades.labels,
        'values': data_analyze_bigrams_bad_grades.values,
        'label': data_analyze_bigrams_bad_grades.name_analyze
    }

    data_bigrams_good_grades = {
        'labels': data_analyze_bigrams_good_grades.labels,
        'values': data_analyze_bigrams_good_grades.values,
        'label': data_analyze_bigrams_good_grades.name_analyze
    }

    data_json_rating_distribution = json.dumps(data_rating_distribution)
    data_json_avg_rating = json.dumps(data_avg_rating)
    data_json_bigrams_bad_grades = json.dumps(data_bigrams_bad_grades)
    data_json_bigrams_good_grades = json.dumps(data_bigrams_good_grades)
    return render(request, 'web/main_page.html', {'profile': profile, 'analyze': analyze,
                                                  'data_rating_distribution': data_json_rating_distribution,
                                                  'data_avg_rating': data_json_avg_rating,
                                                  'data_bigrams_bad_grades': data_json_bigrams_bad_grades,
                                                  'data_bigrams_good_grades': data_json_bigrams_good_grades})


@login_required
def histogram_view(request):
    user = get_object_or_404(User, id=request.user.id)
    profile = get_object_or_404(UserProfile, user=user)
    data_analyze = get_object_or_404(DataAnalyze, name_company=profile.name_company, title='rating_distribution')
    data = {
        'labels': data_analyze.labels,
        'values': data_analyze.values,
        'label': data_analyze.name_analyze
    }
    data_json = json.dumps(data)

    print(data_json)

    return render(request, 'web/histogram_page.html', {'data': data_json})
