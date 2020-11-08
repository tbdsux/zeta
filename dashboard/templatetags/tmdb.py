from django import template
import json

register = template.Library()


@register.filter(name="get_year")
def get_year(str_year):
    # return only the year
    return str(str_year).split("-")[0]


@register.filter(name="mdl_img")
def parse_mdl_img(image):
    # replace the image string
    return str(image).replace("s.jpg", "c.jpg")