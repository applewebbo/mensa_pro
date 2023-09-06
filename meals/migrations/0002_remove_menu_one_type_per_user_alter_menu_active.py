# Generated by Django 4.2.5 on 2023-09-06 13:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("meals", "0001_initial"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="menu",
            name="one_type_per_user",
        ),
        migrations.AlterField(
            model_name="menu",
            name="active",
            field=models.BooleanField(default=False),
        ),
    ]
