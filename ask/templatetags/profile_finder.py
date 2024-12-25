from django import template

from ask import models

register = template.Library()


@register.filter()
def avatar(user_id: int) -> str:
    """
    Finds models.Profile by given user_id and returns it's avatar.
    :param user_id:
    :return:
    """
    return models.Profile.objects.get(user_id=user_id).avatar
