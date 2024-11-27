from django.shortcuts import render
from .models import Query
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import permission_required
from .forms import RenewBookForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


def index(request):
    num_queries_accepted = Query.objects.filter(status__exact='a').count()

    return render(
        request,
        'index.html',
        context={'num_queries_accepted':num_queries_accepted,},
    )
class QueryListView(generic.ListView):
    model = Query.objects.filter(status__exact='a').order_by('-date')
    paginate_by = 4