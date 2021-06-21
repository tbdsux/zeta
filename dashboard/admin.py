from django.contrib import admin

# Register your models here.
from dashboard.models.collections import Collections, Inclution, Stuff

# register collection models
admin.site.register(Collections)
admin.site.register(Inclution)
admin.site.register(Stuff)
