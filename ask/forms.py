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
