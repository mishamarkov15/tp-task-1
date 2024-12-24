from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView, UpdateView

from ask import models
from ask.forms import LoginForm, SettingsForm, RegisterForm


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

    def get(self, request: WSGIRequest, *args, **kwargs):
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

    def get(self, request: WSGIRequest, *args, **kwargs):
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


class RegisterPageView(TemplateView, AsideColumnView):
    """
    Страница регистрации нового пользователя, доступна по пути "/register/"
    """
    template_name = 'ask/register.html'
    extra_context = {
        'top_tags': AsideColumnView().top_flags,
        'form': RegisterForm()
    }

    def get(self, request: WSGIRequest, *args, **kwargs):
        if request.user.is_authenticated:
            return

    def post(self, request: WSGIRequest, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return redirect(reverse('home:settings', kwargs={"pk": user.pk}))
        return render(request, self.template_name, {'form': form})


class LoginPageView(TemplateView, AsideColumnView):
    """
    Страница авторизации пользователя, доступна по пути "/login/"
    """
    template_name = 'ask/login.html'
    extra_context = {
        'form': LoginForm(),
        'top_tags': AsideColumnView().top_flags,
    }

    def get(self, request: WSGIRequest, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('home:settings', kwargs={"pk": request.user.pk}))
        return super().get(request, *args, **kwargs)

    def post(self, request: WSGIRequest, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data.get('login')
            password = form.cleaned_data.get('password')

            user = auth.authenticate(request, username=login, password=password)
            if not user:
                user = auth.authenticate(request, email=login, password=password)

            if user:
                auth.login(request, user)
                return redirect(reverse('home:settings', kwargs={"pk": request.user.pk}))

        form.add_error(None, 'Неверно указан логин или пароль')
        return render(request, self.template_name, {'form': form})


class LogoutPageView(TemplateView, AsideColumnView):
    """
    Страница выхода пользователя, доступна по пути "/logout/"
    """
    template_name = 'ask/logout.html'
    extra_context = {
        'top_tags': AsideColumnView().top_flags,
    }

    def get(self, request: WSGIRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('home:index'))
        return super().get(request, *args, **kwargs)

    def post(self, request: WSGIRequest, *args, **kwargs):
        if request.user.is_authenticated:
            auth.logout(request)
        return redirect(reverse('home:index'))


class SettingsPageView(LoginRequiredMixin, UpdateView, AsideColumnView):
    """
    Страница редактирования профиля пользователя, доступна по пути "/settings/"
    """
    template_name = 'ask/settings.html'
    form_class = SettingsForm
    model = User
    extra_context = {
        'top_tags': AsideColumnView().top_flags,
    }

    def get_success_url(self):
        return reverse('home:settings', kwargs={'pk': self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SettingsForm(instance=self.get_object())
        return context


def paginate(object_list: QuerySet, request: WSGIRequest, paginate_by: int = 10, **kwargs) -> dict:
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
