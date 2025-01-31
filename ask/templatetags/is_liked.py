from django import template
from django.contrib.auth.models import User

from ask import models

register = template.Library()


@register.filter(name='is_liked')
def is_liked(question: models.Question, user_pk: int) -> bool:
    """
    Returns true if question is liked by user.
    :param question:
    :param user:
    :return:
    """
    likes_on_question = models.QuestionLike.objects.filter(question_id=question.pk)
    like_for_profile = likes_on_question.filter(profile=models.Profile.objects.get(pk=user_pk))
    return like_for_profile.exists()
