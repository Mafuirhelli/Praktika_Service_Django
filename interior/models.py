from django.db import models

from django.db import models
from django.urls import reverse


class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    preferences = models.TextField()
    def get_absolute_url(self):
        return reverse('client-detail', args=[str(self.id)])
    def __str__(self):
        return '%s, %s' % (self.last_name, self.first_name)


class Designer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    studio = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.specialty}'


class Project(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='projects')
    designer = models.ForeignKey(Designer, on_delete=models.SET_NULL, null=True, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    def __str__(self):
        return self.title


class ProjectStatus(models.Model):
    PROJ_STATUS = (
        ('n', 'New'),
        ('e', 'Enrolled'),
        ('d', 'Done'),
    )
    status = models.CharField(max_length=1, choices=PROJ_STATUS, blank=True, default='n', help_text='Project status')


class Service(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.name


class Review(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='reviews')
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # Рейтинг от 1 до 5
    comment = models.TextField()
    def __str__(self):
        return f'Review by {self.client} for {self.project}'

