from django.db import models
from django.urls import reverse
from datetime import date
from django.db.models import ForeignKey
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    patronym  = models.CharField(
        max_length=160,
        null=True,
        blank=True
    )
    birthday = models.DateField(
        null=True,
        blank=True
    )
    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True, help_text="Enter a category of the request (3D Design, 2D Design, etc.)")
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('category-detail', args=[str(self.id)]) #Возвращает url для доступа к конкретной заявке.

class Query(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, help_text="Type a brief description of the interior")
    category = ForeignKey('Category', on_delete=models.SET_NULL, null=True, help_text="Выберите категорию заявки")
    plan = models.ImageField(upload_to ='images/', help_text="Select a cover for this request", null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    creationDate = models.DateField(default=date.today)
    design = models.ImageField(upload_to ='images/', null=True)
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