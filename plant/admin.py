from django.contrib import admin

# Register your models here.
from .models import PotRegistry, Plan

# Register account models
admin.site.register(PotRegistry)
admin.site.register(Plan)
