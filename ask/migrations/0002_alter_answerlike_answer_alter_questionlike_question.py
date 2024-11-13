# Generated by Django 5.1.2 on 2024-11-13 13:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ask", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="answerlike",
            name="answer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="likes",
                to="ask.answer",
            ),
        ),
        migrations.AlterField(
            model_name="questionlike",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="likes",
                to="ask.question",
            ),
        ),
    ]