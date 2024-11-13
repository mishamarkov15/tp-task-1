from django.core.management import BaseCommand
from ask.models import *


class Command(BaseCommand):
    help = 'Удаление всех данных из БД.'

    def handle(self, *args, **options):
        self.stdout.write(
            "Эта команда удалит ВСЕ данные из базы данных. Вы уверены, что хотите продолжить? [Y/n]: ",
            ending=""
        )
        answer = input()
        if answer.lower() != 'y':
            return
        Answer.objects.drop_table()
        self.stdout.write("таблица 'answer' очищена")

        AnswerLike.objects.drop_table()
        self.stdout.write("таблица 'answer_like' очищена")

        User.objects.all().delete()
        self.stdout.write("таблица 'auth_user' очищена")

        Profile.objects.drop_table()
        self.stdout.write("таблица 'profile' очищена")

        Question.objects.drop_table()
        self.stdout.write("таблица 'question' очищена")

        QuestionLike.objects.drop_table()
        self.stdout.write("таблица 'question_like' очищена")

        Tag.objects.drop_table()
        self.stdout.write("таблица 'tag' очищена")

