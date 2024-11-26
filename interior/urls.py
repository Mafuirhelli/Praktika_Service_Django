from django.urls import include
from django.urls import path

urlpatterns = [

]

urlpatterns += [
     path('catalog/', include('interior.urls')),
]

from django.views.generic import RedirectView
urlpatterns += [
    path('', RedirectView.as_view(url='/interior/', permanent=True)),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]