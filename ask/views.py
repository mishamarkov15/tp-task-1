from django.shortcuts import render
from django.views.generic import TemplateView


class IndexPageView(TemplateView):
    """
    Главная страница приложения, доступная по пути "/"
    """
    template_name = 'ask/index.html'


class HotQuestionsPageView(TemplateView):
    """
    Страница с горячими новостями, доступная по пути "/hot/"
    """
    template_name = 'ask/hot.html'


class QuestionPageView(TemplateView):
    """
    Страница отображения вопроса, доступна по пути "/question/<int:pk>/"
    """
    template_name = 'ask/question.html'


class AskPageView(TemplateView):
    """
    Страница создания нового вопроса, доступна по пути "/ask/"
    """
    template_name = 'ask/ask.html'


class TagPageView(TemplateView):
    """
    Страница отображения вопросов по тегам, доступна по пути "/tag/blablabla"
    """
    template_name = 'ask/tag.html'


class RegisterPageView(TemplateView):
    """
    Страница регистрации нового пользователя, доступна по пути "/register/"
    """
    template_name = 'ask/register.html'


class LoginPageView(TemplateView):
    """
    Страница авторизации пользователя, доступна по пути "/login/"
    """
    template_name = 'ask/login.html'


class LogoutPageView(TemplateView):
    """
    Страница выхода пользователя, доступна по пути "/logout/"
    """
    template_name = 'ask/logout.html'


class SettingsPageView(TemplateView):
    """
    Страница редактирования профиля пользователя, доступна по пути "/settings/"
    """
    template_name = 'ask/settings.html'
