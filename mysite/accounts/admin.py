from django.contrib import admin
from .models import VisitorProfile


@admin.register(VisitorProfile)
class VisitorProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "available_minutes")
