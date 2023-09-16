from import_export import resources

from .models import Meal


class MealResource(resources.ModelResource):
    def __init__(self, menu_id, week):
        self.menu_id = menu_id
        self.week = week

    def before_save_instance(self, instance, using_transactions, dry_run):
        """Override method to get menu and week fields compiled at runtime"""
        instance.menu_id = self.menu_id
        instance.week = self.week

    def get_queryset(self):
        """Override method to narrow queryset down to the menu and week provided"""
        return self._meta.model.objects.filter(menu=self.menu_id, week=self.week)

    class Meta:
        model = Meal
        import_id_fields = ("day",)
        fields = ("day", "first_course", "second_course", "side_dish", "fruit", "snack")
