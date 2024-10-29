from django.shortcuts import render
from django.views.generic import TemplateView


class IndexPageView(TemplateView):
    """
    Главная страница приложения, доступная по пути "/"
    """
    template_name = 'ask_markov/index.html'


class QuestionPageView(TemplateView):
    """
    Страница отображения вопроса, доступна по пути "/question/<int:pk>/"
    """
    template_name = 'ask_markov/question.html'


class AskPageView(TemplateView):
    """
    Страница создания нового вопроса, доступна по пути "/ask/"
    """
    template_name = 'ask_markov/ask.html'


class RegisterPageView(TemplateView):
    """
    Страница регистрации нового пользователя, доступна по пути "/register/"
    """
    template_name = 'ask_markov/register.html'


class LoginPageView(TemplateView):
    """
    Страница авторизации пользователя, доступна по пути "/login/"
    """
    template_name = 'ask_markov/login.html'


class LogoutPageView(TemplateView):
    """
    Страница выхода пользователя, доступна по пути "/logout/"
    """
    template_name = 'ask_markov/logout.html'


class SettingsPageView(TemplateView):
    """
    Страница редактирования профиля пользователя, доступна по пути "/settings/"
    """
    template_name = 'ask_markov/settings.html'
