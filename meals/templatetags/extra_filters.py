from django import template

register = template.Library()


@register.inclusion_tag("meals/includes/weekly-meals.html", takes_context=True)
def show_meals_of_the_week(context, week):
    if context["week_" + str(week) + "_meals"]:
        context["week_has_meals"] = True
        context["weekly_meals"] = context["week_" + str(week) + "_meals"]
    else:
        context["week_has_meals"] = False
    return context
