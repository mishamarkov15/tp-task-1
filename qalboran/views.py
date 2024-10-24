from django.shortcuts import render
from django.views.generic import TemplateView


class IndexPageView(TemplateView):
    """
    Главная страница приложения, доступная по пути "/"
    """
    template_name = 'qalboran/index.html'


class QuestionPageView(TemplateView):
    """
    Страница отображения вопроса, доступна по пути "/question/<int:pk>/"
    """
    template_name = 'qalboran/question.html'


class AskPageView(TemplateView):
    """
    Страница создания нового вопроса, доступна по пути "/ask/"
    """
    template_name = 'qalboran/ask.html'


class RegisterPageView(TemplateView):
    """
    Страница регистрации нового пользователя, доступна по пути "/register/"
    """
    template_name = 'qalboran/register.html'


class LoginPageView(TemplateView):
    """
    Страница авторизации пользователя, доступна по пути "/login/"
    """
    template_name = 'qalboran/login.html'


class SettingsPageView(TemplateView):
    """
    Страница редактирования профиля пользователя, доступна по пути "/settings/"
    """
    template_name = 'qalboran/settings.html'
