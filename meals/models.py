from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class School(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Menu(models.Model):
    class Types(models.IntegerChoices):
        STANDARD = 1
        GLUTEN_FREE = 2
        LACTOSE_FREE = 3
        VEGAN = 4

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type = models.SmallIntegerField(choices=Types.choices, default=Types.STANDARD)
    active = models.BooleanField(default=False)

    class Meta:
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=["user", "type"],
        #         name="one_type_per_user",
        #     )
        # ]
        ordering = ["type"]

    def __str__(self):
        return f"{self.school} ({self.get_type_display()})"


class Meal(models.Model):
    class Days(models.IntegerChoices):
        MONDAY = 1
        TUESDAY = 2
        WEDNESDAY = 3
        THURSDAY = 4
        FRIDAY = 5

    class Weeks(models.IntegerChoices):
        WEEK_1 = 1
        WEEK_2 = 2
        WEEK_3 = 3
        WEEK_4 = 4

    first_course = models.CharField(max_length=200)
    second_course = models.CharField(max_length=200)
    side_dish = models.CharField(max_length=200)
    fruit = models.CharField(max_length=200)
    snack = models.CharField(max_length=200)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="meals")
    day = models.SmallIntegerField(choices=Days.choices, default=Days.MONDAY)
    week = models.SmallIntegerField(choices=Weeks.choices, default=Weeks.WEEK_1)

    class Meta:
        ordering = ["day"]
        constraints = [
            models.UniqueConstraint(
                fields=["menu", "week", "day"], name="unique_menu_week_day"
            )
        ]

    def __str__(self):
        return f"{self.menu.school} ({self.menu.get_type_display()} - {self.get_day_display()})"


@receiver(post_save, sender=School)
def school_post_save(sender, instance, created, *args, **kwargs):
    """Create all menus related to the school with the default type active and the others not active"""
    if created:
        school = instance
        types = [label for label, day in Menu._meta.get_field("type").choices]
        default = Menu._meta.get_field("type").get_default()
        user = school.user
        for type in types:
            if type == default:
                meal = Menu.objects.create(
                    user=user, school=school, type=type, active=True
                )
            else:
                meal = Menu.objects.create(user=user, school=school, type=type)
            meal.save()
