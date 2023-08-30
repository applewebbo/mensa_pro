# Generated by Django 4.2.4 on 2023-08-21 07:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Menu",
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
                ("title", models.CharField(max_length=200)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "type",
                    models.SmallIntegerField(
                        choices=[
                            (1, "Standard"),
                            (2, "Gluten Free"),
                            (3, "Lactose Free"),
                            (4, "Vegan"),
                        ],
                        default=1,
                    ),
                ),
                ("active", models.BooleanField(default=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Meal",
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
                ("first_course", models.CharField(max_length=200)),
                ("second_course", models.CharField(max_length=200)),
                ("side_dish", models.CharField(max_length=200)),
                ("fruit", models.CharField(max_length=200)),
                ("snack", models.CharField(max_length=200)),
                (
                    "day",
                    models.SmallIntegerField(
                        choices=[
                            (1, "Lunedì"),
                            (2, "Martedì"),
                            (3, "Mercoledì"),
                            (4, "Giovedì"),
                            (5, "Venerdì"),
                        ],
                        default=1,
                    ),
                ),
                (
                    "week",
                    models.SmallIntegerField(
                        choices=[
                            (1, "Settimana 1"),
                            (2, "Settimana 2"),
                            (3, "Settimana 3"),
                            (4, "Settimana 4"),
                        ],
                        default=1,
                    ),
                ),
                (
                    "menu",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="meals.menu"
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="menu",
            constraint=models.UniqueConstraint(
                fields=("user", "type"), name="one_type_per_user"
            ),
        ),
    ]