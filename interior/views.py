from bs4.diagnose import profile
from django.contrib.auth import authenticate
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from .models import Query, Category
from django.views import generic
from django.contrib.auth import authenticate, login
from .forms import RegisterForm, ProfileForm, QueryForm, LoginForm, AddAdminForm
from django.contrib import messages
from .forms import LoginForm
from .forms import QueryForm
from django.contrib.auth.models import User
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy,reverse

def user_page(request):
    username = request.GET.get('username')
    return render(
        request,
        'userpage.html',
        context={'username': username, },
    )

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
        return render(request, 'interior/login.html', {'form': form})
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
            important = form.cleaned_data.get("important")
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
        return Query.objects.filter(author=self.request.user).ordered_by('-important')
class QueryDelete(DeleteView):
    success_url = reverse_lazy('querys')

class QueryListViewN(LoginRequiredMixin,generic.ListView):
    model = Query
    template_name ='interior/query_list_n.html'
    def get_queryset(self):
        return Query.objects.filter(author=self.request.user).order_by('-important').filter(status='n')
class QueryListViewA(LoginRequiredMixin,generic.ListView):
    model = Query
    template_name ='interior/query_list_a.html'
    def get_queryset(self):
        return Query.objects.filter(author=self.request.user).order_by('-important').filter(status='a')
class QueryListViewD(LoginRequiredMixin,generic.ListView):
    model = Query
    template_name ='interior/query_list_d.html'
    def get_queryset(self):
        return Query.objects.filter(author=self.request.user).order_by('-important').filter(status='d')

class QueryAddDesign(UpdateView):
    model = Query
    fields = ["design","status"]

class CategoryListView(LoginRequiredMixin,generic.ListView):
    model = Category
    template_name ='interior/categorys.html'

class CategoryDelete(DeleteView):
    model = Category
    success_url = reverse_lazy('categorys')

class CategoryDetailView(generic.DetailView):
    model = Category

class CategoryCreateView(CreateView):
    model = Category
    fields = '__all__'

class AdminQueryListView(LoginRequiredMixin,generic.ListView):
    model = Query
    template_name ='interior/admin_plea_list.html'
    def get_queryset(self):
        return Query.objects.order_by('-important')


class QueryAddDesign(UpdateView):
    model = Query
    fields = ["design","status"]

    template_name_suffix = "_add_design_form"

class SuperuserQueryListView(LoginRequiredMixin,generic.ListView):
    model = Query
    template_name ='interior/superuser_plea_list.html'
    def get_queryset(self):
        return Query.objects.filter(status='n').order_by('-important')

def QueryAddAdmin(request, pk):
    query = get_object_or_404(Query, pk=pk)
    admins = User.objects.all().filter(is_staff=True)

    if request.method == 'POST':

        form = AddAdminForm(request.POST)

        if form.is_valid():
            query.adminUserName = form.cleaned_data['adminUserName']
            query.save()

            return HttpResponseRedirect(reverse('supermanage') )

    else:
        form = AddAdminForm()
        return render(request, 'interior/query_add_admin_form.html', {'form': form, 'query':query, 'admins':admins})