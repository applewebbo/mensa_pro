import factory


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "accounts.CustomUser"
