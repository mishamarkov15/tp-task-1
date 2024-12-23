from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from ask import models


class IndexPageView(ListView):
    """
    Главная страница приложения, доступная по пути "/".

    TODO: в дальнейшем, когда мы подключим модели (models) к приложению, текущий класс будет унаследован от
    TODO: django.views.generic.ListView, что позволит нам корректно использовать параметр paginate_by.
    """
    template_name = 'ask/index.html'
    paginate_by = 10
    model = models.Question

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_tags'] = models.Tag.objects.hot()[:5]
        return context


class HotQuestionsPageView(TemplateView):
    """
    Страница с горячими новостями, доступная по пути "/hot/"

    TODO: в дальнейшем, когда мы подключим модели (models) к приложению, текущий класс будет унаследован от
    TODO: django.views.generic.ListView, что позволит нам корректно использовать параметр paginate_by.
    """
    template_name = 'ask/hot.html'
    # paginate_by = 10
    # model = models.Question


class QuestionPageView(TemplateView):
    """
    Страница отображения вопроса, доступна по пути "/question/<int:pk>/"
    """
    template_name = 'ask/question.html'

    def get(self, request: HttpRequest, *args, **kwargs):
        """
        Пока временно передаем заглушку в качестве query_set
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        comments = [
            f"This is comment {i + 1}" for i in range(44)
        ]
        return self.paginate(comments, request, paginate_by=5, **kwargs)

    def paginate(self, object_list: QuerySet, request: HttpRequest, paginate_by: int = 10, **kwargs):
        """
        Обработка исключений не нужна, так как если пользователь укажет неверный номер страницы,
        пагинатор не выкинет исключений, а вернет ближайшую корректную страницу.

        :param object_list: список ответов на вопрос.
        :param request:
        :param paginate_by:
        :param kwargs:
        :return:
        """
        p = Paginator(object_list, paginate_by)
        page_number = request.GET.get("page", 1)
        page_obj = p.get_page(page_number)

        context = self.get_context_data(**kwargs)
        context['page_obj'] = page_obj

        return render(request, self.template_name, context)


class AskPageView(TemplateView):
    """
    Страница создания нового вопроса, доступна по пути "/ask/"
    """
    template_name = 'ask/ask.html'


class TagPageView(TemplateView):
    """
    Страница отображения вопросов по тегам, доступна по пути "/tag/blablabla"

    TODO: в дальнейшем, когда мы подключим модели (models) к приложению, текущий класс будет унаследован от
    TODO: django.views.generic.ListView, что позволит нам корректно использовать параметр paginate_by.
    """
    template_name = 'ask/tag.html'
    # paginate_by = 10
    # model = models.Question


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
