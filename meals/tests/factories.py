import factory


class MenuFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "meals.Menu"

    user = factory.SubFactory("accounts.tests.factories.CustomUserFactory")


class MealFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "meals.Meal"

    menu = factory.SubFactory("meals.tests.factories.MenuFactory")
