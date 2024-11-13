from django.contrib.auth.models import User
from django.db import models
from django.db.models import Subquery, OuterRef


class Profile(models.Model):
    class Meta:
        db_table = "profile"
        verbose_name = "User profile"
        verbose_name_plural = "User's profiles"

    avatar = models.ImageField(verbose_name='Картинка профиля', help_text='Размер до 10МБ')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user.username} ({self.user.first_name} {self.user.last_name})"


class Tag(models.Model):
    class Meta:
        db_table = "tag"
        verbose_name = "Tag"
        verbose_name_plural = "Tag's"
        ordering = ['name']

    name = models.CharField(max_length=255, unique=True, blank=False, null=False, verbose_name='Наименование')
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self) -> str:
        return f"{self.name}"


class Question(models.Model):
    class Meta:
        db_table = "question"
        verbose_name = "Question"
        verbose_name_plural = "Question's"
        ordering = ["-created_timestamp"]

    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, verbose_name='Автор', null=True)
    title = models.CharField(max_length=255, verbose_name='Название', null=False, blank=False)
    content = models.TextField(verbose_name='Контент', help_text='Собственно сам вопрос', null=False, blank=False)
    tags = models.ManyToManyField(Tag, related_name='questions', verbose_name='теги', blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_timestamp = models.DateTimeField(auto_now=True, verbose_name='Время обновления')

    def __str__(self) -> str:
        return f"{self.title}"


class Answer(models.Model):
    class Meta:
        db_table = "answer"
        verbose_name = "Answer"
        verbose_name_plural = "Answer's"
        ordering = ["-created_timestamp"]

    content = models.TextField(null=False, blank=False, verbose_name='Ответ')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, verbose_name='Пользователь')
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_timestamp = models.DateTimeField(auto_now=True, verbose_name='Время обновления')

    def __str__(self) -> str:
        return f"{self.profile.user.username} в {self.updated_timestamp.strftime('%d.%m.%Y %H:%M')}"


class AnswerLike(models.Model):
    class Meta:
        db_table = "answer_like"
        verbose_name = "Answer Like"
        verbose_name_plural = "Answer Like's"
        unique_together = ('profile', 'answer',)

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='likes')
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Время лайка')

    def __str__(self) -> str:
        return f"{self.profile.user.username} [Ответ от: {self.answer.profile.user.username}]"


class QuestionLike(models.Model):
    class Meta:
        db_table = "question_like"
        verbose_name = "Question Like"
        verbose_name_plural = "Question Like's"
        unique_together = ('profile', 'question',)

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='likes')
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Время лайка')

    def __str__(self) -> str:
        return f"{self.profile.user.username} [{self.question.title[:50]}]"


class QuestionManager(models.Manager):
    def new_questions(self):
        return self.order_by('-created_timestamp')

    def popular(self):
        return self.annotate(
            popularity=Subquery(
                QuestionLike.objects.filter(
                    question_id=OuterRef('id')
                ).count()
            )
        ).order_by('popularity')
