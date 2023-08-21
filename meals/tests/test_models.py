import pytest
from meals.tests.factories import MealFactory, MenuFactory

pytestmark = pytest.mark.django_db


class TestMenu:
    def test_factory(self):
        """The factory produces a valid model instance"""

        menu = MenuFactory(title="Menu Title")

        assert menu is not None
        assert menu.title == "Menu Title"


class TestMeal:
    def test_factory(self):
        """The factory produces a valid model instance"""

        meal = MealFactory()

        assert meal is not None
        assert meal.menu is not None
