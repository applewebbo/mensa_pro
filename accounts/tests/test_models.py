import pytest
from accounts.tests.factories import CustomUserFactory

pytestmark = pytest.mark.django_db


class TestCustomUser:
    def test_factory(self):
        """The factory produces a valid user instance"""

        user = CustomUserFactory()

        assert user is not None
        assert user.__str__() == "user_0@test.com"
