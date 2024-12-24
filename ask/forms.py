from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from ask.models import Profile


class LoginForm(forms.Form):
    template_name_div = 'forms/login-form.html'

    login = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ваш email или username'
            }
        ),
        label='Логин',
        help_text='email or username')

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Ваш пароль',
            },
        ),
        label="Пароль")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'ask-field'


class SettingsForm(forms.ModelForm):
    template_name_div = 'forms/settings-form.html'

    profile_picture = forms.ImageField(label='Новый аватар', required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        labels = {
            'username': 'Никнейм',
            'email': 'Почта',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'ask-field'


class RegisterForm(forms.ModelForm):
    template_name_div = 'forms/register-form.html'

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Придумайте пароль',
            },
        ),
        label="Пароль")

    password_confirm = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Пароль ещё раз',
            },
        ),
        label="Подтверждение пароля"
    )

    avatar = forms.ImageField(required=False, label='Загрузка аватара', widget=forms.FileInput(attrs={
        'accept': 'image/png, image/gif, image/jpeg'
    }))

    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )
        labels = {
            'username': 'никнейм',
            'email': 'Почта'
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Разрешено использовать: A-Z, a-z, 0-9 и _'}),
            'email': forms.EmailInput(attrs={'placeholder': 'example@domain.ru'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'ask-field'

    def clean_password(self):
        password: str = self.cleaned_data.get('password')
        if not (8 <= len(password) <= 32):
            self.add_error('password', 'Длина пароля должна быть от 8 до 32 символов')
            raise ValidationError('Пароль указан неверно')
        if password.count(' ') != 0:
            self.add_error('password', 'Пароль не может содержать пробелов')
            raise ValidationError('Пароль содержит пробелы')
        if not any(sym in '$#!&.,-_+=' for sym in password):
            self.add_error('password', 'Пароль должен содержать хотя бы один специальный символ')
            raise ValidationError('Пароль не соответсвует требованиям')

        return password

    def clean(self):
        data = super().clean()
        if 'password' in self.cleaned_data.keys() and data.get('password') != data.get('password_confirm'):
            self.add_error('password_confirm', 'пароли не совпали')
            raise ValidationError("Пароли не совпадают")
        return data

    def save(self, commit=True):
        user: User = super().save(commit=False)

        user.set_password(self.cleaned_data.get('password'))

        user.save()

        profile = Profile.objects.create(user=user)
        print(self.cleaned_data)
        profile.avatar = self.cleaned_data.get('avatar', None)
        profile.save()

        return user
