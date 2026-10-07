from django.contrib import admin
from .models import Goal, Booth


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Booth)
class BoothAdmin(admin.ModelAdmin):
    list_display = ("name", "visit_duration")
    search_fields = ("name",)
    filter_horizontal = ("goals",)