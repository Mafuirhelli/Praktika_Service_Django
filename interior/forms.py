from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from datetime import date
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

    def clean_date_of_birth(self):
        dob = self.cleaned_data['birthday']
        today = date.today()
        if (dob.year + 18, dob.month, dob.day) > (today.year, today.month, today.day):
            raise forms.ValidationError('Вам должно быть 18!')
        return dob


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин')
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input'}), validators=[RussianValidator()], error_messages={'required': 'Введите имя'})
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-input'}), validators=[RussianValidator()], error_messages={'required': 'Введите фамилию'})
    patronym = forms.CharField(label='Отчество', widget=forms.TextInput(attrs={'class': 'form-input'}),
                               validators=[RussianValidator()], error_messages={'required': 'Введите отчество'})
    birthday = forms.DateField(label='День рождения', widget=forms.DateInput(attrs={'class': 'form-input'}),
                               error_messages={'requied': 'Введите день рождения'})
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name','last_name', 'patronym', 'birthday', 'password1', 'password2']
        labels = {
            'email': 'E-mail',
            'patronym': 'Отчество'
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
    category = forms.MultipleChoiceField(choices=[(category.pk, category) for category in Category.objects.all()], widget=forms.CheckboxSelectMultiple())
    plan = forms.ImageField()
