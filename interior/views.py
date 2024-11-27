from django.shortcuts import render
from .models import Request
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
from .models import Author

def index(request):
    num_requests_accepted = Request.objects.filter(status__exact='a').count()

    return render(
        request,
        'index.html',
        context={'num_requests_accepted':num_requests_accepted,},
    )
class RequestListView(generic.ListView):
    model = Request.objects.filter(status__exact='a').order_by('-date')
    paginate_by = 4