from bs4.diagnose import profile
from django.contrib.auth import authenticate
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from .models import Query, Category
from django.views import generic
from django.contrib.auth import authenticate, login
from .forms import RegisterForm, ProfileForm
from django.contrib import messages
from .forms import LoginForm
from .forms import QueryForm
from django.contrib.auth.models import User
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

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

def query_create(request):
    if request.method == 'GET':
        form = QueryForm()
        return render(request, 'interior/query_form.html', { 'form': form})
    if request.method == 'POST':
        form = QueryForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            description = form.cleaned_data.get("description")
            category = form.cleaned_data.get("category")
            if request.user.is_authenticated:
                username = request.user.username
            plan = form.cleaned_data.get("plan")
            obj = Query.objects.create(title = title, description = description, category = category, plan = plan, author = User.objects.get(username = username))
            obj.save()
            messages.success(request, 'Вы успешно создали заявку')
            return redirect('index')
        else:
            return render(request, 'interior/query_form.html', {'form': form})
class QueryDetailView(generic.DetailView):
    model = Query
class QueryListView(LoginRequiredMixin,generic.ListView):
    model = Query
    template_name ='interior/query_list.html'
    def get_queryset(self):
        return Query.objects.filter(author=self.request.user).ordered_by('creationDate')
class QueryDelete(DeleteView):
    success_url = reverse_lazy('querys')

class QueryListViewN(LoginRequiredMixin,generic.ListView):
    model = Query
    template_name ='interior/query_list_n.html'
    def get_queryset(self):
        return Query.objects.filter(author=self.request.user).order_by('creationDate').filter(status='n')
class QueryListViewA(LoginRequiredMixin,generic.ListView):
    model = Query
    template_name ='interior/query_list_a.html'
    def get_queryset(self):
        return Query.objects.filter(author=self.request.user).order_by('creationDate').filter(status='a')
class QueryListViewD(LoginRequiredMixin,generic.ListView):
    model = Query
    template_name ='interior/query_list_d.html'
    def get_queryset(self):
        return Query.objects.filter(author=self.request.user).order_by('creationDate').filter(status='d')