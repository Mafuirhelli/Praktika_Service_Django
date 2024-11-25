from django.contrib import admin

from .models import Client, Designer, Project, Service, Review
# Register your models here.
admin.site.register(Client)
admin.site.register(Designer)
admin.site.register(Project)
admin.site.register(Service)
admin.site.register(Review)
