from bs4.diagnose import profile
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from .models import Query, Category
from django.views import generic
from django.contrib.auth import authenticate, login
from .forms import RegisterForm, ProfileForm
from django.contrib import messages
from .forms import LoginForm

def index(request):
    num_queries_accepted = Query.objects.filter(status__exact='a').count()

    return render(
        request,
        'index.html',
        context={'num_queries_accepted':num_queries_accepted,},
    )
def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        profile_form = ProfileForm(request.POST)
        return render(request, 'interior/register.html', {'form': form, 'profile_form': profile_form})
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save(commit=False)
            profile = profile_form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            profile.save()
            messages.success(request, 'Вы успешно зарегестрировались')
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'interior/register.html', {'form': form, 'profile_form': profile_form})

def sign_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'interior/register.html', {'form': form})
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('userpage')
        else:
            return render(request, 'interior/register.html', {'form': form})

def user_page(request):
    username = request.GET.get('username')
    return render(
        request,
        'userpage.html',
        context={'username': username, },
    )

# def query_create(request):
#     pass
# class QueryDetailForm(generic.DetailView):\
#     model = Query