# Generated by Django 4.2.13 on 2024-07-14 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("zeugnis", "0013_rename_category_fragenkatalog_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="fragenkatalog",
            options={},
        ),
        migrations.AddField(
            model_name="feedbackgeber",
            name="führungskraft",
            field=models.BooleanField(default=False),
        ),
    ]