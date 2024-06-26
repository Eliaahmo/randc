# Generated by Django 4.2.13 on 2024-06-16 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("zeugnis", "0004_feedbackgeber"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="feedbackgeber",
            options={"verbose_name_plural": "feedbackgeber"},
        ),
        migrations.AlterModelOptions(
            name="feedbackitem",
            options={"verbose_name_plural": "Feedback Rückmeldungen"},
        ),
        migrations.RenameField(
            model_name="feedbackgeber",
            old_name="passwort",
            new_name="password",
        ),
        migrations.AlterField(
            model_name="feedbackgeber",
            name="benutzername",
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
