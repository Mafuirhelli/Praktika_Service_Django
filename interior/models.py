from django.db import models
from django.urls import reverse
from datetime import date
from django.db.models import ForeignKey


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True, help_text="Enter a category of the request (3D Design, 2D Design, etc.)")
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('category-detail', args=[str(self.id)]) #Возвращает url для доступа к конкретной заявке.

class Query(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, help_text="Type a brief description of the interior")
    category = ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    plan = models.ImageField(upload_to ='images/', help_text="Select a cover for this request", null=True)
    creationDate = models.DateField(default=date.today)
    design = models.ImageField(upload_to ='images/', null=True)
    adminUserName = models.CharField(max_length=200, null = True, blank = True)
    LOAN_STATUS = (
        ('n', 'New'),
        ('a', 'Accepted for work'),
        ('d', 'Done'),
    )
    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='n')

    def get_absolute_url(self):
        return reverse('query-detail', args=[str(self.id)]) #Возвращает url для доступа к конкретной заявке.

    def __str__(self):
        return self.title #Строка для представления объекта Model.