from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Menu(models.Model):
    class Types(models.IntegerChoices):
        STANDARD = 1
        GLUTEN_FREE = 2
        LACTOSE_FREE = 3
        VEGAN = 4

    title = models.CharField(max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type = models.SmallIntegerField(choices=Types.choices, default=Types.STANDARD)
    active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "type"],
                name="one_type_per_user",
            )
        ]

    def __str__(self):
        return f"{self.title} ({self.user.email})"


class Meal(models.Model):
    class Days(models.IntegerChoices):
        LUNEDÌ = 1
        MARTEDÌ = 2
        MERCOLEDÌ = 3
        GIOVEDÌ = 4
        VENERDÌ = 5

    class Weeks(models.IntegerChoices):
        SETTIMANA_1 = 1
        SETTIMANA_2 = 2
        SETTIMANA_3 = 3
        SETTIMANA_4 = 4

    first_course = models.CharField(max_length=200)
    second_course = models.CharField(max_length=200)
    side_dish = models.CharField(max_length=200)
    fruit = models.CharField(max_length=200)
    snack = models.CharField(max_length=200)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    day = models.SmallIntegerField(choices=Days.choices, default=Days.LUNEDÌ)
    week = models.SmallIntegerField(choices=Weeks.choices, default=Weeks.SETTIMANA_1)

    def __str__(self):
        return f"{self.menu.title} ({self.menu.get_type_display()} - {self.get_day_display()})"


@receiver(post_save, sender=Menu)
def menu_post_save(sender, instance, created, *args, **kwargs):
    # TODO: add check for week already present to implement automatic progressive week (up to 4)
    if created:
        menu = instance
        days_choices = Meal._meta.get_field("day").choices
        days = [label for label, day in days_choices]
        for day in days:
            meal = Meal.objects.create(menu=menu, day=day)
            meal.save()
