import factory


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "accounts.CustomUser"

    email = factory.Sequence(lambda n: "user_%d@test.com" % n)
