from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView

from ask import models


class AsideColumnView(object):
    @property
    def top_flags(self):
        return models.Tag.objects.hot()[:5]


class IndexPageView(ListView, AsideColumnView):
    """
    Главная страница приложения, доступная по пути "/".

    TODO: в дальнейшем, когда мы подключим модели (models) к приложению, текущий класс будет унаследован от
    TODO: django.views.generic.ListView, что позволит нам корректно использовать параметр paginate_by.
    """
    template_name = 'ask/index.html'
    paginate_by = 10
    model = models.Question
    queryset = models.Question.objects.new_questions()
    extra_context = {
        'top_tags': AsideColumnView().top_flags
    }


class HotQuestionsPageView(ListView, AsideColumnView):
    """
    Страница с горячими новостями, доступная по пути "/hot/"

    TODO: в дальнейшем, когда мы подключим модели (models) к приложению, текущий класс будет унаследован от
    TODO: django.views.generic.ListView, что позволит нам корректно использовать параметр paginate_by.
    """
    template_name = 'ask/hot.html'
    paginate_by = 10
    model = models.Question
    queryset = models.Question.objects.popular()
    extra_context = {
        'top_tags': AsideColumnView().top_flags
    }


class QuestionPageView(DetailView, AsideColumnView):
    """
    Страница отображения вопроса, доступна по пути "/question/<int:pk>/"
    """
    template_name = 'ask/question.html'
    model = models.Question
    extra_context = {
        'top_tags': AsideColumnView().top_flags,
    }

    def get(self, request: HttpRequest, *args, **kwargs):
        """
        Пока временно передаем заглушку в качестве query_set
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        self.object = self.get_object()
        answers = models.Answer.objects.filter(question_id=self.object.pk)
        context = self.get_context_data(*args, **kwargs)
        context.update(paginate(answers, request, paginate_by=10, **kwargs))
        return self.render_to_response(context)


class AskPageView(TemplateView):
    """
    Страница создания нового вопроса, доступна по пути "/ask/"
    """
    template_name = 'ask/ask.html'


class TagPageView(DetailView, AsideColumnView):
    """
    Страница отображения вопросов по тегам, доступна по пути "/tag/blablabla"
    """
    template_name = 'ask/tag.html'
    model = models.Tag
    extra_context = {
        'top_tags': AsideColumnView().top_flags
    }

    def get(self, request: HttpRequest, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        self.object = self.get_object()
        questions = models.Question.objects.by_tag(self.object)
        context = self.get_context_data(*args, **kwargs)
        context.update(paginate(questions, request, paginate_by=10, **kwargs))
        return self.render_to_response(context)


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


def paginate(object_list: QuerySet, request: HttpRequest, paginate_by: int = 10, **kwargs) -> dict:
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

    context = {'page_obj': page_obj}

    return context
