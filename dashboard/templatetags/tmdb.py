from django import template

register = template.Library()


@register.filter(name="get_year")
def get_year(str_year):
    # return only the year
    return str_year.split("-")[0]
