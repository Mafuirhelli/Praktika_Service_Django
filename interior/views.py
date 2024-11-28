from django.shortcuts import render, redirect
from .models import Query, Category
from django.views import generic
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import login

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
        return render(request, 'interior/register.html', {'form': form})
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'Вы успешно зарегестрировались')
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'interior/register.html', {'form': form})


# def query_create(request):
#     pass
# class QueryDetailForm(generic.DetailView):\
#     model = Query