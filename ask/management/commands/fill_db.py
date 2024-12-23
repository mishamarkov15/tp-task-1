import random
from typing import Union, Type

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.management import BaseCommand, CommandParser
from django.db import models

from ask.models import Profile, Question, Tag, Answer, AnswerLike, QuestionLike


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
                password=make_password('admin', None, 'md5'),
            ) for i in range(ratio)
        ]
        objs = User.objects.bulk_create(users)
        self.stdout.write(f"Created {ratio} django.Users...")

        profiles = [
            Profile(
                user=obj,
                avatar=None,
            ) for obj in objs
        ]
        Profile.objects.bulk_create(profiles)
        self.stdout.write(f"{ratio} Profile objects was successfully created!")

    def generate_tags(self, ratio: int, *args, **options):
        self.stdout.write(f"Generating {ratio} random tags...")

        last_tag_id = 0
        try:
            last_tag_id = Tag.objects.order_by('-id').first().id
        except Exception:
            pass

        tags = [
            Tag(
                name=f"тэг {last_tag_id + i}"
            )
            for i in range(ratio)
        ]
        Tag.objects.bulk_create(tags)
        self.stdout.write(f"{ratio} random tags  was successfully created!")

    def generate_questions(self, ratio: int, *args, **options):
        self.stdout.write(f"Generating {ratio} random questions...")

        last_question_id = 0
        try:
            last_question_id = Question.objects.order_by('-id').first().id
        except Exception:
            pass

        profiles = Profile.objects.values_list('id', flat=True)
        tags = Tag.objects.values_list('id', flat=True)

        questions = [
            Question(
                profile_id=random.choice(profiles),
                title=f'Вопрос #{last_question_id + i}',
                content=f'Задаю вопрос {last_question_id + i} на платформе. Не подскажите ответ?',
            )
            for i in range(ratio)
        ]
        objs = Question.objects.bulk_create(questions)
        for question in objs:
            try:
                question.tags.add(
                    *list({Tag.objects.get(id=random.choice(tags)) for _ in range(random.randint(1, 10))}))
                question.save()
            except ValueError as ve:
                continue
        self.stdout.write(f"{ratio} random questions was successfully created!")

    def generate_answers(self, ratio: int, *args, **options):
        self.stdout.write(f"Generating {ratio} random answers...")

        last_answer_id = 0
        try:
            last_answer_id = Answer.objects.order_by('-id').first().id
        except Exception:
            pass

        questions = Question.objects.values_list('id', flat=True)
        profiles = Profile.objects.values_list('id', flat=True)

        answers = [
            Answer(
                content=f'Ответ {last_answer_id + i}. '
                        f'Это замечательный и развернутый ответ {last_answer_id + i} на вопрос.',
                question_id=random.choice(questions),
                profile_id=random.choice(profiles)
            )
            for i in range(ratio)
        ]
        Answer.objects.bulk_create(answers)
        self.stdout.write(f"{ratio} random answers  was successfully created!")

    def generate_likes(self, ratio: int,
                       _model_base: Union[Type[Answer], Type[Question]],
                       _model_like: Union[Type[AnswerLike], Type[QuestionLike]],
                       *args, **options):
        self.stdout.write(f"Generating {ratio} random likes for model {_model_like}...")

        objs = _model_base.objects.values_list('id', flat=True)
        profiles = Profile.objects.values_list('id', flat=True)

        likes = []
        existing_likes = set()  # тут хранятся пары существующих лайков
        for _ in range(ratio):
            # Пока пары лайк - ответ/вопрос не будем во множестве уже проставленных лайков, ищем снова
            obj_id = random.choice(objs)
            profile_id = random.choice(profiles)
            while (obj_id, profile_id) in existing_likes:
                obj_id = random.choice(objs)
                profile_id = random.choice(profiles)
            existing_likes.add((obj_id, profile_id))

            if _model_base == Answer:
                likes.append(
                    _model_like(
                        answer_id=obj_id,
                        profile_id=profile_id,
                    )
                )
            else:
                likes.append(
                    _model_like(
                        question_id=obj_id,
                        profile_id=profile_id
                    )
                )

        _model_like.objects.bulk_create(likes)
        self.stdout.write(f"{ratio} random likes {_model_like} was successfully created!")

    def handle(self, *args, **options):
        ratio = options['ratio']
        if ratio < 0:
            self.stderr.write("ratio не может быть отрицательным числом.")
            return
        self.generate_users(ratio, args, options)
        self.generate_tags(ratio, args, options)
        self.generate_questions(ratio * 10, args, options)
        self.generate_answers(ratio * 100, args, options)
        self.generate_likes(ratio * 150, Answer, AnswerLike, args, options)
        self.generate_likes(ratio * 50, Question, QuestionLike, args, options)
