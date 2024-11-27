from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date
from django.db.models import ForeignKey


class category(models.Model):
    name = models.CharField(max_length=200, unique=True, help_text="Enter a category of the request (3D Design, 2D Design, etc.)")
    def __str__(self):
        return self.name


class Request(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, help_text="Type a brief description of the interior")
    category = ForeignKey('category', on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to ='images/', help_text="Select a cover for this request", null=True)
    creator = ForeignKey(User, on_delete=models.SET_NULL, null=True)
    LOAN_STATUS = (
        ('n', 'New'),
        ('a', 'Accepted for work'),
        ('d', 'Done'),
    )
    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='n')
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title #Строка для представления объекта Model.


    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)]) #Возвращает url для доступа к конкретной заявке.
