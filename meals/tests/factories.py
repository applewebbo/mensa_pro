import factory


class SchoolFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "meals.School"

    user = factory.SubFactory("accounts.tests.factories.CustomUserFactory")


class MenuFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "meals.Menu"

    user = factory.SubFactory("accounts.tests.factories.CustomUserFactory")
    school = factory.SubFactory(
        "meals.tests.factories.SchoolFactory", user=factory.SelfAttribute("..user")
    )


class MealFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "meals.Meal"

    menu = factory.SubFactory("meals.tests.factories.MenuFactory")
