from django.shortcuts import render
from django.views.generic import TemplateView


class IndexPageView(TemplateView):
    """
    Главная страница приложения, доступная по пути "/"
    """
    template_name = 'qantilope/index.html'
