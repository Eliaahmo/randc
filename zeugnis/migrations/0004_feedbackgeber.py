# Generated by Django 4.2.13 on 2024-06-12 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("zeugnis", "0003_delete_feedbackgeber"),
    ]

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
        ),
    ]