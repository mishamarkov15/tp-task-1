import random

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.management import BaseCommand, CommandParser

from ask.models import Profile, Question


class Command(BaseCommand):
    help = '. '.join([
        "Заполнение БД рандомными данными в количестве <ratio>",
        "Пользователей: ratio",
        "Вопросы: ratio * 10",
        "Ответы: ratio * 100",
        "Тэги: ratio",
        "Оценки пользователей: ratio * 200",
    ])

    def add_arguments(self, parser: CommandParser, *args, **kwargs):
        parser.add_argument("ratio",
                            nargs='?',
                            type=int,
                            default=15000,
                            help='Коэффициент генерируемых данных. См. -h.'
                            )

    def generate_users(self, ratio: int, *args, **options):
        self.stdout.write(f"Generating {ratio} random users...")

        last_user_id = 0
        try:
            last_user_id = User.objects.order_by('-id').first().id
        except Exception:
            pass

        users = [
            User(
                username=f"username_{last_user_id + i}",
                first_name=f"Имя {last_user_id + i}",
                last_name=f"Фамилия {last_user_id + i}",
                email=f"user{last_user_id + i}_tp@mail.ru",
                password=make_password('admin'),
            ) for i in range(ratio)
        ]
        User.objects.bulk_create(users)
        self.stdout.write(f"Created {ratio} django.Users...")

        profiles = [
            Profile(
                user=User.objects.get(username=f"username_{last_user_id + i}"),
                avatar=None,
            ) for i in range(ratio)
        ]
        Profile.objects.bulk_create(profiles)
        self.stdout.write(f"{ratio} Profile objects was successfully created!")

    def generate_questions(self, ratio: int, *args, **options):
        self.stdout.write(f"Generating {ratio} random questions...")

        last_question_id = 0
        try:
            last_question_id = Question.objects.order_by('-id').first().id
        except Exception:
            pass

        profiles = Profile.objects.values_list('id', flat=True)

        questions = [
            Question(
                profile_id=random.choice(profiles),
                title=f'Вопрос #{i}',
                content=f'Задаю вопрос {i} на платформе. Не подскажите ответ?',
            )
            for i in range(ratio)
        ]
        Question.objects.bulk_create(questions)
        self.stdout.write(f"{ratio} random questions  was successfully created!")

    def handle(self, *args, **options):
        ratio = options['ratio']
        if ratio < 0:
            self.stderr.write("ratio не может быть отрицательным числом.")
            return
        self.generate_users(ratio, args, options)
        self.generate_questions(ratio * 10, args, options)
