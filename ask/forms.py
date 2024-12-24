from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
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

    template_name_div = 'forms/login-form.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'ask-field'


class SettingsForm(forms.ModelForm):
    template_name_div = 'forms/settings-form.html'

    old_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Укажите при изменении пароля',
        }
    ), label='Старый пароль', required=False)

    new_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Введите новый пароль',
        }
    ), label='Новый пароль', required=False)

    new_password_confirm = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Подтвердите новый пароль',
        }
    ), label='Подтверждение пароля', required=False)

    profile_picture = forms.ImageField(label='Загрузите новое фото', required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        labels = {
            'username': 'Никнейм',
            'email': 'Почта',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'ask-field'
