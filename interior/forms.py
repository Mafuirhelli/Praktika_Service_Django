from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from datetime import datetime
from interior.models import Profile
from .models import Category


class RussianValidator:
    ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя- "
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else "Должны присутствовать только русские символы, дефис и пробел."

    def __call__(self, value):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code, params={"value": value})

class ProfileForm(forms.ModelForm):
    patronym = forms.CharField(label='Отчество', widget=forms.TextInput(attrs={'class': 'form-input'}), validators=[RussianValidator()], error_messages={'required': 'Введите отчество'})
    birthday = forms.DateField(label = 'День рождения', widget=forms.DateInput(attrs={'class': 'form-input'}), error_messages={'requied': 'Введите день рождения'})
    class Meta:
        model = Profile
        fields = ['patronym', 'birthday']

    def clean_birthday(self):
        dob = self.cleaned_data['birthday']
        age = (datetime.now() - dob).days / 365
        if age < 18:
            raise forms.ValidationError('18+')
        return dob


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин')
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input'}), validators=[RussianValidator()], error_messages={'required': 'Введите имя'})
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-input'}), validators=[RussianValidator()], error_messages={'required': 'Введите фамилию'})
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name','last_name', 'password1', 'password2']
        labels = {
            'email': 'E-mail',
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-input'}),
        }

        def clean_password2(self):
            cd = self.cleaned_data
            if cd['password'] != cd['password2']:
                raise ValidationError("Пароли не совпадают!")
            return cd['password2']


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(widget=forms.PasswordInput)

class QueryForm(forms.Form):
    title = forms.CharField(max_length=50)
    description = forms.CharField(max_length=1000)
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    plan = forms.ImageField()