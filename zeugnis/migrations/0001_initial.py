# Generated by Django 4.2.13 on 2024-06-12 19:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="feedbackGeber",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("benutzername", models.CharField(max_length=200)),
                ("passwort", models.CharField(max_length=200)),
                ("angemeldet", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name_plural": "feedback Geber",
            },
        ),
        migrations.CreateModel(
            name="feedbackItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateField(default=datetime.date.today)),
                ("person", models.CharField(default="leer", max_length=200)),
                ("category", models.CharField(max_length=1000)),
                ("grading", models.SmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="mitarbeiter",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("vorname", models.CharField(default="leer", max_length=200)),
                ("name", models.CharField(default="leer", max_length=200)),
                ("initial", models.CharField(default="leer", max_length=200)),
            ],
            options={
                "verbose_name_plural": "mitarbeiter",
            },
        ),
    ]
